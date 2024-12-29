import display

def pixel(x, y, color):
    """Dibuja un píxel en las coordenadas especificadas."""
    display.set_active_window(x, y, x, y)  # Configurar para un solo píxel
    display.write_cmd(0x2C)
    display.write_data(color >> 8)  # Byte alto del color
    display.write_data(color & 0xFF)  # Byte bajo del color
    
def line(x0, y0, x1, y1, color):
    """Dibuja una línea entre los puntos (x0, y0) y (x1, y1) con el color especificado."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        pixel(x0, y0, color)  # Dibuja el píxel en las coordenadas actuales
        if x0 == x1 and y0 == y1:  # Si hemos llegado al final
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x0 += sx
        if err2 < dx:
            err += dx
            y0 += sy    
    
  
def rectangle(x0, y0, x1, y1, color, filled=False):
    """
    Dibuja un rectángulo entre los puntos (x0, y0) y (x1, y1) con el color especificado.
    Si 'filled' es True, el rectángulo estará relleno.
    """
    if filled:
        # Optimización para rectángulos rellenos usando ventanas y buffers
        x_start = min(x0, x1)
        x_end = max(x0, x1)
        y_start = min(y0, y1)
        y_end = max(y0, y1)
        
        display.set_active_window(x_start, y_start, x_end, y_end)  # Configurar la ventana activa
        display.write_cmd(0x2C)  # Comando para escribir en memoria
        
        # Crear un buffer para una línea completa
        line_length = x_end - x_start + 1
        line_buffer = bytearray([color >> 8, color & 0xFF] * line_length)
        
        # Enviar líneas al display
        for _ in range(y_start, y_end + 1):
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(line_buffer)
            display.cs.value(1)
    else:
        # Contorno del rectángulo (no relleno)
        # Líneas horizontales superior e inferior
        for x in range(min(x0, x1), max(x0, x1) + 1):
            pixel(x, min(y0, y1), color)  # Línea superior
            pixel(x, max(y0, y1), color)  # Línea inferior
        
        # Líneas verticales izquierda y derecha
        for y in range(min(y0, y1), max(y0, y1) + 1):
            pixel(min(x0, x1), y, color)  # Línea izquierda
            pixel(max(x0, x1), y, color)  # Línea derecha


def circle(x0, y0, radius, color, filled=False):
    """
    Dibuja un círculo con centro en (x0, y0) y un radio 'radius'.
    Si 'filled' es True, el círculo estará relleno.
    """
    x = radius
    y = 0
    err = 0

    while x >= y:
        if filled:
            # Dibuja líneas horizontales para rellenar el círculo
            display.set_active_window(x0 - x, y0 + y, x0 + x, y0 + y)
            display.write_cmd(0x2C)
            line_color = bytearray([color >> 8, color & 0xFF] * (2 * x + 1))
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(line_color)
            display.cs.value(1)

            display.set_active_window(x0 - x, y0 - y, x0 + x, y0 - y)
            display.write_cmd(0x2C)
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(line_color)
            display.cs.value(1)

            display.set_active_window(x0 - y, y0 + x, x0 + y, y0 + x)
            display.write_cmd(0x2C)
            line_color = bytearray([color >> 8, color & 0xFF] * (2 * y + 1))
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(line_color)
            display.cs.value(1)

            display.set_active_window(x0 - y, y0 - x, x0 + y, y0 - x)
            display.write_cmd(0x2C)
            display.cs.value(0)
            display.dc.value(1)
            display.spi.write(line_color)
            display.cs.value(1)
        else:
            # Dibuja solo el contorno del círculo
            pixel(x0 + x, y0 + y, color)
            pixel(x0 - x, y0 + y, color)
            pixel(x0 + x, y0 - y, color)
            pixel(x0 - x, y0 - y, color)
            pixel(x0 + y, y0 + x, color)
            pixel(x0 - y, y0 + x, color)
            pixel(x0 + y, y0 - x, color)
            pixel(x0 - y, y0 - x, color)

        y += 1
        err += 1 + 2 * y
        if 2 * (err - x) + 1 > 0:
            x -= 1
            err += 1 - 2 * x
  
            
def polygon(color, filled=False, *vertices):
    """
    Dibuja un polígono basado en una lista de vértices.
    :param color: Color en formato RGB565.
    :param filled: Si es True, rellena el polígono.
    :param vertices: Vértices del polígono como argumentos ((x1, y1), (x2, y2), ...).
    """
    if len(vertices) < 3:
        raise ValueError("Un polígono debe tener al menos 3 vértices.")
    
    if filled:
        # Escaneo horizontal para llenar el polígono
        min_y = min(y for _, y in vertices)
        max_y = max(y for _, y in vertices)

        for y in range(min_y, max_y + 1):
            intersections = []
            for i in range(len(vertices)):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % len(vertices)]
                if y1 < y2:
                    x_start, y_start = x1, y1
                    x_end, y_end = x2, y2
                else:
                    x_start, y_start = x2, y2
                    x_end, y_end = x1, y1
                
                if y_start <= y < y_end:
                    x = int(x_start + (y - y_start) * (x_end - x_start) / (y_end - y_start))
                    intersections.append(x)
            
            intersections.sort()
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    display.set_active_window(intersections[i], y, intersections[i + 1], y)
                    display.write_cmd(0x2C)  # Comando para escribir en memoria
                    line_color = bytearray([color >> 8, color & 0xFF] * (intersections[i + 1] - intersections[i] + 1))
                    display.cs.value(0)
                    display.dc.value(1)
                    display.spi.write(line_color)
                    display.cs.value(1)
    else:
        # Dibuja el contorno del polígono
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            line(x1, y1, x2, y2, color)

