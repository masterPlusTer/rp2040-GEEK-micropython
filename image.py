import display

def show_bmp(file_path, x_offset=0, y_offset=0):
    """
    Muestra un archivo BMP en el display reflejado horizontalmente.
    :param file_path: Ruta del archivo BMP.
    :param x_offset: Desplazamiento horizontal para dibujar la imagen.
    :param y_offset: Desplazamiento vertical para dibujar la imagen.
    """
    with open(file_path, "rb") as bmp_file:
        # Leer el encabezado BMP
        bmp_file.seek(10)
        pixel_data_offset = int.from_bytes(bmp_file.read(4), "little")

        bmp_file.seek(18)
        width = int.from_bytes(bmp_file.read(4), "little")
        height = int.from_bytes(bmp_file.read(4), "little")

        bmp_file.seek(28)
        bits_per_pixel = int.from_bytes(bmp_file.read(2), "little")

        if bits_per_pixel != 24:
            raise ValueError("Solo se admiten BMP de 24 bits.")

        # Crear un buffer para la imagen completa
        image_buffer = bytearray(width * height * 2)

        # Mover a los datos de píxeles
        bmp_file.seek(pixel_data_offset)

        # Procesar toda la imagen
        for y in range(height):
            line_buffer = bytearray(bmp_file.read(width * 3))  # Leer línea RGB888
            for x in range(width):
                b = line_buffer[3 * x]
                g = line_buffer[3 * x + 1]
                r = line_buffer[3 * x + 2]

                # Convertir a RGB565
                color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

                # Insertar el color reflejado en el buffer
                mirrored_x = width - x - 1
                index = 2 * (y * width + mirrored_x)
                image_buffer[index] = color >> 8  # Byte alto
                image_buffer[index + 1] = color & 0xFF  # Byte bajo

        # Enviar la imagen completa al display
        display.set_window_and_write(x_offset, y_offset, x_offset + width - 1, y_offset + height - 1, image_buffer)
