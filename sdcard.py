# sdcard.py
# Driver minimalista para tarjetas SD vía SPI (MicroPython).
# Compatible con os.VfsFat: readblocks, writeblocks, ioctl.
#
# Uso típico:
#   from machine import Pin, SPI
#   import os, sdcard
#
#   spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0,
#             sck=Pin(18), mosi=Pin(19), miso=Pin(20))
#   cs  = Pin(21, Pin.OUT, value=1)
#   sd  = sdcard.SDCard(spi, cs)              # init a 1 MHz
#   vfs = os.VfsFat(sd)
#   os.mount(vfs, "/sd")
#
#   # Opcional: subir velocidad después de init
#   sd.set_frequency(10_000_000)

from time import ticks_ms, ticks_diff
from micropython import const

# Comandos SD (SPI mode)
_CMD0   = const(0x00)  # GO_IDLE_STATE
_CMD8   = const(0x08)  # SEND_IF_COND
_CMD9   = const(0x09)  # SEND_CSD
_CMD10  = const(0x0A)  # SEND_CID
_CMD12  = const(0x0C)  # STOP_TRANSMISSION
_CMD16  = const(0x10)  # SET_BLOCKLEN
_CMD17  = const(0x11)  # READ_SINGLE_BLOCK
_CMD18  = const(0x12)  # READ_MULTIPLE_BLOCK
_CMD24  = const(0x18)  # WRITE_BLOCK
_CMD25  = const(0x19)  # WRITE_MULTIPLE_BLOCK
_CMD55  = const(0x37)  # APP_CMD
_CMD58  = const(0x3A)  # READ_OCR

_ACMD41 = const(0x29)  # SD_SEND_OP_COND (ACMD)

_TOKEN_START_BLOCK   = const(0xFE)
_TOKEN_START_BLOCK_M = const(0xFC)
_TOKEN_STOP_TRAN     = const(0xFD)

_R1_IDLE_STATE = const(0x01)

# ioctl ops (MicroPython)
_IOCTL_INIT   = const(1)
_IOCTL_DEINIT = const(2)
_IOCTL_SYNC   = const(3)
_IOCTL_SEC_COUNT = const(4)
_IOCTL_SEC_SIZE  = const(5)

