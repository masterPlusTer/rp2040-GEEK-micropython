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

        # Configurar la ventana activa en el display
        display.set_active_window(x_offset, y_offset, x_offset + width - 1, y_offset + height - 1)
        display.write_cmd(0x2C)  # Comando para escribir en memoria

        # Mover a los datos de píxeles
        bmp_file.seek(pixel_data_offset)

        # Buffer para procesar una línea completa
        line_buffer = bytearray(width * 3)  # Buffer para la línea en formato RGB888
        mirrored_line = bytearray(width * 2)  # Buffer para la línea reflejada en RGB565

        # Procesar línea por línea
        for y in range(height):
            # Leer una línea completa en formato RGB888
            bmp_file.readinto(line_buffer)

            # Convertir y reflejar la línea
            for x in range(width):
                b = line_buffer[3 * x]
                g = line_buffer[3 * x + 1]
                r = line_buffer[3 * x + 2]

                # Convertir a RGB565
                color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

                # Insertar el color reflejado
                mirrored_x = width - x - 1
                mirrored_line[2 * mirrored_x] = color >> 8
                mirrored_line[2 * mirrored_x + 1] = color & 0xFF

            # Enviar la línea reflejada al display
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(mirrored_line)
            display.cs.value(1)


