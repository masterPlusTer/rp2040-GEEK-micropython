# sd_helpers.py
# Utilidades para montar SD y obtener info en MicroPython (RP2040)

import os
from machine import Pin, SPI
import sdcard

# Pines típicos del RP2040-GEEK (SPI0). Cambia si tu placa usa otros.
SCK  = 18
MOSI = 19
MISO = 20
CS   = 21

def mount_sd(spi_id=0, sck=SCK, mosi=MOSI, miso=MISO, cs_pin=CS,
             init_baud=1_000_000, work_baud=10_000_000, mount_point="/sd"):
    """
    Monta la SD en /sd. Baja velocidad para init y sube luego.
    Devuelve (sd, mount_point). Lanza OSError en fallo.
    """
    spi = SPI(spi_id, baudrate=init_baud, polarity=0, phase=0,
              sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
    cs = Pin(cs_pin, Pin.OUT, value=1)

    sd = sdcard.SDCard(spi, cs, baudrate=init_baud)
    # Sube velocidad de trabajo
    try:
        sd.set_frequency(work_baud)
    except Exception:
        pass

    vfs = os.VfsFat(sd)
    # Si ya estaba montada, desmonta limpia
    try:
        os.mount(vfs, mount_point)
    except OSError:
        try:
            os.umount(mount_point)
        except Exception:
            pass
        os.mount(vfs, mount_point)
    return sd, mount_point

def bytes_to_mib(nbytes):
    return nbytes / (1024 * 1024)

def get_sd_info(mount_point="/sd", sd_obj=None):
    """
    Devuelve dict con: capacidad_total, espacio_libre, espacio_utilizado, archivos.
    Usa ioctl si sd_obj está, si no intenta statvfs.
    """
    total = None
    if sd_obj is not None:
        try:
            sec_size = sd_obj.ioctl(5, 0)      # SEC_SIZE
            sec_cnt  = sd_obj.ioctl(4, 0)      # SEC_COUNT
            if sec_size and sec_cnt:
                total = sec_size * sec_cnt
        except Exception:
            total = None

    # statvfs para libre y tamaño de bloque
    st = os.statvfs(mount_point)
    blksz = st[0]
    free  = st[3] * blksz
    if total is None:
        total = st[2] * blksz  # blocks totales si ioctl no dio

    used = max(0, total - free)

    # Lista de archivos nivel raíz
    try:
        lista = os.listdir(mount_point)
    except Exception:
        lista = []

    return {
        "capacidad_total_mb": bytes_to_mib(total),
        "espacio_libre_mb":   bytes_to_mib(free),
        "espacio_usado_mb":   bytes_to_mib(used),
        "archivos":           lista,
    }
