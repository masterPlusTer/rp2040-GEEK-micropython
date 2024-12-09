from machine import Pin,SPI,PWM
import framebuf
import time
import os
import gc



BL = 25
DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

gc.enable()
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(65535)#max 65535

class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,50_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    @micropython.viper
    def swap(self):
        buf=ptr8(self.buffer)
        for x in range(0,240*135*2,2):
            tt=buf[x]
            buf[x]=buf[x+1]
            buf[x+1]=tt
    @micropython.viper
    def ins(self,ins_data,ins_len:int,start:int):
        ins_buf=ptr8(ins_data)
        buf=ptr8(self.buffer)
        for x in range(ins_len):
            buf[start+x]=ins_buf[x]
    @micropython.viper
    def mirror(self):
        buf=ptr8(self.buffer)
        for y in range(0,135):
            for x in range(0,120):
                temp_x=(240-x)*2
                temp_y=y*480
                t1=buf[x*2+temp_y]
                t2=buf[x*2+temp_y+1]
                buf[x*2+temp_y]=buf[temp_x+temp_y]
                buf[x*2+temp_y+1]=buf[temp_x+temp_y+1]
                buf[temp_x+temp_y]=t1
                buf[temp_x+temp_y+1]=t2
    @micropython.viper
    def flip_y(self):
        """
        Rota la imagen en el eje Y (invertir verticalmente).
        """
        buf = ptr8(self.buffer)
        for y in range(0, 135 // 2):
            for x in range(0, 240):
                # Coordenadas de píxeles en las filas opuestas
                temp_top = (y * 240 + x) * 2
                temp_bottom = ((134 - y) * 240 + x) * 2

                # Intercambiar píxeles entre las filas
                t1 = buf[temp_top]
                t2 = buf[temp_top + 1]
                buf[temp_top] = buf[temp_bottom]
                buf[temp_top + 1] = buf[temp_bottom + 1]
                buf[temp_bottom] = t1
                buf[temp_bottom + 1] = t2
    
    def draw_bmp(self, filename):
        """
        Dibuja una imagen BMP en el display.
        Parámetros:
            filename: Nombre del archivo BMP a mostrar.
        """
        try:
            # Cargar la imagen BMP
            img = BMPReader(filename)

            # Procesar y mostrar la imagen completa
            for x in range(self.width):
                start = x * self.height * 2  # Desplazamiento para cada columna
                buffer = img.get_buf(self.height * 2, start)
                self.ins(buffer, len(buffer), start)

            # Invertir verticalmente (si es necesario)
            self.flip_y()

            # Actualizar la pantalla
            self.show()

        except Exception as e:
            print(f"Error al cargar el archivo BMP: {e}")
          
                
    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.swap()
        self.spi.write(self.buffer)
        self.swap()
        self.cs(1)
        
    def draw_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            super().pixel(x, y, color)
            
            
            
    def draw_line(self, x1, y1, x2, y2, color):
        """
        Dibuja una línea entre dos puntos con el color ajustado.
        """
        # Diferencias en las coordenadas
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        # Dibujar la línea
        while True:
            self.draw_pixel(x1, y1, color)

            if x1 == x2 and y1 == y2:
                break

            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy           
            
            
    def draw_generic_shape(self, outline_points, color, fill=False):
        """
        Dibuja una figura genérica con bordes y opcionalmente relleno.
        Parámetros:
        - outline_points: Lista de tuplas [(x1, y1), (x2, y2), ..., (xn, yn)].
        - color: Color en formato RGB565.
        - fill: Si es True, llena la figura. Por defecto, False.
        """
        if fill:
            # Rellenar la figura usando un algoritmo de escaneo
            sorted_points = sorted(outline_points, key=lambda p: p[1])  # Ordenar por coordenada Y
            y_min = sorted_points[0][1]
            y_max = sorted_points[-1][1]

            for y in range(y_min, y_max + 1):
                intersections = []
                for i in range(len(outline_points)):
                    x1, y1 = outline_points[i]
                    x2, y2 = outline_points[(i + 1) % len(outline_points)]  # Conectar el último punto con el primero

                    # Verificar si la línea cruza la línea de escaneo
                    if y1 <= y < y2 or y2 <= y < y1:
                        x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        intersections.append(int(x))

                intersections.sort()  # Ordenar las intersecciones por X

                # Dibujar líneas horizontales entre pares de intersecciones
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        x_start = intersections[i]
                        x_end = intersections[i + 1]
                        for x in range(x_start, x_end + 1):
                            self.draw_pixel(x, y, color)
        else:
            # Dibujar solo los bordes conectando los puntos
            for i in range(len(outline_points)):
                x1, y1 = outline_points[i]
                x2, y2 = outline_points[(i + 1) % len(outline_points)]  # Conectar el último punto con el primero
                self.draw_line(x1, y1, x2, y2, color)


    def draw_circle(self, x0, y0, radius, color, fill=False):
        """
        Dibuja un círculo.
        Parámetros:
        - x0, y0: Coordenadas del centro del círculo.
        - radius: Radio en píxeles.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el círculo. Por defecto, False.
        """
        if fill:
            # Rellenar el círculo usando la ecuación
            for y in range(-radius, radius + 1):
                for x in range(-radius, radius + 1):
                    if x**2 + y**2 <= radius**2:
                        self.draw_pixel(x0 + x, y0 + y, color)
        else:
            # Dibujar solo los bordes del círculo usando el algoritmo de Bresenham
            x = 0
            y = radius
            d = 3 - 2 * radius

            while x <= y:
                # Dibujar los puntos en los ocho octantes
                self.draw_pixel(x0 + x, y0 + y, color)
                self.draw_pixel(x0 - x, y0 + y, color)
                self.draw_pixel(x0 + x, y0 - y, color)
                self.draw_pixel(x0 - x, y0 - y, color)
                self.draw_pixel(x0 + y, y0 + x, color)
                self.draw_pixel(x0 - y, y0 + x, color)
                self.draw_pixel(x0 + y, y0 - x, color)
                self.draw_pixel(x0 - y, y0 - x, color)

                if d < 0:
                    d += 4 * x + 6
                else:
                    d += 4 * (x - y) + 10
                    y -= 1
                x += 1


    def draw_square(self, x0, y0, side, color, fill=False):
        """
        Dibuja un cuadrado.
        Parámetros:
        - x0, y0: Coordenadas de la esquina superior izquierda.
        - side: Tamaño del lado del cuadrado.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el cuadrado. Por defecto, False.
        """
        points = [
            (x0, y0), (x0 + side, y0),
            (x0 + side, y0 + side), (x0, y0 + side)
        ]
        self.draw_generic_shape(points, color, fill)


    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color, fill=False):
        """
        Dibuja un triángulo.
        Parámetros:
        - x1, y1: Coordenadas del primer vértice.
        - x2, y2: Coordenadas del segundo vértice.
        - x3, y3: Coordenadas del tercer vértice.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el triángulo. Por defecto, False.
        """
        points = [(x1, y1), (x2, y2), (x3, y3)]
        self.draw_generic_shape(points, color, fill)


    def draw_shape(self, points, color, fill=False):
        """
        Dibuja una forma basada en una lista de puntos.
        Parámetros:
        - points: Lista de tuplas [(x1, y1), (x2, y2), ..., (xn, yn)] que representan los vértices.
        - color: Color en formato RGB565.
        - fill: Si es True, llena la forma. Por defecto, False.
        """
        self.draw_generic_shape(points, color, fill)
        
        
        ## figuras no perfectas rectangulo , ovalo , trapecio
        
    def draw_rectangle(self, x0, y0, width, height, color, fill=False):
        """
        Dibuja un rectángulo.
        Parámetros:
        - x0, y0: Coordenadas de la esquina superior izquierda.
        - width: Ancho del rectángulo.
        - height: Alto del rectángulo.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el rectángulo. Por defecto, False.
        """
        points = [
            (x0, y0), (x0 + width, y0),
            (x0 + width, y0 + height), (x0, y0 + height)
        ]
        self.draw_generic_shape(points, color, fill)


    def draw_oval(self, x0, y0, rx, ry, color, fill=False):
        """
        Dibuja un óvalo.
        Parámetros:
        - x0, y0: Coordenadas del centro.
        - rx: Radio horizontal.
        - ry: Radio vertical.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el óvalo. Por defecto, False.
        """
        if fill:
            for y in range(-ry, ry + 1):
                for x in range(-rx, rx + 1):
                    # Ecuación del óvalo: (x^2 / rx^2) + (y^2 / ry^2) <= 1
                    if (x**2 / rx**2) + (y**2 / ry**2) <= 1:
                        self.draw_pixel(x0 + x, y0 + y, color)
        else:
            x = 0
            y = ry
            px = 0
            py = 2 * rx**2 * y
            points = []

            # Región 1: Incrementa x
            p1 = ry**2 - (rx**2 * ry) + (0.25 * rx**2)
            while px < py:
                points.extend([
                    (x0 + x, y0 + y), (x0 - x, y0 + y),
                    (x0 + x, y0 - y), (x0 - x, y0 - y)
                ])
                x += 1
                px += 2 * ry**2
                if p1 < 0:
                    p1 += ry**2 + px
                else:
                    y -= 1
                    py -= 2 * rx**2
                    p1 += ry**2 + px - py

            # Región 2: Incrementa y
            p2 = ry**2 * (x + 0.5)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2
            while y >= 0:
                points.extend([
                    (x0 + x, y0 + y), (x0 - x, y0 + y),
                    (x0 + x, y0 - y), (x0 - x, y0 - y)
                ])
                y -= 1
                py -= 2 * rx**2
                if p2 > 0:
                    p2 += rx**2 - py
                else:
                    x += 1
                    px += 2 * ry**2
                    p2 += rx**2 - py + px

            # Dibujar los bordes del óvalo
            for px, py in points:
                self.draw_pixel(px, py, color)

    def draw_trapezoid(self, x1, y1, x2, y2, x3, y3, x4, y4, color, fill=False):
        """
        Dibuja un trapecio.
        Parámetros:
        - x1, y1: Coordenadas del primer vértice (esquina superior izquierda).
        - x2, y2: Coordenadas del segundo vértice (esquina superior derecha).
        - x3, y3: Coordenadas del tercer vértice (esquina inferior derecha).
        - x4, y4: Coordenadas del cuarto vértice (esquina inferior izquierda).
        - color: Color en formato RGB565.
        - fill: Si es True, llena el trapecio. Por defecto, False.
        """
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.draw_generic_shape(points, color, fill)            
        
