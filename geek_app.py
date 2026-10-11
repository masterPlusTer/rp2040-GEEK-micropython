
"""
RP2040-GEEK - SD Explorer
MicroPython - No third-party libraries.

LCD: ST7789 240x135
SD: SPI0, CS GP23

Commands are entered through Thonny REPL.
"""

import os
import gc
import sys
import time

import display
import write
import sd_helpers


# -------------------------------------------
# CONFIGURATION
# -------------------------------------------

LOGO_PATH = "/assets/RP2040-GEEK.bmp"

BLACK = 0x0000
WHITE = 0xFFFF
CYAN = 0x07FF
GREEN = 0x07E0
RED = 0xF800
YELLOW = 0xFFE0
GREY = 0x8410
NAVY = 0x1082


# -------------------------------------------
# APPLICATION
# -------------------------------------------

class GeekApp:

    def __init__(self):
        self.cwd = "/sd"
        self.mounted = False
        self.sd = None
        self.message = "Ready"
        self.selected = 0
        self.entries = []
        self.page = 0

    # ---------------------------------------
    # SCREEN
    # ---------------------------------------

    def line(self, y, txt, color=WHITE):
        txt = str(txt).replace("\n", " ")
        txt = txt.replace("\r", " ")

        write.text(
            4,
            y,
            txt[:29],
            color,
            BLACK,
            size=8
        )

    def screen(self, title, lines):
        display.fill_screen(BLACK)

        display.fill_rect(
            0, 0, 239, 16, NAVY
        )

        write.text(
            4,
            4,
            title[:28],
            CYAN,
            NAVY,
            size=8
        )

        for i, item in enumerate(lines[:9]):

            color = WHITE

            if isinstance(item, tuple):
                item, color = item

            self.line(
                19 + 12 * i,
                item,
                color
            )

    def status(self):
        self.screen(
            "RP2040 GEEK / HOME",
            [
                "SD: " + (
                    "MOUNTED"
                    if self.mounted
                    else "NOT MOUNTED"
                ),
                "Path: " + self.cwd[-22:],
                "MicroPython: "
                + str(sys.implementation.version[0])
                + "."
                + str(sys.implementation.version[1]),
                "Free heap: " + str(gc.mem_free()),
                "LCD 240x135 / SPI1",
                "SD SPI0 / CS GP23",
                ("Last: " + self.message)[-29:],
                "Enter commands in Thonny",
                "Type help for commands"
            ]
        )

    # ---------------------------------------
    # SD CARD
    # ---------------------------------------

    def mount(self):

        if self.mounted:
            return "SD already mounted"

        try:
            self.sd, _ = sd_helpers.mount_sd()

            self.mounted = True
            self.cwd = "/sd"

            return "SD mounted at /sd"

        except Exception as exc:

            self.sd = None
            self.mounted = False

            return "SD mount failed: " + str(exc)

    def unmount(self):

        if not self.mounted:
            return "SD not mounted"

        os.umount("/sd")

        self.mounted = False
        self.sd = None
        self.cwd = "/sd"
        self.entries = []

        return "SD unmounted"

    def require_sd(self):

        if not self.mounted:
            raise OSError(
                "SD is not mounted. Use: mount"
            )

    # ---------------------------------------
    # SAFE PATH HANDLING
    # ---------------------------------------

    def path(self, name="."):

        self.require_sd()

        if name.startswith("/sd"):
            parts = name.split("/")

        elif name.startswith("/"):
            raise ValueError(
                "Only /sd paths allowed"
            )

        else:
            parts = (
                self.cwd + "/" + name
            ).split("/")

        clean = []

        for item in parts:

            if item in ("", "."):
                continue

            if item == "..":

                if len(clean) > 1:
                    clean.pop()

                continue

            clean.append(item)

        if not clean or clean[0] != "sd":
            raise ValueError(
                "Path outside SD"
            )

        return "/" + "/".join(clean)

    # ---------------------------------------
    # DIRECTORY LISTING
    # ---------------------------------------

    def listing(self):

        self.require_sd()

        entries = []

        for name in os.listdir(self.cwd):

            full = self.path(name)
            st = os.stat(full)

            is_dir = bool(st[0] & 0x4000)

            entries.append(
                (name, is_dir, st[6])
            )

        entries.sort(
            key=lambda e: (
                not e[1],
                e[0].lower()
            )
        )

        self.entries = entries

        return entries

    def browser(self, page=None):

        if page is not None:
            self.page = max(0, page)

        entries = self.listing()

        pages = max(
            1,
            (len(entries) + 7) // 8
        )

        self.page = min(
            self.page,
            pages - 1
        )

        start = self.page * 8

        lines = [
            (
                "> " + self.cwd[-25:],
                YELLOW
            )
        ]

        for i, (name, is_dir, size) in enumerate(
            entries[start:start + 8]
        ):

            index = start + i

            prefix = (
                "[D]"
                if is_dir
                else "   "
            )

            label = "%d %s%s" % (
                index,
                prefix,
                name
            )

            lines.append(label[:29])

        self.screen(
            "SD BROWSER %d/%d" % (
                self.page + 1,
                pages
            ),
            lines
        )

        print()
        print(
            "Directory:",
            self.cwd,
            "(%d items)" % len(entries)
        )

        for i, (name, is_dir, size) in enumerate(entries):

            print(
                "%3d  %s  %-32s %d" % (
                    i,
                    "DIR " if is_dir else "FILE",
                    name,
                    size
                )
            )

        return "Listed %d items" % len(entries)

    # ---------------------------------------
    # FILE INDEX
    # ---------------------------------------

    def name_from_index(self, token):

        try:
            i = int(token)

            if (
                str(i) == token
                and 0 <= i < len(self.entries)
            ):
                return self.entries[i][0]

        except ValueError:
            pass

        return token

    # ---------------------------------------
    # FILE VIEWER
    # ---------------------------------------

    def view(self, name):

        full = self.path(
            self.name_from_index(name)
        )

        if os.stat(full)[0] & 0x4000:
            raise ValueError(
                "That is a directory"
            )

        # BMP IMAGE
        if full.lower().endswith(".bmp"):

            import image

            display.fill_screen(BLACK)
            image.show_bmp(full)

            return "BMP displayed: " + full

        # TEXT FILE
        if full.lower().endswith(
            (
                ".txt",
                ".py",
                ".md",
                ".csv",
                ".json",
                ".log",
                ".ini",
                ".cfg"
            )
        ):

            with open(full, "rb") as f:
                data = f.read(384)

            text = data.decode(
                "utf-8",
                "replace"
            )

            print()
            print("---", full, "---")
            print(text)

            self.screen(
                "TEXT PREVIEW",
                text.splitlines()[:9]
            )

            return "Text preview: " + full

        # HEX VIEWER
        with open(full, "rb") as f:
            data = f.read(96)

        print(
            "First 96 bytes:",
            repr(data)
        )

        lines = []

        for i in range(0, len(data), 8):

            hex_data = " ".join(
                "%02X" % b
                for b in data[i:i + 8]
            )

            lines.append(
                "%04X %s" % (
                    i,
                    hex_data
                )
            )

        self.screen(
            "HEX PREVIEW",
            lines
        )

        return "Binary preview: " + full

    # ---------------------------------------
    # LOGO / INTERNAL FLASH BMP
    # ---------------------------------------

    def logo(self, pause=0):

        import image

        try:
            os.stat(LOGO_PATH)

        except OSError:
            raise OSError(
                "Missing " + LOGO_PATH
            )

        display.fill_screen(BLACK)

        image.show_bmp(LOGO_PATH)

        if pause:
            time.sleep(pause)

        return "BMP displayed: " + LOGO_PATH

    # ---------------------------------------
    # SYSTEM INFORMATION
    # ---------------------------------------

    def info(self):

        self.require_sd()

        d = sd_helpers.get_sd_info(
            "/sd",
            self.sd
        )

        lines = [
            "SD card information",
            "Total: %.1f MiB"
            % d["capacidad_total_mb"],
            "Free: %.1f MiB"
            % d["espacio_libre_mb"],
            "Used: %.1f MiB"
            % d["espacio_usado_mb"],
            "Current: " + self.cwd[-20:],
            "CPU: %d MHz"
            % (machine_freq() // 1000000),
            "RAM free: %d" % gc.mem_free()
        ]

        self.screen(
            "SYSTEM / STORAGE",
            lines
        )

        for line in lines:
            print(line)

        return "Info updated"

    # ---------------------------------------
    # SD TEST
    # ---------------------------------------

    def self_test(self):

        self.require_sd()

        filename = self.path(
            "__geek_test.tmp"
        )

        if filename in [
            self.path(n)
            for n in os.listdir(self.cwd)
        ]:
            raise OSError(
                "Test file exists; refusing to overwrite"
            )

        original = bytes(
            (i * 13 + 7) & 255
            for i in range(1024)
        )

        try:

            with open(filename, "wb") as f:
                f.write(original)

            with open(filename, "rb") as f:
                readback = f.read()

            if readback != original:
                raise OSError(
                    "Readback mismatch"
                )

        finally:
            try:
                os.remove(filename)
            except OSError:
                pass

        self.screen(
            "SD TEST",
            [
                "Write 1024 bytes: OK",
                "Readback compare: OK",
                "Cleanup: OK"
            ]
        )

        return "SD write/read/delete test PASS"

    # ---------------------------------------
    # COMMAND PROCESSOR
    # ---------------------------------------

    def command(self, cmdline):

        cmdline = cmdline.strip()

        if not cmdline:
            return ""

        verb, _, arg = cmdline.partition(" ")

        verb = verb.lower()
        arg = arg.strip()

        try:

            if verb == "help":
                print(HELP)
                return "Help printed"

            if verb == "home":
                self.status()
                return "Home"

            if verb == "mount":
                return self.mount()

            if verb == "umount":
                return self.unmount()

            if verb in ("ls", "list"):
                return self.browser(0)

            if verb == "next":
                return self.browser(self.page + 1)

            if verb == "prev":
                return self.browser(self.page - 1)

            if verb == "cd":

                p = self.path(
                    self.name_from_index(
                        arg or ".."
                    )
                )

                if not (
                    os.stat(p)[0] & 0x4000
                ):
                    raise ValueError(
                        "Not a directory"
                    )

                self.cwd = p

                return self.browser(0)

            if verb in ("open", "cat"):

                if not arg:
                    raise ValueError(
                        "open requires filename or index"
                    )

                return self.view(arg)

            if verb in ("logo", "image", "bmp"):
                return self.logo()

            if verb == "info":
                return self.info()

            if verb == "test":
                return self.self_test()

            # CREATE DIRECTORY
            if verb == "mkdir":

                if not arg:
                    raise ValueError(
                        "mkdir requires directory name"
                    )

                p = self.path(arg)

                os.mkdir(p)

                return "Created " + p

            # CREATE EMPTY FILE
            if verb == "touch":

                if not arg:
                    raise ValueError(
                        "touch requires filename"
                    )

                p = self.path(arg)

                try:
                    os.stat(p)
                except OSError:
                    pass
                else:
                    raise OSError(
                        "File already exists"
                    )

                with open(p, "wb"):
                    pass

                return "Created " + p

            # DELETE FILE OR EMPTY DIRECTORY
            if verb in ("rm", "rmdir"):

                if not arg:
                    raise ValueError(
                        verb + " requires target"
                    )

                p = self.path(
                    self.name_from_index(arg)
                )

                if p == "/sd":
                    raise ValueError(
                        "Cannot delete SD root"
                    )

                response = input(
                    "DELETE "
                    + p
                    + " ? Type YES: "
                )

                if response != "YES":
                    return "Cancelled"

                if verb == "rm":
                    os.remove(p)
                else:
                    os.rmdir(p)

                return "Deleted " + p

            # RENAME
            if verb == "rename":

                a, sep, b = arg.partition("|")

                if not sep:
                    raise ValueError(
                        "rename old | new"
                    )

                old = self.path(
                    self.name_from_index(
                        a.strip()
                    )
                )

                new = self.path(b.strip())

                if old == "/sd" or new == "/sd":
                    raise ValueError(
                        "Cannot rename SD root"
                    )

                try:
                    os.stat(new)
                except OSError:
                    pass
                else:
                    raise ValueError(
                        "Destination already exists"
                    )

                os.rename(old, new)

                return "Renamed to " + new

            # COPY
            if verb == "copy":

                a, sep, b = arg.partition("|")

                if not sep:
                    raise ValueError(
                        "copy source | destination"
                    )

                old = self.path(
                    self.name_from_index(
                        a.strip()
                    )
                )

                new = self.path(b.strip())

                if old == "/sd" or new == "/sd":
                    raise ValueError(
                        "Cannot copy SD root"
                    )

                if os.stat(old)[0] & 0x4000:
                    raise ValueError(
                        "File copy only"
                    )

                try:
                    os.stat(new)
                except OSError:
                    pass
                else:
                    raise ValueError(
                        "Destination already exists"
                    )

                try:
                    with open(old, "rb") as source:
                        with open(new, "wb") as dest:

                            while True:
                                chunk = source.read(512)

                                if not chunk:
                                    break

                                dest.write(chunk)

                except Exception:
                    try:
                        os.remove(new)
                    except OSError:
                        pass
                    raise

                return "Copied to " + new

            # BRIGHTNESS
            if verb == "brightness":

                v = int(arg)

                if not 0 <= v <= 100:
                    raise ValueError(
                        "Use 0..100"
                    )

                display.brightness(
                    v * 65535 // 100
                )

                return "Brightness: %d%%" % v

            # RGB COLOR TEST
            if verb == "colors":

                for color, label in (
                    (RED, "RED"),
                    (GREEN, "GREEN"),
                    (0x001F, "BLUE")
                ):

                    display.fill_screen(color)

                    print(
                        label,
                        "visible for 1 second"
                    )

                    time.sleep(1)

                self.status()

                return "Color check complete"

            # GARBAGE COLLECTION
            if verb == "gc":

                before = gc.mem_free()

                gc.collect()

                after = gc.mem_free()

                return (
                    "Heap free %d -> %d"
                    % (before, after)
                )

            if verb == "quit":
                return None

            raise ValueError(
                "Unknown command; type help"
            )

        except Exception as exc:

            self.screen(
                "ERROR",
                [
                    str(exc)[:29],
                    "See Thonny console"
                ]
            )

            return "ERROR: " + str(exc)


# -------------------------------------------
# HELP
# -------------------------------------------

HELP = """
RP2040-GEEK COMMANDS

home                 Home status screen
mount                Mount SD card
umount               Unmount SD card

ls / list            List SD files
next / prev          Next / previous page
cd folder            Enter directory
cd ..                Parent directory

open filename        Open file
open 0               Open file by index

logo                 Show internal BMP

info                 SD / RAM / CPU information
test                 SD read/write/delete test

mkdir dirname        Create directory
touch filename       Create empty file

copy old | new       Copy file
rename old | new     Rename file

rm filename          Delete file
rmdir dirname        Delete empty directory

brightness 0..100    Adjust backlight
colors               RGB test
gc                   Garbage collection

help                 Show commands
quit                 Exit app

File management is restricted to /sd.
"""


# -------------------------------------------
# CPU FREQUENCY
# -------------------------------------------

def machine_freq():

    import machine

    return machine.freq()


# -------------------------------------------
# MAIN APPLICATION
# -------------------------------------------

def run():

    # Initialize LCD
    display.init_display()

    display.set_rotation(1)

    app = GeekApp()

    print()
    print("RP2040-GEEK starting...")

    # ---------------------------------------
    # STARTUP LOGO
    # ---------------------------------------

    try:
        result = app.logo(pause=2)
        print(result)

    except Exception as exc:
        print(
            "Startup logo skipped:",
            exc
        )

    # ---------------------------------------
    # AUTOMATIC SD MOUNT
    # ---------------------------------------

    print("Initializing SD card...")

    result = app.mount()

    print(result)

    app.message = result

    # ---------------------------------------
    # INITIAL SCREEN
    # ---------------------------------------

    if app.mounted:

        print("SD ready.")

        print(
            "Use ls, list or open <index>."
        )

        try:
            app.browser(0)

        except Exception as exc:

            print(
                "SD directory error:",
                exc
            )

            app.status()

    else:

        app.status()

        print(
            "SD unavailable. Retry using mount."
        )

    # ---------------------------------------
    # HELP
    # ---------------------------------------

    print(HELP)

    print(
        "The GEEK has no navigation keypad."
    )

    print(
        "Use Thonny REPL."
    )

    # ---------------------------------------
    # COMMAND LOOP
    # ---------------------------------------

    while True:

        try:
            cmd = input("GEEK> ")

        except (EOFError, KeyboardInterrupt):

            print("Exited")
            break

        result = app.command(cmd)

        if result is None:
            break

        app.message = result

        if result:
            print(result)

    return app


# -------------------------------------------
# DIRECT EXECUTION
# -------------------------------------------

if __name__ == "__main__":
    run()