class SDCard:
    """Driver SD por SPI para MicroPython.

    - Soporta SDSC (byte addressing) y SDHC/SDXC (block addressing).
    - readblocks(sector, buf) / writeblocks(sector, buf) con sector de 512 bytes.
    - ioctl para VfsFat.
    """

    def __init__(self, spi, cs, baudrate=1_000_000, timeout_ms=1000):
        self.spi = spi
        self.cs = cs
        self.timeout_ms = timeout_ms
        self.cmdbuf = bytearray(6)
        self.dummy = b"\xFF"
        self.sector_size = 512
        self.high_capacity = False
        self._ocr = 0
        self._sectors = None

        # Selección inactiva
        self.cs.init(self.cs.OUT, value=1)

        # Ensure slow clock for init; some ports need reinit to change speed
        try:
            self.spi.init(baudrate=baudrate, polarity=0, phase=0)
        except TypeError:
            # Algunos ports no aceptan init completo, al menos reconfigura baudrate
            self.spi.init(baudrate=baudrate)

        self._init_card()

        # Subir un poco el clock por defecto tras init (puedes luego llamar a set_frequency)
        try:
            self.spi.init(baudrate=4_000_000, polarity=0, phase=0)
        except TypeError:
            self.spi.init(baudrate=4_000_000)

    # --------------------- Utilidades SPI/ChipSelect ---------------------

    def set_frequency(self, hz):
        """Cambia la frecuencia del SPI tras la inicialización."""
        try:
            self.spi.init(baudrate=hz, polarity=0, phase=0)
        except TypeError:
            self.spi.init(baudrate=hz)

    def _cs_low(self):
        self.cs(0)

    def _cs_high(self):
        self.cs(1)

    def _clock_dummy(self, n=10):
        # En SPI mode, hay que enviar unos clocks con CS alto antes de CMD0
        self._cs_high()
        for _ in range(n):
            self.spi.write(self.dummy)

    def _wait_token(self, token, timeout_ms=None):
        if timeout_ms is None:
            timeout_ms = self.timeout_ms
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < timeout_ms:
            b = self.spi.read(1, 0xFF)[0]
            if b == token:
                return True
        return False

    def _wait_not_busy(self, timeout_ms=None):
        if timeout_ms is None:
            timeout_ms = self.timeout_ms
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < timeout_ms:
            if self.spi.read(1, 0xFF)[0] == 0xFF:
                return True
        return False

    def _cmd(self, cmd, arg, crc):
        """Envia un comando y devuelve el primer byte R1."""
        self.cmdbuf[0] = 0x40 | cmd
        self.cmdbuf[1] = (arg >> 24) & 0xFF
        self.cmdbuf[2] = (arg >> 16) & 0xFF
        self.cmdbuf[3] = (arg >> 8) & 0xFF
        self.cmdbuf[4] = arg & 0xFF
        self.cmdbuf[5] = crc

        self._cs_low()
        # un dummy antes ayuda en algunos lectores
        self.spi.write(self.dummy)
        self.spi.write(self.cmdbuf)

        # Lee respuesta R1 (máx ~8 bytes)
        for _ in range(8):
            r = self.spi.read(1, 0xFF)[0]
            if r != 0xFF:
                return r
        return 0xFF  # timeout de R1

    def _cmd_r3(self, cmd, arg, crc):
        """CMD con respuesta R3/R7 (R1 + 4 bytes). Devuelve (r1, value32)."""
        r1 = self._cmd(cmd, arg, crc)
        val = 0
        if r1 <= 1:
            data = self.spi.read(4, 0xFF)
            val = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
        self._cs_high()
        self.spi.write(self.dummy)
        return r1, val

    def _cmd_nocs(self, cmd, arg, crc):
        """Como _cmd, pero no levanta CS automáticamente. Útil para secuencias ACMD."""
        self.cmdbuf[0] = 0x40 | cmd
        self.cmdbuf[1] = (arg >> 24) & 0xFF
        self.cmdbuf[2] = (arg >> 16) & 0xFF
        self.cmdbuf[3] = (arg >> 8) & 0xFF
        self.cmdbuf[4] = arg & 0xFF
        self.cmdbuf[5] = crc
        self._cs_low()
        self.spi.write(self.dummy)
        self.spi.write(self.cmdbuf)
        # leer r1
        for _ in range(8):
            r = self.spi.read(1, 0xFF)[0]
            if r != 0xFF:
                return r
        return 0xFF

    def _acmd(self, acmd, arg):
        """APP_CMD (CMD55) seguido del ACMDx, manteniendo CS bajo entre comandos."""
        # CMD55
        r = self._cmd_nocs(_CMD55, 0, 0x01)
        if r > 1:
            self._cs_high()
            self.spi.write(self.dummy)
            return r
        # ACMD
        # Para ACMD, el CRC normalmente no importa; 0x01 suele servir.
        r = self._cmd_nocs(acmd, arg, 0x01)
        self._cs_high()
        self.spi.write(self.dummy)
        return r

    # --------------------- Inicialización ---------------------

    def _init_card(self):
        # Clocks con CS alto
        self._clock_dummy(10)

        # CMD0: Idle
        r = self._cmd(_CMD0, 0, 0x95)
        self._cs_high()
        self.spi.write(self.dummy)
        if r != _R1_IDLE_STATE:
            raise OSError("SD: no entra en IDLE (CMD0) r=%d" % r)

        # CMD8: chequeo de tensión y versión (2.7-3.6V y patrón 0xAA)
        r, r7 = self._cmd_r3(_CMD8, 0x1AA, 0x87)  # 0x87 CRC válido para CMD8
        support_v2 = False
        if r == _R1_IDLE_STATE:
            # tarjeta SDv2 debería devolver eco 0x1AA
            if (r7 & 0xFFF) == 0x1AA:
                support_v2 = True

        # Espera ACMD41 hasta que salga de IDLE
        start = ticks_ms()
        arg = 0x40000000 if support_v2 else 0x00000000  # HCS si v2
        while True:
            r = self._acmd(_ACMD41, arg)
            if r == 0:
                break
            if ticks_diff(ticks_ms(), start) > self.timeout_ms:
                raise OSError("SD: timeout en ACMD41")

        # CMD58: leer OCR para confirmar HC
        r, ocr = self._cmd_r3(_CMD58, 0, 0x01)
        if r != 0:
            raise OSError("SD: CMD58 fallo r=%d" % r)
        self._ocr = ocr
        self.high_capacity = bool(ocr & 0x40000000)

        # Si no es SDHC, fija tamaño de bloque a 512 con CMD16
        if not self.high_capacity:
            r = self._cmd(_CMD16, self.sector_size, 0x01)
            self._cs_high()
            self.spi.write(self.dummy)
            if r != 0:
                raise OSError("SD: CMD16 fallo r=%d" % r)

        # Intenta calcular número de sectores leyendo CSD (opcional pero útil para ioctl)
        self._calc_sectors()

    def _calc_sectors(self):
        """Lee CSD y estima cantidad de sectores. Si falla, deja _sectors en None."""
        # CMD9 → CSD
        r = self._cmd(_CMD9, 0, 0x01)
        if r != 0:
            self._cs_high()
            self.spi.write(self.dummy)
            self._sectors = None
            return

        # Esperar token de inicio
        if not self._wait_token(_TOKEN_START_BLOCK, timeout_ms=self.timeout_ms):
            self._cs_high()
            self.spi.write(self.dummy)
            self._sectors = None
            return

        csd = bytearray(16)
        mv = memoryview(csd)
        self.spi.readinto(mv, 0xFF)

        # CRC (2 bytes)
        self.spi.read(2, 0xFF)
        self._cs_high()
        self.spi.write(self.dummy)

        csd_ver = (csd[0] >> 6) & 0x03
        if csd_ver == 1:
            # CSD v2.0 (SDHC/SDXC)
            c_size = ((csd[7] & 0x3F) << 16) | (csd[8] << 8) | csd[9]
            capacity = (c_size + 1) * 512 * 1024  # bytes
        else:
            # CSD v1.0 (SDSC)
            c_size = ((csd[6] & 0x03) << 10) | (csd[7] << 2) | ((csd[8] & 0xC0) >> 6)
            c_size_mult = ((csd[9] & 0x03) << 1) | ((csd[10] & 0x80) >> 7)
            read_bl_len = csd[5] & 0x0F
            block_len = 1 << read_bl_len
            mult = 1 << (c_size_mult + 2)
            capacity = (c_size + 1) * mult * block_len  # bytes

        if capacity >= 512:
            self._sectors = capacity // 512
        else:
            self._sectors = None

    # --------------------- API Vfs (read/write/ioctl) ---------------------

    def readblocks(self, block_num, buf):
        """Lee uno o más bloques de 512 bytes a 'buf'."""
        nbytes = len(buf)
        if nbytes % self.sector_size != 0:
            raise ValueError("Buffer size must be multiple of 512")
        nblocks = nbytes // self.sector_size

        # Dirección: en bloques si HC, en bytes si SDSC
        addr = block_num if self.high_capacity else block_num * self.sector_size

        if nblocks == 1:
            r = self._cmd(_CMD17, addr, 0x01)
            if r != 0:
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: CMD17 r=%d" % r)
            if not self._wait_token(_TOKEN_START_BLOCK):
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: timeout token READ")
            self.spi.readinto(buf, 0xFF)
            # descartar CRC
            self.spi.read(2, 0xFF)
            self._cs_high(); self.spi.write(self.dummy)
            return 0

        # Multiple
        r = self._cmd(_CMD18, addr, 0x01)
        if r != 0:
            self._cs_high(); self.spi.write(self.dummy)
            raise OSError("SD: CMD18 r=%d" % r)

        mv = memoryview(buf)
        off = 0
        for _ in range(nblocks):
            if not self._wait_token(_TOKEN_START_BLOCK):
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: timeout token READ mult")
            self.spi.readinto(mv[off: off + self.sector_size], 0xFF)
            self.spi.read(2, 0xFF)
            off += self.sector_size

        # STOP_TRANSMISSION
        self._cmd(_CMD12, 0, 0x01)
        self._cs_high(); self.spi.write(self.dummy)
        return 0

    def writeblocks(self, block_num, buf):
        """Escribe uno o más bloques de 512 bytes desde 'buf'."""
        nbytes = len(buf)
        if nbytes % self.sector_size != 0:
            raise ValueError("Buffer size must be multiple of 512")
        nblocks = nbytes // self.sector_size

        addr = block_num if self.high_capacity else block_num * self.sector_size

        if nblocks == 1:
            r = self._cmd(_CMD24, addr, 0x01)
            if r != 0:
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: CMD24 r=%d" % r)
            if not self._wait_not_busy():
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: busy antes de WRITE")
            # token + data + crc
            self.spi.write(bytes([_TOKEN_START_BLOCK]))
            self.spi.write(buf)
            self.spi.write(b"\xFF\xFF")
            # data response
            dr = self.spi.read(1, 0xFF)[0] & 0x1F
            if dr != 0x05:
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: data resp=%02x" % dr)
            if not self._wait_not_busy(self.timeout_ms):
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: busy tras WRITE")
            self._cs_high(); self.spi.write(self.dummy)
            return 0

        # multiple
        r = self._cmd(_CMD25, addr, 0x01)
        if r != 0:
            self._cs_high(); self.spi.write(self.dummy)
            raise OSError("SD: CMD25 r=%d" % r)

        mv = memoryview(buf)
        off = 0
        for _ in range(nblocks):
            if not self._wait_not_busy():
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: busy antes de WRITE mult")
            self.spi.write(bytes([_TOKEN_START_BLOCK_M]))
            self.spi.write(mv[off: off + self.sector_size])
            self.spi.write(b"\xFF\xFF")
            dr = self.spi.read(1, 0xFF)[0] & 0x1F
            if dr != 0x05:
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: data resp mult=%02x" % dr)
            if not self._wait_not_busy(self.timeout_ms):
                self._cs_high(); self.spi.write(self.dummy)
                raise OSError("SD: busy tras WRITE mult")
            off += self.sector_size

        # stop tran token
        self.spi.write(bytes([_TOKEN_STOP_TRAN]))
        if not self._wait_not_busy(self.timeout_ms):
            self._cs_high(); self.spi.write(self.dummy)
            raise OSError("SD: busy tras STOP mult")

        self._cs_high(); self.spi.write(self.dummy)
        return 0

    def ioctl(self, op, arg):
        if op == _IOCTL_INIT:
            return 0
        if op == _IOCTL_DEINIT:
            return 0
        if op == _IOCTL_SYNC:
            # Asegura que no esté busy
            self._cs_low()
            self._wait_not_busy()
            self._cs_high()
            return 0
        if op == _IOCTL_SEC_COUNT:
            # Si no lo logramos calcular, devuelve 0 y el FS puede ignorarlo.
            return 0 if self._sectors is None else int(self._sectors)
        if op == _IOCTL_SEC_SIZE:
            return self.sector_size
        return 0
