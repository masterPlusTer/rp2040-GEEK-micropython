import draw
import write
import display

# Colores RGB565
WHITE  = 0xFFFF
BLACK  = 0x0000
BLUE   = 0x001F
RED    = 0xF800
YELLOW = 0xFFE0

def _fmt_mib(x):
    # Redondeo amable para pantallas chicas
    try:
        return "{:.1f}".format(float(x))
    except:
        return "?"

def draw_interface(sd_info=None):
    """
    Dibuja la interfaz de usuario y, si sd_info viene con datos, los muestra.
    sd_info = {
      "capacidad_total_mb": float,
      "espacio_libre_mb": float,
      "espacio_usado_mb": float,
      "archivos": [str, ...]
    }
    """

    rotation = display.get_rotation()

    # Encabezado
    draw.rectangle(0, 0, 239, 20, color=BLUE, filled=True)     # barra azul
    write.text(5, 5, "Interfaz UI", WHITE, BLUE, size=10)

    # Línea bajo header opcional
    # draw.line(0, 20, 239, 20, WHITE)

    # Tabla blanca a la izquierda
    draw.rectangle(5, 25, 125, 100, color=WHITE, filled=False)

    # Líneas horizontales de la tabla (3 filas)
    for row in range(1, 4):
        y = 25 + row * 20
        draw.line(5, y, 125, y, WHITE)

    # Líneas verticales (3 columnas)
    draw.line(45, 25, 45, 100, WHITE)
    draw.line(85, 25, 85, 100, WHITE)

    # Si hay info de SD, rellenamos la tabla con datos reales
    if sd_info:
        cap  = _fmt_mib(sd_info.get("capacidad_total_mb", 0))
        free = _fmt_mib(sd_info.get("espacio_libre_mb", 0))
        used = _fmt_mib(sd_info.get("espacio_usado_mb", 0))
        files = sd_info.get("archivos", [])
        # Cabeceras
        write.text(8,  30, "Cap",  WHITE, BLACK, size=8)
        write.text(50, 30, "Free", WHITE, BLACK, size=8)
        write.text(90, 30, "Used", WHITE, BLACK, size=8)
        # Valores
        write.text(8,  50, cap + "M",  WHITE, BLACK, size=8)
        write.text(50, 50, free + "M", WHITE, BLACK, size=8)
        write.text(90, 50, used + "M", WHITE, BLACK, size=8)
        # Extras: #files y mount
        write.text(8,  70,  "#Files", WHITE, BLACK, size=8)
        write.text(50, 70,  str(len(files)), WHITE, BLACK, size=8)
        write.text(8,  90,  "Status", WHITE, BLACK, size=8)
        write.text(50, 90,  "OK", WHITE, BLACK, size=8)
    else:
        # Placeholders si no hay SD
        cell_texts = [
            ["Cap", "Free", "Used"],
            ["?",    "?",    "?   "],
            ["#Files", "Status", "ERR"],
        ]
        for i, row in enumerate(cell_texts):
            y = 25 + i * 20 + 5
            write.text(8,  y, row[0], WHITE, BLACK, size=8)
            write.text(50, y, row[1], WHITE, BLACK, size=8)
            write.text(90, y, row[2], WHITE, BLACK, size=8)

    # Botón rojo (decorativo)
    draw.rectangle(10, 110, 110, 125, color=RED, filled=True)
    write.text(40, 115, "OK", WHITE, RED, size=8)

    # Panel amarillo para listar archivos según rotación
    if rotation == 3:      # Horizontal normal
        x0, y0, x1, y1 = 130, 25, 235, 125
        draw.rectangle(x0, y0, x1, y1, color=YELLOW, filled=False)
        start_x = x0 + 5
        line_step = 30
    elif rotation == 0:    # Vertical normal
        x0, y0, x1, y1 = 5, 145, 125, 200
        draw.rectangle(x0, y0, x1, y1, color=YELLOW, filled=False)
        start_x = x0 + 5
        line_step = 20
    elif rotation == 2:    # Horizontal invertido
        x0, y0, x1, y1 = 5, 140, 125, 215
        draw.rectangle(x0, y0, x1, y1, color=YELLOW, filled=False)
        start_x = x0 + 5
        line_step = 25
    elif rotation == 1:    # Vertical invertido
        x0, y0, x1, y1 = 130, 25, 235, 125
        draw.rectangle(x0, y0, x1, y1, color=YELLOW, filled=False)
        start_x = x0 + 5
        line_step = 30
    else:
        # Por si tu driver devuelve un valor raro
        x0, y0, x1, y1 = 130, 25, 235, 125
        draw.rectangle(x0, y0, x1, y1, color=YELLOW, filled=False)
        start_x = x0 + 5
        line_step = 30

    # Contenido del panel: lista de archivos de la SD o placeholders
    if sd_info and sd_info.get("archivos"):
        max_rows = max(1, (y1 - y0) // line_step)
        names = sd_info["archivos"][:max_rows]
        for i, name in enumerate(names):
            y = y0 + i * line_step + 5
            # recorte suave a ~12-14 chars para no desbordar
            shown = name[:14]
            write.text(start_x, y, shown, YELLOW, BLACK, size=8)
        # si hay más, indicarlo
        if len(sd_info["archivos"]) > max_rows:
            y = y0 + max_rows * line_step
            if y < y1 - 5:
                write.text(start_x, y, "...", YELLOW, BLACK, size=8)
    else:
        # Sin SD o sin archivos
        placeholders = ["<no SD>" if not sd_info else "<vacio>"]
        for i, item in enumerate(placeholders):
            y = y0 + i * line_step + 5
            write.text(start_x, y, item, YELLOW, BLACK, size=8)
