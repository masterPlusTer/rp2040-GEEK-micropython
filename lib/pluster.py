import board
#BRILLO DEL DISPLAY
brilloDefault = 0.5

def brillo(nuevo_brillo):
    global brilloDefault
    brilloDefault = nuevo_brillo / 10.0  # División entre 10 para agregar el decimal
    board.DISPLAY.brightness = brilloDefault


