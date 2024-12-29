import display
import draw
import font_small
import font_medium
import font_large

def draw_char(x, y, char, color, bg_color, size=8):
    """
    Dibuja un carácter en el display con un tamaño específico.
    :param x: Coordenada X inicial.
    :param y: Coordenada Y inicial.
    :param char: Carácter a dibujar.
    :param color: Color del texto en formato RGB565.
    :param bg_color: Color de fondo en formato RGB565.
    :param size: Tamaño de la fuente (8, 10, 12).
    """
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

    # Obtener el bitmap del carácter
    bitmap = font[char]
    # Crear un buffer para el carácter completo
    char_buffer = bytearray(width * height * 2)

    # Procesar el bitmap y llenar el buffer
    for row_index, row in enumerate(bitmap):
        for col_index in range(width):
            if row & (1 << (width - 1 - col_index)):
                pixel_color = color  # Pixel encendido
            else:
                pixel_color = bg_color  # Pixel apagado

            # Calcular posición en el buffer
            index = 2 * (row_index * width + col_index)
            char_buffer[index] = pixel_color >> 8  # Byte alto
            char_buffer[index + 1] = pixel_color & 0xFF  # Byte bajo

    # Dibujar el carácter usando una ventana activa
    display.set_window_and_write(x, y, x + width - 1, y + height - 1, char_buffer)


def text(x, y, text, color, bg_color, size=8):
    """
    Dibuja una cadena de texto comenzando en la posición (x, y) con un tamaño específico.
    :param x: Coordenada X inicial.
    :param y: Coordenada Y inicial.
    :param text: Texto a dibujar.
    :param color: Color del texto en formato RGB565.
    :param bg_color: Color de fondo en formato RGB565.
    :param size: Tamaño de la fuente (8, 10, 12).
    """
    if size == 8:
        spacing = 8
    elif size == 10:
        spacing = 10
    elif size == 12:
        spacing = 12
    else:
        raise ValueError("Tamaño de fuente no soportado. Usa 8, 10 o 12.")

    for i, char in enumerate(text):
        draw_char(x + i * spacing, y, char, color, bg_color, size)



