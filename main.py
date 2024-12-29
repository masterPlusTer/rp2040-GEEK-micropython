import display
import draw
import write
import image
# Inicializar el display
display.init_display()
display.fill_screen(0b0000000000000000)  # Llenar la pantalla con azul

# Colores en formato RGB565
red = 0b1111100000000000    # Rojo puro
green = 0b0000011111100000  # Verde puro
blue = 0b0000000000011111   # Azul puro
yellow = 0b1111111111100000 # Amarillo
black = 0b0000000000000000  # Negro
white = 0b1111111111111111  # Blanco


display.set_rotation(3)  # Apaisado (90 grados)



# Dibujar píxeles en diferentes posiciones y colores
#draw_pixel(0, 0, red)       # Esquina superior izquierda
#draw.pixel(134, 0, red)       # Esquina superior derecha

#draw.pixel(120, 150, blue)

#draw.pixel(0, 239, blue) # Esquina inferior izquierda

#draw.pixel(134, 239, green) # Esquina inferior derecha

#draw.line(134, 239,10, 10, green) # linea verde
draw.line(134, 239,50, 50, red) # linea roja
#draw.line(134, 239,100,100, blue) # linea azul


# Dibuja un rectángulo sin relleno
#draw.rectangle(10, 10, 50, 30, color=0b0000011111100000)  # Color verde

# Dibuja un rectángulo con relleno
draw.rectangle(60, 10, 100, 30, color=0b0000000000011111, filled=True)  # Color azul

 #Dibuja un círculo sin relleno
#draw.circle(95, 95, radius=30, color=0b1111100000000000)  # Color rojo

# Dibuja un círculo relleno
#draw.circle(50, 50, radius=30, color=0xFFFF00, filled=True)  # Color amarillo


# Dibuja un polígono sin relleno
draw.polygon(0b0000011111100000, False, (10, 10), (20, 50), (80, 60), (50, 10), (9, 10))

# Dibuja un polígono relleno
#draw.polygon(0b1111100000000000, True, (60, 60), (120, 50), (180, 60), (150, 100), (90, 100))



# Escribir texto en el display
write.text(10, 20, "abcdefghijklmnopqrstuvwxyz", 0b1111100000000000, 0b0000000000000000)  # Texto rojo sobre fondo negro
#write.text(10, 30, "ABCDEFGHIJKLMNOPQRSTUVWZYZ", 0b1111100000000000, 0b0000000000000000)  # Texto rojo sobre fondo negro
#write.text(10, 40, "1234567890 _ ? !", 0b1111100000000000, 0b0000000000000000)  # Texto rojo sobre fondo negro
#write.text(10, 50, "+ - = % # < >", 0b1111100000000000, 0b0000000000000000)  # Texto rojo sobre fondo negro


#write.text(10, 60, "abcdefghijklmnopqrstuvwxyz", 0b1111100000000000, 0b0000000000000000, size=10)  # Texto rojo sobre fondo negro
#write.text(10, 70, "ABCDEFGHIJKLMNOPQRSTUVWZYZ", 0b1111100000000000, 0b0000000000000000, size=10)  # Texto rojo sobre fondo negro
write.text(10, 80, "1234567890 _ ? !", 0b1111100000000000, 0b0000000000000000, size=10)  # Texto rojo sobre fondo negro
#write.text(10, 90, "+ - = % # < >", 0b1111100000000000, 0b0000000000000000, size=10)  # Texto rojo sobre fondo negro


#write.text(10, 100, "abcdefghijklmnopqrstuvwxyz", 0b1111100000000000, 0b0000000000000000, size=12)  # Texto rojo sobre fondo negro
#write.text(10, 110, "ABCDEFGHIJKLMNOPQRSTUVWZYZ", 0b1111100000000000, 0b0000000000000000, size=12)  # Texto rojo sobre fondo negro
write.text(10, 120, "1234567890 _ ? !", 0b1111100000000000, 0b0000000000000000, size=12)  # Texto rojo sobre fondo negro
#write.text(10, 130, "+ - = % # < >", 0b1111100000000000, 0b0000000000000000, size=12)  # Texto rojo sobre fondo negro


#image.show_bmp("/RP2040-GEEK.bmp", x_offset=0, y_offset=0)


