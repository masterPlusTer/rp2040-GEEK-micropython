import display
import struct, gc

def show_bmp(file_path, x_offset=0, y_offset=0, mirror=False, flip_vertical=False):
    """
    Muestra un BMP 24 bpp (RGB888) en el display sin agotar RAM.
    - mirror:   espejo horizontal (False = normal)
    - flip_vertical: invierte verticalmente (False = normal)
    """
    with open(file_path, "rb") as f:
        # Encabezados BMP
        if f.read(2) != b"BM":
            raise ValueError("No es un BMP válido (BM)")

        file_size, _, _, pixel_data_offset = struct.unpack("<IHHI", f.read(12))
        dib_size = struct.unpack("<I", f.read(4))[0]
        if dib_size < 40:
            raise ValueError("DIB header inesperado")

        width, height, planes, bpp = struct.unpack("<iiHH", f.read(12))
        compression, img_size = struct.unpack("<II", f.read(8))

        # Saltar resto del DIB
        if dib_size > 40:
            f.seek(dib_size - 40, 1)

        if bpp != 24:
            raise ValueError("Solo se admiten BMP de 24 bits.")
        if compression not in (0,):
            raise ValueError("BMP con compresión no soportada.")

        # BMP bottom-up si height > 0, top-down si height < 0
        top_down = height < 0
        H = abs(height)
        W = width
        stride = ((W * 3 + 3) // 4) * 4

        f.seek(pixel_data_offset, 0)
        row_out = bytearray(W * 2)

        for out_row in range(H):
            # Fila fuente en archivo
            src_row = out_row if top_down else (H - 1 - out_row)
            # Si piden flip vertical, invertimos la selección visible
            if flip_vertical:
                src_row = (H - 1 - src_row)

            pos = pixel_data_offset + src_row * stride
            f.seek(pos, 0)
            row24 = f.read(stride)

            if mirror:
                for x in range(W):
                    i = x * 3
                    b = row24[i]; g = row24[i+1]; r = row24[i+2]
                    r5 = (r >> 3) & 0x1F
                    g6 = (g >> 2) & 0x3F
                    b5 = (b >> 3) & 0x1F
                    rgb565 = (r5 << 11) | (g6 << 5) | b5
                    mx = W - 1 - x
                    di = mx * 2
                    row_out[di]   = (rgb565 >> 8) & 0xFF
                    row_out[di+1] = rgb565 & 0xFF
            else:
                di = 0
                for x in range(W):
                    i = x * 3
                    b = row24[i]; g = row24[i+1]; r = row24[i+2]
                    r5 = (r >> 3) & 0x1F
                    g6 = (g >> 2) & 0x3F
                    b5 = (b >> 3) & 0x1F
                    rgb565 = (r5 << 11) | (g6 << 5) | b5
                    row_out[di]   = (rgb565 >> 8) & 0xFF
                    row_out[di+1] = rgb565 & 0xFF
                    di += 2

            display.set_window_and_write(
                x_offset,
                y_offset + out_row,
                x_offset + W - 1,
                y_offset + out_row,
                row_out
            )

            if (out_row & 7) == 0:
                gc.collect()