class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_info()
    def get_buf(self,data_len:int,start:int=0):
        assert data_len%2 == 0,\
            "return data RGB565,the length have to be a multiple of 2"
        assert start%2 == 0,\
            "return data RGB565,the startpos have to be a multiple of 2"
        buffer=bytearray(data_len)
        with open(self._filename, 'rb') as f:
            f.seek(self.start_pos+(int(start/2*3)))
            img_bytes = bytearray(f.read(int(data_len/2*3)))
            f.close()
        for x in range (int(data_len/2)):

            r=img_bytes[x*3+2]
            g=img_bytes[x*3+1]
            b=img_bytes[x*3]

            img_data = ((r&0xf8)<<8) | ((g&0xf8)<<3) | ((b&0xf8)>>3)
            buffer[x*2]  =   img_data&0xff  
            buffer[x*2+1]= (img_data>>8)&0xff
        img_bytes=0
        return buffer

    def _read_img_info(self):
        def lebytes_to_int(bytes):
            n = 0x00
            while len(bytes) > 0:
                n <<= 8
                n |= bytes.pop()
            return int(n)

        with open(self._filename, 'rb') as f:
            img_bytes = list((f.read(38)))
            f.close()
        # Before we proceed, we need to ensure certain conditions are met
        assert img_bytes[0:2] == [66, 77], "Not a valid BMP file"
        assert lebytes_to_int(img_bytes[30:34]) == 0, \
            "Compression is not supported"
        assert lebytes_to_int(img_bytes[28:30]) == 24, \
            "Only 24-bit colour depth is supported"

        self.start_pos = lebytes_to_int(img_bytes[10:14])
        self.end_pos = self.start_pos + lebytes_to_int(img_bytes[34:38])

        self.width = lebytes_to_int(img_bytes[18:22])
        self.height = lebytes_to_int(img_bytes[22:26])        
        
    
