# RP2040 & RP2350 GEEK - MicroPython

### One codebase. Two microcontrollers. Plenty of room to experiment. 🚀

A beginner-friendly MicroPython project for the **Waveshare RP2040-GEEK** and **RP2350-GEEK**.

This project started as a collection of experiments with an LCD display, some graphics functions and a microSD card. Eventually, it became a small, self-contained application that runs on both devices.
<img width="1080" height="1440" alt="rp2040-rp2350-geek" src="https://github.com/user-attachments/assets/16c03392-908e-4cfe-8ae9-754a44c32ea6" />
<img width="1080" height="1440" alt="geek-startup-bmp" src="https://github.com/user-attachments/assets/f47ad1fc-b20a-46b7-b09b-e46dfd28010b" />
<img width="1080" height="1440" alt="geek-sd-browser" src="https://github.com/user-attachments/assets/2b86e3d5-bcb5-49e7-8de9-06dcc9723522" />

The idea is simple: **give beginners a working starting point instead of making them figure out every hardware detail from scratch.**

You can use it as a file explorer, experiment with the display, learn how SPI works, modify the code or build something entirely different.

No third-party MicroPython libraries are required. The necessary drivers are included in this repository.

---

## ✅ Tested on both devices

The same application has been successfully tested on:

- **Waveshare RP2040-GEEK**
- **Waveshare RP2350-GEEK**

On both boards, the application successfully:

- Starts the LCD
- Displays the startup BMP image
- Mounts the microSD card
- Lists the files on the card
- Opens the interactive command interface in Thonny

**Important:** Each board requires the appropriate MicroPython firmware. The firmware is different, but the application code is shared.

This is a tested starting point, not a guarantee that every possible peripheral, firmware version or future hardware revision will behave identically.

## 🧠 What's the difference between the boards?

The boards use different Raspberry Pi microcontrollers.

| Feature | RP2040-GEEK | RP2350-GEEK |
|---|---|---|
| Microcontroller | RP2040 | RP2350 |
| Generation | Earlier | Newer |
| Architecture | Dual-core Arm Cortex-M0+ | Dual-core Arm Cortex-M33 or Hazard3 RISC-V architecture |
| Flash on the tested GEEK models | 4 MB | 16 MB |
| MicroPython firmware | RP2040 build | RP2350 build |
| Application in this repository | Same code | Same code |

The RP2350 provides more advanced hardware capabilities, but this project intentionally uses features common to both devices.

The different flash capacities also mean that available storage and room for additional applications may differ.

You are free to extend the code according to the capabilities and limitations of your own board.

## 📦 What's included?

- ST7789 LCD driver
- Basic graphics functions
- Text rendering and bitmap fonts
- BMP image display
- microSD card driver
- microSD file explorer
- File creation, copying, renaming and deletion
- Text and hexadecimal file previews
- CPU and free-memory information
- Display color and brightness tests

The interface uses the LCD for displaying information and the **Thonny REPL** for entering commands.

Neither device has a dedicated navigation keypad suitable for a conventional file manager, so this approach keeps the project simple without requiring additional hardware.

## 📁 Project structure

```text
/
├── main.py
├── geek_app.py
├── lib/
│   ├── display.py
│   ├── draw.py
│   ├── write.py
│   ├── image.py
│   ├── interfaceUI.py
│   ├── sdcard.py
│   ├── sd_helpers.py
│   ├── font_small.py
│   ├── font_medium.py
│   ├── font_large.py
│   └── font_xlarge.py
└── assets/
    └── RP2040-GEEK.bmp
```

The repository may also include examples, tests and documentation files. Only copy the files you need onto the device.

## 🚀 Getting started

### Step 1: Install MicroPython

Install the correct MicroPython firmware for your board.

Useful resources:

