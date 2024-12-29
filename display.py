from machine import Pin, SPI, PWM  # Añadido PWM
import time

# Configuración de SPI y pines para RP2040
BL = 25  # Backlight
DC = 8   # Data/Command
CS = 9   # Chip Select
SCK = 10 # Clock
MOSI = 11 # Master Out Slave In
RST = 12 # Reset

# Configuración del Backlight
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(65535)  # Máxima intensidad del backlight

# Configuración de SPI
spi = SPI(1, baudrate=50000000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
cs = Pin(CS, Pin.OUT)
dc = Pin(DC, Pin.OUT)
rst = Pin(RST, Pin.OUT)

# Offset para coordenadas
OFFSET_X = 52  # Offset horizontal
OFFSET_Y = 40  # Offset vertical

def write_cmd(cmd):
    """Escribir un comando al controlador del display."""
    cs(1)
    dc(0)
    cs(0)
    spi.write(bytearray([cmd]))
    cs(1)

def write_data(data):
    """Escribir datos al controlador del display."""
    cs(1)
    dc(1)
    cs(0)
    spi.write(bytearray([data]))
    cs(1)

def init_display():
    """Inicializar el display."""
    rst(1)
    time.sleep(0.1)
    rst(0)
    time.sleep(0.1)
    rst(1)
    time.sleep(0.1)

    write_cmd(0x36)  # Configuración de memoria
    write_data(0x70)

    write_cmd(0x3A)  # Formato de píxel: RGB565
    write_data(0x05)

    write_cmd(0xB2)
    write_data(0x0C)
    write_data(0x0C)
    write_data(0x00)
    write_data(0x33)
    write_data(0x33)

    write_cmd(0xB7)  # Frame Rate Control
    write_data(0x35)

    write_cmd(0xBB)
    write_data(0x19)

    write_cmd(0xC0)
    write_data(0x2C)

    write_cmd(0xC2)
    write_data(0x01)

    write_cmd(0xC3)
    write_data(0x12)

    write_cmd(0xC4)
    write_data(0x20)

    write_cmd(0xC6)
    write_data(0x0F)

    write_cmd(0xD0)
    write_data(0xA4)
    write_data(0xA1)

    write_cmd(0xE0)  # Positive Voltage Gamma Control
    for value in [0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23]:
        write_data(value)

    write_cmd(0xE1)  # Negative Voltage Gamma Control
    for value in [0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23]:
        write_data(value)

    write_cmd(0x21)  # Display Inversion On
    write_cmd(0x11)  # Sleep Out
    time.sleep(0.1)
    write_cmd(0x29)  # Display On

def set_rotation(rotation):
    """
    Configura la orientación del display.
    :param rotation: 0, 1, 2, o 3 (0: normal, 1: 90°, 2: 180°, 3: 270°)
    """
    madctl_values = [0x00, 0x60, 0xC0, 0xA0]
    if rotation < 0 or rotation > 3:
        raise ValueError("La rotación debe ser 0, 1, 2 o 3")
    
    write_cmd(0x36)  # Comando MADCTL
    write_data(madctl_values[rotation])

    global WIDTH, HEIGHT, OFFSET_X, OFFSET_Y
    if rotation % 2 == 0:
        WIDTH, HEIGHT = 240, 320
        OFFSET_X, OFFSET_Y = 52, 40
    else:
        WIDTH, HEIGHT = 320, 240
        OFFSET_X, OFFSET_Y = 40, 52
      
def set_active_window(x0, y0, x1, y1):
    """Configura la ventana activa del display."""
    x0 += OFFSET_X
    x1 += OFFSET_X
    y0 += OFFSET_Y
    y1 += OFFSET_Y
    write_cmd(0x2A)  # Configurar columnas
    write_data(x0 >> 8)
    write_data(x0 & 0xFF)
    write_data(x1 >> 8)
    write_data(x1 & 0xFF)

    write_cmd(0x2B)  # Configurar filas
    write_data(y0 >> 8)
    write_data(y0 & 0xFF)
    write_data(y1 >> 8)
    write_data(y1 & 0xFF)

def fill_screen(color):
    """Llena toda la pantalla con un color utilizando un buffer por líneas."""
    write_cmd(0x2A)  # Rango de columnas
    write_data(0x00)
    write_data(0x28)
    write_data(0x01)
    write_data(0x17)

    write_cmd(0x2B)  # Rango de filas
    write_data(0x00)
    write_data(0x35)
    write_data(0x00)
    write_data(0xBB)

    write_cmd(0x2C)  # Escribir en memoria

    cs(1)
    dc(1)
    cs(0)

    # Crear un buffer para una sola línea (240 píxeles)
    high_byte = color >> 8
    low_byte = color & 0xFF
    line_buffer = bytearray([high_byte, low_byte] * 240)

    # Enviar el buffer línea por línea
    for _ in range(135):  # Altura de la pantalla
        spi.write(line_buffer)
    
    cs(1)
def set_window_and_write(x_start, y_start, x_end, y_end, data):
    """
    Configura la ventana activa en el display y escribe un bloque de datos.
    :param x_start: Coordenada inicial en X.
    :param y_start: Coordenada inicial en Y.
    :param x_end: Coordenada final en X.
    :param y_end: Coordenada final en Y.
    :param data: Datos en formato RGB565 a escribir en la ventana activa.
    """
    set_active_window(x_start, y_start, x_end, y_end)
    write_cmd(0x2C)  # Comando para iniciar escritura en memoria
    cs.value(0)
    dc.value(1)
    spi.write(data)
    cs.value(1)

