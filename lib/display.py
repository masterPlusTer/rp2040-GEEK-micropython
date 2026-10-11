
"""
RP2040-GEEK - ST7789 Display Driver
Resolution: 240 x 135
MicroPython - No external libraries

SPI1:
    BL   = GP25
    DC   = GP8
    CS   = GP9
    SCK  = GP10
    MOSI = GP11
    RST  = GP12

Public API:
    init_display()
    set_rotation(rotation)
    get_rotation()
    set_active_window(x0, y0, x1, y1)
    fill_screen(color)
    fill_rect(x0, y0, x1, y1, color)
    set_window_and_write(x0, y0, x1, y1, data)
    pixel(x, y, color)
    brightness(value)

Color format: RGB565
"""

from machine import Pin, SPI, PWM
import time


# --------------------------------------------------
# HARDWARE CONFIGURATION
# --------------------------------------------------

BL = 25
DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

spi = SPI(
    1,
    baudrate=40_000_000,
    polarity=0,
    phase=0,
    sck=Pin(SCK),
    mosi=Pin(MOSI)
)

cs = Pin(CS, Pin.OUT, value=1)
dc = Pin(DC, Pin.OUT, value=1)
rst = Pin(RST, Pin.OUT, value=1)

pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(65535)


# --------------------------------------------------
# DISPLAY GEOMETRY
# --------------------------------------------------

_current_rotation = 1

WIDTH = 240
HEIGHT = 135

# Corrected landscape offsets.
OFFSET_X = 40
OFFSET_Y = 53

# Rotation 1 is the intended orientation.
# Other rotation offsets are provisional and
# must be checked on the real LCD.

_ROTATIONS = (
    # width, height, x_offset, y_offset, MADCTL

    (135, 240, 53, 40, 0x00),
    (240, 135, 40, 53, 0x70),
    (135, 240, 53, 40, 0xC0),
    (240, 135, 40, 53, 0xB0),
)


# --------------------------------------------------
# REUSABLE BUFFERS
# --------------------------------------------------

_ONE = bytearray(1)
_FOUR = bytearray(4)
_PIXEL = bytearray(2)

# 256 pixels in RGB565.
_BLOCK = bytearray(512)


# --------------------------------------------------
# LOW LEVEL SPI
# --------------------------------------------------

def write_cmd(cmd):
    _ONE[0] = cmd & 0xFF

    cs(0)
    dc(0)

    spi.write(_ONE)

    cs(1)


def write_data(data):
    if isinstance(data, int):
        _ONE[0] = data & 0xFF
        data = _ONE

    cs(0)
    dc(1)

    spi.write(data)

    cs(1)


def _command_data(cmd, payload):
    write_cmd(cmd)
    write_data(payload)


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

def init_display():
    # Hardware reset.
    rst(1)
    time.sleep_ms(100)

    rst(0)
    time.sleep_ms(100)

    rst(1)
    time.sleep_ms(100)

    # RGB565, 16 bits per pixel.
    _command_data(0x3A, b'\x05')

    # Porch setting.
    _command_data(
        0xB2,
        bytes((0x0C, 0x0C, 0x00, 0x33, 0x33))
    )

    # Gate control.
    _command_data(0xB7, b'\x35')

    # VCOM.
    _command_data(0xBB, b'\x19')

    # LCM control.
    _command_data(0xC0, b'\x2C')

    # VDV and VRH.
    _command_data(0xC2, b'\x01')
    _command_data(0xC3, b'\x12')
    _command_data(0xC4, b'\x20')

    # Frame rate.
    _command_data(0xC6, b'\x0F')

    # Power control.
    _command_data(0xD0, b'\xA4\xA1')

    # Positive gamma.
    _command_data(
        0xE0,
        bytes((
            0xD0, 0x04, 0x0D, 0x11,
            0x13, 0x2B, 0x3F, 0x54,
            0x4C, 0x18, 0x0D, 0x0B,
            0x1F, 0x23
        ))
    )

    # Negative gamma.
    _command_data(
        0xE1,
        bytes((
            0xD0, 0x04, 0x0C, 0x11,
            0x13, 0x2C, 0x3F, 0x44,
            0x51, 0x2F, 0x1F, 0x1F,
            0x20, 0x23
        ))
    )

    # Display inversion ON.
    write_cmd(0x21)

    # Apply selected orientation.
    set_rotation(_current_rotation)

    # Sleep out.
    write_cmd(0x11)
    time.sleep_ms(120)

    # Display ON.
    write_cmd(0x29)


# --------------------------------------------------
# ROTATION
# --------------------------------------------------

def set_rotation(rotation):
    global WIDTH
    global HEIGHT
    global OFFSET_X
    global OFFSET_Y
    global _current_rotation

    if rotation not in (0, 1, 2, 3):
        raise ValueError(
            "rotation must be 0, 1, 2 or 3"
        )

    (
        WIDTH,
        HEIGHT,
        OFFSET_X,
        OFFSET_Y,
        madctl
    ) = _ROTATIONS[rotation]

    _current_rotation = rotation

    _command_data(
        0x36,
        bytes((madctl,))
    )


