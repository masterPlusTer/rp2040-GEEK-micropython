import display
import draw
import font_small
import font_medium
import font_large


def draw_char(x, y, char, color, bg_color, size=8):
    """Dibuja un carácter en el display con un tamaño específico."""
    if size == 8:
        font = font_small.font_8x8
        width, height = 8, 8
    elif size == 10:
        font = font_medium.font_10x10
        width, height = 10, 10
    elif size == 12:
        font = font_large.font_12x12
        width, height = 12, 12
    else:
        raise ValueError("Tamaño de fuente no soportado. Usa 8, 10 o 12.")

    if char not in font:
        return  # Salta si el carácter no está en la fuente

    bitmap = font[char]
    for row_index, row in enumerate(bitmap):
        for col_index in range(width):
            if row & (1 << (width - 1 - col_index)):  # Verifica cada bit
                draw.pixel(x + col_index, y + row_index, color)  # Pixel encendido
            else:
                draw.pixel(x + col_index, y + row_index, bg_color)  # Pixel apagado
def text(x, y, text, color, bg_color, size=8):
    """Dibuja una cadena de texto comenzando en la posición (x, y) con un tamaño específico."""
    if size == 8:
        spacing = 8
    elif size == 10:
        spacing = 10
    elif size == 12:
        spacing = 12
    else:
        raise ValueError("Tamaño de fuente no soportado. Usa 8, 10 o 12.")

    for i, char in enumerate(text):
        draw_char(x + i * spacing, y, char, color, bg_color, size=size)



