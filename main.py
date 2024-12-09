from GEEK import LCD_1inch14, BMPReader
import time



LCD = LCD_1inch14()
    #color BRG
LCD.fill(LCD.red) # que es lo mismo que escribir LCD.fill(0b1111100000000000) o su equivalente en hexadecimal
LCD.draw_line(10, 10, 10, 100, 0b1111100000000000)  # rojo
LCD.draw_line(20, 20, 10, 100, 0b0000000000011111)  # azul
LCD.draw_line(30, 30, 10, 100, 0b0000011111100000)  # verde
#LCD.show()
#lcd.draw_line(10, 10, 10, 100, 0b1111100000000000)  # rojo



    
#LCD.draw_bmp("RP2040-GEEK.bmp")



#LCD.text("RP2040-GEEK",60,40,0XF800)
#LCD.text("read bmp file ...",60,80,0X001F)
#LCD.show()
#LCD.draw_pixel(10, 10, 0b0000011111100000)  # verde

#LCD.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0x001F, fill=True)  # Pentágono azul lleno
#LCD.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0b000011111100000, fill=True)  # Pentágono verde lleno

#LCD.draw_rectangle(50, 50, 100, 60, 0xF800, fill=False)  # Rectángulo rojo lleno
#LCD.draw_oval(120, 67, 50, 30, 0b0000000000011111, fill=True)  # Óvalo azul lleno
#LCD.draw_oval(120, 67, 50, 30, 0b0000000000011111)  # Óvalo azul 

#LCD.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F, fill=True)  # Trapecio azul lleno
#LCD.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F)  # Trapecio azul solo borde
#LCD.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0x001F, fill=True)  # Pentágono azul lleno
#LCD.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0b000011111100000, fill=True)  # Pentágono verde lleno

#LCD.draw_rectangle(50, 50, 100, 60, 0xF800, fill=True)  # Rectángulo rojo lleno
#LCD.draw_oval(120, 67, 50, 30, 0b0000000000011111, fill=True)  # Óvalo azul lleno
LCD.draw_oval(120, 67, 50, 30, 0b0000000000011111)  # Óvalo azul 

#LCD.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F, fill=True)  # Trapecio azul lleno
#LCD.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F)  # Trapecio azul solo borde

#LCD.draw_square(50, 30, 40, 0x07E0)  # Cuadrado verde
#LCD.draw_square(50, 30, 40, 0x07E0, fill=True)  # Cuadrado verde lleno
#LCD.draw_circle(120, 67, 50, 0xF800, fill=True)  # Círculo rojo lleno

#LCD.draw_triangle(50, 50, 150, 50, 100, 100, 0x001F, fill=True)  # Azul

LCD.show()