def get_rotation():
    return _current_rotation


# --------------------------------------------------
# ACTIVE WINDOW
# --------------------------------------------------

def set_active_window(x0, y0, x1, y1):
    """
    Configure ST7789 address window.

    Coordinates are logical screen coordinates.
    This low-level function does not clip.
    """

    x0 += OFFSET_X
    x1 += OFFSET_X
    y0 += OFFSET_Y
    y1 += OFFSET_Y

    # Column address set.
    _FOUR[0] = (x0 >> 8) & 0xFF
    _FOUR[1] = x0 & 0xFF
    _FOUR[2] = (x1 >> 8) & 0xFF
    _FOUR[3] = x1 & 0xFF

    _command_data(0x2A, _FOUR)

    # Row address set.
    _FOUR[0] = (y0 >> 8) & 0xFF
    _FOUR[1] = y0 & 0xFF
    _FOUR[2] = (y1 >> 8) & 0xFF
    _FOUR[3] = y1 & 0xFF

    _command_data(0x2B, _FOUR)


# --------------------------------------------------
# CLIPPING
# --------------------------------------------------

def _clip_rect(x0, y0, x1, y1):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    if x0 > x1:
        x0, x1 = x1, x0

    if y0 > y1:
        y0, y1 = y1, y0

    if (
        x1 < 0 or
        y1 < 0 or
        x0 >= WIDTH or
        y0 >= HEIGHT
    ):
        return None

    return (
        max(0, x0),
        max(0, y0),
        min(WIDTH - 1, x1),
        min(HEIGHT - 1, y1)
    )


# --------------------------------------------------
# FILLED RECTANGLES
# --------------------------------------------------

def fill_rect(x0, y0, x1, y1, color):
    rect = _clip_rect(x0, y0, x1, y1)

    if rect is None:
        return

    x0, y0, x1, y1 = rect

    pixels = (x1 - x0 + 1) * (y1 - y0 + 1)

    high = (color >> 8) & 0xFF
    low = color & 0xFF

    # Fill reusable block.
    for i in range(0, len(_BLOCK), 2):
        _BLOCK[i] = high
        _BLOCK[i + 1] = low

    set_active_window(x0, y0, x1, y1)
    write_cmd(0x2C)

    cs(0)
    dc(1)

    try:
        while pixels >= 256:
            spi.write(_BLOCK)
            pixels -= 256

        if pixels:
            spi.write(
                memoryview(_BLOCK)[:pixels * 2]
            )

    finally:
        cs(1)


# --------------------------------------------------
# FILL SCREEN
# --------------------------------------------------

def fill_screen(color):
    fill_rect(
        0,
        0,
        WIDTH - 1,
        HEIGHT - 1,
        color
    )


# --------------------------------------------------
# RGB565 BLOCK WRITING
# --------------------------------------------------

def set_window_and_write(x0, y0, x1, y1, data):
    """
    Write an RGB565 image block.

    Pixel bytes must be big-endian RGB565.
    Coordinates are inclusive.

    Off-screen portions are clipped.
    """

    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    if x1 < x0 or y1 < y0:
        raise ValueError(
            "window end before start"
        )

    width = x1 - x0 + 1
    height = y1 - y0 + 1

    expected = width * height * 2

    if len(data) != expected:
        raise ValueError(
            "RGB565 data size does not match window"
        )

    rect = _clip_rect(x0, y0, x1, y1)

    if rect is None:
        return

    ax, ay, bx, by = rect

    view = memoryview(data)

    # Entire source rectangle visible.
    if (ax, ay, bx, by) == (x0, y0, x1, y1):
        set_active_window(x0, y0, x1, y1)
        write_cmd(0x2C)
        write_data(view)
        return

    # Partially visible rectangle.
    # Preserve original row stride.
    for row in range(ay, by + 1):

        start = (
            (row - y0) * width +
            (ax - x0)
        ) * 2

        end = start + (bx - ax + 1) * 2

        set_active_window(ax, row, bx, row)
        write_cmd(0x2C)

        write_data(view[start:end])


# --------------------------------------------------
# SINGLE PIXEL
# --------------------------------------------------

def pixel(x, y, color):
    x = int(x)
    y = int(y)

    if not (
        0 <= x < WIDTH and
        0 <= y < HEIGHT
    ):
        return

    _PIXEL[0] = (color >> 8) & 0xFF
    _PIXEL[1] = color & 0xFF

    set_active_window(x, y, x, y)
    write_cmd(0x2C)
    write_data(_PIXEL)


# --------------------------------------------------
# BACKLIGHT
# --------------------------------------------------

def brightness(value):
    """
    Backlight brightness: 0..65535.

    0     = off
    65535 = full brightness
    """

    value = max(
        0,
        min(65535, int(value))
    )

    pwm.duty_u16(value)