- [MicroPython downloads](https://micropython.org/download/)
- [Waveshare Wiki](https://www.waveshare.com/wiki/Main_Page)
- [Thonny IDE](https://thonny.org/)

Make sure you select the firmware appropriate for your RP2040 or RP2350 device.

Do not assume that the same UF2 firmware file works on both boards.

### Step 2: Copy the files

Connect your GEEK device to your computer and open Thonny.

Copy the following to the board's internal filesystem:

1. `main.py`
2. `geek_app.py`
3. The entire `lib` directory
4. The `assets` directory containing the startup BMP

**Keep the `/lib` folder structure intact.**

MicroPython normally searches `/lib` for modules, so your application can import them without needing their full paths.

### Step 3: Insert a microSD card

Insert a compatible, FAT-formatted microSD card.

For the initial test, use a card containing files you do not mind experimenting with. Some available commands create or delete files.

### Step 4: Start the application

Restart the board or run `main.py` in Thonny.

You should see something similar to:

```text
RP2040-GEEK starting...
BMP displayed: /assets/RP2040-GEEK.bmp
Initializing SD card...
SD mounted at /sd
SD ready.

Directory: /sd (...)
...
GEEK>
```

The startup banner may still say RP2040-GEEK. This is only an application label and can be changed; it does not indicate a board compatibility problem.

The SD card mounts automatically when available.

If mounting fails, the application can still start and you can retry using `mount`.

## 💻 Using the SD Explorer

Commands are typed into the Thonny console at the `GEEK>` prompt.

### Navigation

| Command | Description |
|---|---|
| `ls` or `list` | List files and directories |
| `cd folder` | Enter a directory |
| `cd ..` | Go to the parent directory |
| `next` | Next page |
| `prev` | Previous page |
| `open 0` | Open the file at index 0 |
| `open filename.txt` | Open a file by name |
| `home` | Display the home screen |

### File management

| Command | Description |
|---|---|
| `mkdir folder` | Create a directory |
| `touch file.txt` | Create an empty file |
| `copy old.txt \| new.txt` | Copy a file |
| `rename old.txt \| new.txt` | Rename a file |
| `rm file.txt` | Delete a file with confirmation |
| `rmdir folder` | Remove an empty directory |

These file-management commands operate inside `/sd`.

Existing destinations are protected against accidental overwrites.

Be careful with deletion commands, and keep backups of important files.

### Hardware and system tools

| Command | Description |
|---|---|
| `info` | Display SD, CPU and memory information |
| `test` | Test SD write, read and delete operations |
| `colors` | Display red, green and blue test screens |
| `brightness 50` | Set LCD brightness to 50% |
| `gc` | Collect garbage and display free memory |
| `logo` | Display the startup BMP from internal flash |
| `mount` | Mount the SD card |
| `umount` | Unmount the SD card |
| `help` | Show available commands |
| `quit` | Exit the interactive application |

The SD test creates a temporary file, reads it back and deletes it.

## 🎨 Working with the LCD

You can use the display driver independently of the file explorer.

Example:

```python
import display

display.init_display()
display.set_rotation(1)

display.fill_screen(0x0000)
display.fill_rect(10, 10, 100, 50, 0x07E0)
```

Colors use **RGB565**:

```python
RED   = 0xF800
GREEN = 0x07E0
BLUE  = 0x001F
WHITE = 0xFFFF
BLACK = 0x0000
```

The working application uses the display in its **240 × 135 landscape orientation**.

Other rotations may require additional offset calibration for your particular LCD module.

## 🖼️ Displaying BMP images

The repository includes a BMP viewer.

The startup image is stored at:

```text
/assets/RP2040-GEEK.bmp
```

You can display it from the application by typing:

```text
GEEK> logo
```

The image viewer supports the uncompressed 24-bit BMP format used by this project.

You can also open compatible BMP files from the microSD card:

```text
GEEK> open picture.bmp
```

## 🔧 No external libraries

This project is intentionally self-contained.

It uses modules provided by MicroPython, such as:

- `machine`
- `os`
- `sys`
- `time`
- `gc`

Hardware drivers and graphics utilities are provided in `/lib`.

You do not need to install a separate ST7789 package or SD-card driver.

You do, however, need an appropriate MicroPython firmware build with support for the hardware interfaces used by the board.

## 🛠️ Troubleshooting

**The SD card does not mount**

Check that the card is inserted, formatted with a supported FAT filesystem and working correctly.

Try the `mount` command and inspect the error in Thonny.

**The screen has strange colors**

Use the `colors` command to check RGB565 output.

The ST7789's color order is controlled partly by its initialization registers.

**The image is shifted or has strange pixels around the edges**

Check the display offsets in `lib/display.py`. The working landscape configuration for the tested hardware uses offsets X=40 and Y=53.

**A module cannot be imported**

Make sure the `/lib` directory exists on the device and contains the required `.py` files.

You can inspect the module search paths with:

```python
import sys
print(sys.path)
```

**The application starts automatically**

That's expected. MicroPython runs `main.py` during startup.

To stop automatic launching, rename or remove `main.py`. The library files can remain installed.

## 🧪 A starting point, not a finished product

This repository is deliberately simple.

It is intended to help people who are learning MicroPython, SPI, LCD displays, SD storage or embedded programming.

The RP2040 and RP2350 offer capabilities beyond those currently used here.

You can add animations, sensors, graphics experiments, data loggers, file tools or entirely new applications.

You can also take advantage of each microcontroller's specific features when you need them.

The fact that the same initial program runs on both boards does not mean every hardware feature is interchangeable.

It simply means that we have a useful common foundation.

## ❤️ Final note

I'm not trying to provide a giant framework or a perfect operating system.

I wanted a small collection of tools that work, are easy to understand and can be modified without fighting a mountain of dependencies.

It started with some experiments. Now the same code runs on two different GEEK boards.

That's a pretty nice result.

**Have fun, break things (preferably in software), fix them and make something of your own.**
