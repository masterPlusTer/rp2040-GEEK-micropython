# RP2040-GEEK MicroPython / SD Explorer

A self-contained screen + microSD file manager for the Waveshare RP2040-GEEK.
**No third-party libraries**: includes its own ST7789 screen and SPI SD drivers.

## Important hardware facts

- Onboard LCD is 240 x 135; screen is an **output** device, not touch-sensitive.
- The only onboard button is **BOOT** (connected to QSPI boot selection), not a standard menu/navigation input. There is no built-in up/down/select keypad. Thus, **menu commands are typed in Thonny REPL**, with results and previews shown on the LCD.
- SD SPI0: SCK **GP18**, MOSI **GP19**, MISO **GP20**, CS **GP23**. This fixes an incorrect GP21 setting in the previous package. See [Waveshare RP2040-GEEK](https://www.waveshare.com/wiki/RP2040-GEEK) and [Zephyr pinout](https://docs.zephyrproject.org/latest/boards/waveshare/rp2040_geek/doc/index.html).
- The display is only refreshed after a command; no continuous redraw loop.

## Install in Thonny

1. Copy the contents of `lib/` to **`/lib/` on the board** (replace previous copies).
2. Copy `geek_app.py` and `main.py` to the **board's root** (`/`).
3. Soft reset, open Thonny Shell; `main.py` launches automatically. If you want to run manually, rename `main.py` and type `import geek_app; geek_app.run()`.
4. Type `mount`, then `ls`, `open 0`, `cd 0`, etc. in the **Thonny Shell**, not the editor.
5. The SD must already be formatted FAT. No command formats it.

If your display shows strange colors or an incorrectly offset image, run `colors` and report the actual red/green/blue appearance. Rotation offsets have not been tested on your hardware; do not assume this software is validated on the physical board.

## Main commands

```text
help                list commands
mount               mount SD at /sd
umount              safely unmount SD
ls                  list current directory (all entries in REPL)
next / prev         page entries shown on LCD
cd folder           change into folder; cd .. goes up
open name           text preview, hex preview, or 24-bit BMP display
info                memory + SD capacity
mkdir directory     create directory
touch filename      create an empty file without overwriting
copy old | new      copy a file (no overwrite)
rename old | new    rename a file (no overwrite)
rm filename         remove file after typing YES
rmdir dirname       remove empty folder after typing YES
test                write 1024 bytes, read back, delete temporary file
brightness 50       change LCD brightness (0..100)
colors              RGB test (3 seconds)
gc                  collect garbage and report free heap
quit                exit application
```

All file commands are confined to `/sd`. Deletions require confirmation. Files with spaces are accepted; use ` | ` to separate source/destination in `copy` and `rename`. Files larger than the text preview limit are not loaded into RAM at once.

### What you cannot do yet

- Navigate with BOOT alone reliably; it is the QSPI flash boot-select pin, not a regular safe GPIO input.
- Play audio without extra hardware, use Wi-Fi/Bluetooth or touch interactions.
- Display PNG/JPEG; the bundled image reader supports uncompressed 24-bit BMP only.
- Confirm the display initialization or SD hardware works until you run it on the board.

## Repo layout

```text
main.py                 launch app at power-on
geek_app.py             interactive file manager (Thonny controls)
lib/display.py          ST7789 controller
lib/draw.py             primitives
lib/write.py           bitmap fonts rendering
lib/image.py           24-bit BMP reader
lib/sdcard.py          bundled SPI SD driver
lib/sd_helpers.py      SD mount/info, CS=GP23
lib/font_*.py          bundled fonts
examples/              stand-alone examples
assets/                test BMP image
```

---

## Original graphics library documentation

# RP2040-GEEK · MicroPython 🛠️

A small, self-contained graphics and microSD toolkit for the **Waveshare RP2040-GEEK** and its **240 × 135 ST7789 LCD**.

It started as a collection of experiments. Now at least the files are in the right places. Progress! 😅

## What it can do

- ST7789 LCD over SPI, 16-bit **RGB565** color.
- Pixels, lines, rectangles, circles and filled polygons.
- Text using four **bundled** bitmap fonts: 8, 10, 12 and 20 pixels.
- Stream **24-bit uncompressed BMP** images without a full framebuffer.
- Read and write a FAT-formatted microSD card using the **included** `sdcard.py` driver.
- Show a simple SD information screen.

**No `mip`, `pip`, internet access, external display drivers, or third-party modules required.** You **do need MicroPython firmware** installed on the board; `machine`, `os`, `struct` and other built-in modules come from MicroPython itself. The SD driver is shipped in this repo.

## Repository layout

```text
rp2040-GEEK-micropython/
├── main.py                 # safe boot demo; NO SD writes
├── lib/                    # modules imported automatically by MicroPython
│   ├── display.py          # ST7789 low-level driver and fast rectangles
│   ├── draw.py             # graphics primitives
│   ├── write.py            # bitmap text
│   ├── image.py            # 24-bit BMP reader
│   ├── interfaceUI.py      # SD information screen
│   ├── sd_helpers.py       # mount and inspect SD
│   ├── sdcard.py           # bundled SPI SD driver
│   └── font_*.py           # four bundled fonts
├── examples/               # copy ONE to board root to run it
│   ├── graphics_demo.py
│   ├── sd_info.py
│   ├── create_file_on_sd.py
│   └── bmp_demo.py
├── assets/RP2040-GEEK.bmp
├── tests/static_checks.py
└── LICENSE
```

## Install with Thonny

1. Install the official **MicroPython RP2040 firmware** on your board, and connect with Thonny.
2. On the **board** (not just on your PC), create `/lib`.
3. Copy **all contents of this repository's `lib/`** into the board's `/lib/` directory. Keep the file names.
4. Copy `main.py` into the board's `/` directory (optional). It runs automatically at boot.
5. To run an example, copy its `.py` file to the board root and run it from Thonny. Copy the BMP from `assets/` separately for `bmp_demo.py`.

Expected board layout:

```text
/
├── main.py
├── lib/
│   ├── display.py
│   ├── draw.py
│   ├── write.py
│   ├── image.py
│   ├── sdcard.py
│   ├── sd_helpers.py
│   └── ...
└── RP2040-GEEK.bmp       # only if using the BMP demo
```

Standard imports continue to work; no need to write `from lib import display`:

```python
import sys
print(sys.path)             # normally includes '/lib'
import display, draw, write
print(display.__file__)
```

**Avoid duplicate modules** at `/display.py` and `/lib/display.py`, because the root copy may win. Reboot after moving modules.

## Hardware pinout used by this project

| Device | Signal | GPIO |
|---|---|---:|
| LCD ST7789 | Backlight PWM | 25 |
| LCD ST7789 | DC | 8 |
| LCD ST7789 | CS | 9 |
| LCD ST7789 | SCK / SPI1 | 10 |
| LCD ST7789 | MOSI / SPI1 | 11 |
| LCD ST7789 | RST | 12 |
| microSD | SCK / SPI0 | 18 |
| microSD | MOSI / SPI0 | 19 |
| microSD | MISO / SPI0 | 20 |
| microSD | CS | 23 |

The SD CS pin has been corrected to **GP23** according to the Waveshare schematic; test on the device.

## Graphics quick start

```python
import display, draw, write
display.init_display()
display.set_rotation(1)      # 240x135 landscape, original configuration
display.fill_screen(0x0000)  # black (RGB565)
draw.rectangle(10, 10, 90, 50, 0x07E0, filled=True)
draw.circle(140, 70, 20, 0xF800, filled=True)
write.text(10, 80, 'Hello RP2040', 0xFFFF, 0x0000, size=8)
```

### Public API

- `display.init_display()` initializes the LCD.
- `display.set_rotation(0..3)` changes orientation; **rotation 1 is the preserved original hardware configuration**.
- `display.WIDTH`, `display.HEIGHT`, `display.get_rotation()` expose current state.
- `display.fill_screen(rgb565)` and `display.fill_rect(x0,y0,x1,y1,rgb565)` write color blocks efficiently.
- `display.brightness(0..65535)` adjusts the backlight PWM.
- `draw.pixel(x,y,c)`, `draw.line(x1,y1,x0,y0,c)`, `draw.rectangle(x0,y0,x1,y1,c,filled=False)`, `draw.circle(x,y,r,c,filled=False)`.
- `draw.polygon(color, filled, (x,y), ...)` draws a polygon.
- `write.text(x,y,string,fg,bg,size=8)` and `write.draw_char(...)` support 8/10/12/20 px fonts.
- `image.show_bmp(path,x_offset=0,y_offset=0,mirror=False,flip_vertical=False)` streams an uncompressed **24-bit BMP**.

Coordinate order for `draw.line` is **retained from the original project** for compatibility. Dimensions and clipping use the current display orientation.

### Colors

All graphics use 16-bit **RGB565**, not 24-bit RGB888:

```python
BLACK=0x0000; WHITE=0xFFFF
RED=0xF800; GREEN=0x07E0; BLUE=0x001F
YELLOW=0xFFE0; CYAN=0x07FF
```

## SD card

The bundled `sdcard.py` is imported by `sd_helpers.py`. A **FAT16/FAT32** formatted card is normally appropriate; this repository does not format or partition cards.

```python
from sd_helpers import mount_sd, get_sd_info
sd, mountpoint = mount_sd()  # mounts at /sd; may raise OSError
print(get_sd_info(mountpoint, sd))
with open('/sd/test.txt', 'w') as f:
    f.write('Hello from RP2040-GEEK\n')
```

`examples/create_file_on_sd.py` **writes** a new file when explicitly run. Neither `main.py` nor the graphics demo mounts or writes to the SD automatically. To remount an already-mounted SD, unmount it deliberately or soft-reset the board; the helper won't silently unmount your filesystem on errors.

## What changed from the original version?

- Drivers, helpers, fonts and UI moved into `/lib`; executable examples moved into `/examples`.
- SPI commands use shared buffers instead of repeated one-byte allocations.
- Filled rectangles and screen clears use fixed-size SPI blocks and clip offscreen coordinates.
- Horizontal and vertical lines use block operations; filled polygons fix a broken edge-coordinate assignment.
- Text loads font modules **on demand** rather than importing all four at startup.
- BMP loader no longer forces garbage collection every eight lines.
- SD mount errors no longer trigger indiscriminate unmount/remount.
- Boot demo is safe and has **no automatic SD file writes**.

## Limits and testing

- **Static checks pass on desktop CPython**, but this version has **not been tested on physical RP2040-GEEK hardware**. Pin assignment and LCD color/offset behavior require a board test.
- Original 240 × 135 landscape is the reference (`rotation=1`, MADCTL `0x70`, offsets `52,40`). The other rotations are best-effort candidates requiring visual calibration.
- Direct-to-screen rendering means **no framebuffer** and low RAM consumption, but many isolated pixels are still slower than large SPI blocks.
- Font bitmap data belongs to this repository; no external font packages needed.
- If you need maximum speed for animated scenes, benchmark before increasing SPI clock: the default is conservatively set to 40 MHz.

## Troubleshooting

- **`ImportError`**: check `sys.path`, `/lib/`, duplicate root files, and reboot after copying.
- **Blank LCD**: check firmware, pins, reset, orientation and display initialization; try `display.fill_screen(0xF800)`.
- **Wrong colors**: check panel MADCTL/RGB order for the board revision rather than swapping RGB565 bytes blindly.
- **SD error**: confirm card insertion, FAT formatting, wiring and available power before changing SPI speed.
- **`OSError` when remounting**: the SD is probably still mounted. Unmount explicitly before mounting again.

## License

See [LICENSE](LICENSE). Improvements are based on the repository's original code.

Hardware isn't obliged to cooperate, but at least the source tree can. 🔧
