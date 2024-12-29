import draw
import write
import display

def draw_interface():
    """
    Dibuja la interfaz de usuario según la rotación configurada en display.set_rotation().
    """
    # Leer la rotación configurada en display
    # Aquí asumimos que `display.get_rotation()` devolvería el valor configurado
    rotation = display.get_rotation()  # Este valor podría ser el mismo pasado al set_rotation() si no hay un método get_rotation()

    # Limpiar pantalla

    # Dibujar encabezado
    draw.rectangle(0, 0, 239, 20, color=0b0000000000011111, filled=True)  # Encabezado azul
    write.text(5, 5, "Interfaz UI", 0b1111111111111111, 0b0000000000011111, size=10)

    # Dibujar una tabla
    draw.rectangle(5, 25, 125, 100, color=0b1111111111111111, filled=False)  # Contorno de la tabla

    # Líneas horizontales
    for row in range(1, 4):
        y = 25 + row * 20
        draw.line(5, y, 125, y, 0b1111111111111111)

    # Líneas verticales
    draw.line(45, 25, 45, 100, 0b1111111111111111)
    draw.line(85, 25, 85, 100, 0b1111111111111111)

    # Rellenar las celdas de la tabla con texto
    cell_texts = [
        ["F1", "D1", "D2"],
        ["F2", "D3", "D4"],
        ["F3", "D5", "D6"],
    ]
    for i, row in enumerate(cell_texts):
        y = 25 + i * 20 + 5
        write.text(8, y, row[0], 0b1111111111111111, 0b0000000000000000, size=8)  # Primera columna
        write.text(50, y, row[1], 0b1111111111111111, 0b0000000000000000, size=8)  # Segunda columna
        write.text(90, y, row[2], 0b1111111111111111, 0b0000000000000000, size=8)

    # Dibujar un botón
    draw.rectangle(10, 110, 110, 125, color=0b1111100000000000, filled=True)  # Botón rojo
    write.text(40, 115, "OK", 0b1111111111111111, 0b1111100000000000, size=8)

    # Dibujar una lista o cuadro amarillo según la rotación
    if rotation == 3:  # Horizontal normal
        draw.rectangle(130, 25, 235, 125, color=0b1111111111100000, filled=False)  # A la derecha del blanco
        list_items = ["Item1", "Item2", "Item3"]
        for i, item in enumerate(list_items):
            y = 25 + i * 30
            write.text(135, y + 5, item, 0b1111111111100000, 0b0000000000000000, size=8)
    elif rotation == 0:  # Vertical normal
        draw.rectangle(5, 145, 125, 200, color=0b1111111111100000, filled=False)  # Debajo del blanco
        list_items = ["Item1", "Item2", "Item3"]
        for i, item in enumerate(list_items):
            y = 145 + i * 20
            write.text(10, y + 5, item, 0b1111111111100000, 0b0000000000000000, size=8)
    elif rotation == 2:  # Horizontal invertido
        draw.rectangle(5, 140, 125, 215, color=0b1111111111100000, filled=False)  # Debajo del blanco
        list_items = ["Item1", "Item2", "Item3"]
        for i, item in enumerate(list_items):
            y = 150 + i * 25
            write.text(10, y, item, 0b1111111111100000, 0b0000000000000000, size=8)
    elif rotation == 1:  # Vertical invertido
        draw.rectangle(130, 25, 235, 125, color=0b1111111111100000, filled=False)  # A la derecha del blanco
        list_items = ["Item1", "Item2", "Item3"]
        for i, item in enumerate(list_items):
            y = 25 + i * 30
            write.text(135, y + 5, item, 0b1111111111100000, 0b0000000000000000, size=8)

