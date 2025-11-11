import display
import draw
import write
import image  # si no lo usas, no molesta
from sd_helpers import mount_sd, get_sd_info

# ---- Inicializar display ----
display.init_display()
display.fill_screen(0b0000000000000000)  # Negro

# Colores RGB565
RED     = 0b1111100000000000
GREEN   = 0b0000011111100000
BLUE    = 0b0000000000011111
YELLOW  = 0b1111111111100000
BLACK   = 0b0000000000000000
WHITE   = 0b1111111111111111
CYAN    = 0b0000011111111111
ORANGE  = 0b1111110000000000

display.set_rotation(1)  # Apaisado

# ---- Montar SD y obtener info ----
sd = None
mount_point = "/sd"
sd_ok = False
sd_info = None
try:
    sd, mount_point = mount_sd()  # usa SPI0: 18/19/20/21
    sd_ok = True
    sd_info = get_sd_info(mount_point, sd_obj=sd)
except Exception as e:
    sd_ok = False
    sd_info = None
    # Si quieres, muestra error en consola:
    print("SD ERROR:", e)

# ---- Decoración: líneas/figuras de tu demo ----
#draw.line(134, 239, 10, 10, GREEN)  # línea verde
#draw.rectangle(10, 10, 50, 30, color=GREEN)                     # rect sin relleno
draw.rectangle(180, 10, 220, 30, color=BLUE, filled=True)        # rect relleno
#draw.circle(95, 95, radius=30, color=RED)                       # círculo sin relleno
draw.circle(210, 120, radius=10, color=YELLOW, filled=True)       # círculo relleno
#draw.polygon(GREEN, False, (10, 10), (20, 50), (80, 60), (50, 10), (9, 10))
#draw.polygon(RED,   True,  (60, 60), (120, 50), (180, 60), (150, 100), (90, 100))

# ---- Texto: datos de la SD (sustituye lo “aleatorio”) ----
x0 = 10
y0 = 20
bg = BLACK

if sd_ok and sd_info:
    write.text(x0, y0,      "SD Card Info",           WHITE, bg, size=12)
    y0 += 12

    cap = sd_info["capacidad_total_mb"]
    libre = sd_info["espacio_libre_mb"]
    usado = sd_info["espacio_usado_mb"]

    write.text(x0, y0,      "Estado: OK",             GREEN, bg, size=12);   y0 += 12
    write.text(x0, y0,      "Capacidad: %.2f MiB" % cap,    CYAN,  bg, size=12); y0 += 12
    write.text(x0, y0,      "Libre:     %.2f MiB" % libre,  CYAN,  bg, size=12); y0 += 12
    write.text(x0, y0,      "Usado:     %.2f MiB" % usado,  CYAN,  bg, size=12); y0 += 16

    write.text(x0, y0,      "Archivos en /sd:",       ORANGE, bg, size=12);  y0 += 12

    # Lista 10 items máx para no llenar la pantalla
    max_items = 10
    for name in sd_info["archivos"][:max_items]:
        # recorta si tu write.text no hace clipping
        shown = name[:28]
        write.text(x0 + 6, y0, "- " + shown, WHITE, bg, size=12)
        y0 += 12

    # Si hay más, indica paginación
    if len(sd_info["archivos"]) > max_items:
        write.text(x0 + 6, y0, "... (mas archivos)", YELLOW, bg, size=12)
        y0 += 12

else:
    write.text(x0, y0, "SD Card Info", WHITE, bg, size=12); y0 += 12
    write.text(x0, y0, "Estado: ERROR", RED, bg, size=12);  y0 += 12
    write.text(x0, y0, "Ver consola y FAT32", WHITE, bg, size=12)

# Imagen en la SD
#image.show_bmp("/sd/RP2040-GEEK.bmp", x_offset=0, y_offset=0)

# Imagen en la raiz del rp2040
#image.show_bmp("RP2040-GEEK.bmp", x_offset=0, y_offset=0)



