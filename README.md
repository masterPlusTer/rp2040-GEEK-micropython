interface novato friendly para el rp2040-GEEK ( en construccion )


# GEEK.py: Librería para Pantallas LCD con RP2040

## Introducción
La librería **GEEK.py** está diseñada para facilitar el control de pantallas LCD en dispositivos basados en el microcontrolador RP2040, como la Raspberry Pi Pico. Incluye funciones avanzadas para dibujar figuras, mostrar imágenes BMP y realizar operaciones de bajo nivel con el display.

Esta guía está orientada a usuarios principiantes y proporciona instrucciones claras sobre cómo empezar a usar la librería.

---

## Requisitos

### Hardware
- Microcontrolador RP2040 (Raspberry Pi Pico o similar).
- Pantalla LCD de 1.14 pulgadas compatible con el controlador ST7789.
- Conexiones SPI configuradas según los pines especificados:
  - **BL (Backlight)**: Pin 25
  - **DC (Data/Command)**: Pin 8
  - **CS (Chip Select)**: Pin 9
  - **SCK (Serial Clock)**: Pin 10
  - **MOSI (Master Out, Slave In)**: Pin 11
  - **RST (Reset)**: Pin 12

### Software
- MicroPython instalado en el RP2040.
- Librería **GEEK.py**.

---

## Instalación
1. **Descargar la librería**:
   Copia el archivo `GEEK.py` en tu dispositivo RP2040 utilizando herramientas como Thonny o cualquier editor compatible con MicroPython.

2. **Conectar la pantalla LCD**:
   Realiza las conexiones entre tu pantalla LCD y el RP2040 según los pines mencionados en la sección de requisitos.

3. **Probar la configuración inicial**:
   Abre el entorno de desarrollo y escribe el siguiente código para verificar que la pantalla esté funcionando:

   ```python
   from GEEK import LCD_1inch14
   
   lcd = LCD_1inch14()
   lcd.draw_pixel(10, 10, lcd.red)  # Dibuja un pixel rojo en (10, 10)
   lcd.show()
   ```

---

## Uso de la Librería

### Inicialización de la Pantalla

Para inicializar la pantalla, crea una instancia de la clase `LCD_1inch14`:

```python
from GEEK import LCD_1inch14

lcd = LCD_1inch14()
```

### Dibujar Figuras

La librería proporciona múltiples funciones para dibujar:

#### Píxel
```python
lcd.draw_pixel(x, y, color)
```
Dibuja un píxel en la posición `(x, y)` con el color especificado.

#### Línea
```python
lcd.draw_line(x1, y1, x2, y2, color)
```
Dibuja una línea entre los puntos `(x1, y1)` y `(x2, y2)`.

#### Círculo
```python
lcd.draw_circle(x0, y0, radius, color, fill=False)
```
Dibuja un círculo con centro en `(x0, y0)` y radio `radius`. Usa `fill=True` para rellenarlo.

#### Cuadrado
```python
lcd.draw_square(x0, y0, side, color, fill=False)
```
Dibuja un cuadrado con esquina superior izquierda en `(x0, y0)` y lado de longitud `side`.

#### Rectángulo
```python
lcd.draw_rectangle(x0, y0, width, height, color, fill=False)
```
Dibuja un rectángulo con esquina superior izquierda en `(x0, y0)` y dimensiones `width` x `height`.

#### Triángulo
```python
lcd.draw_triangle(x1, y1, x2, y2, x3, y3, color, fill=False)
```
Dibuja un triángulo conectando los puntos `(x1, y1)`, `(x2, y2)` y `(x3, y3)`.

#### Forma Genérica
```python
lcd.draw_shape(points, color, fill=False)
```
Dibuja una figura definida por la lista de puntos `points`.

### Mostrar Imágenes BMP

La librería permite cargar y mostrar imágenes BMP.

```python
lcd.draw_bmp('imagen.bmp')
```
Asegúrate de que el archivo BMP esté en la memoria del dispositivo y sea de 24 bits.

---

## Colores
Los colores deben especificarse en formato RGB565. Algunos colores predefinidos son:

- **Rojo**: `LCD.red`
- **Verde**: `LCD.green`
- **Azul**: `LCD.blue`
- **Blanco**: `LCD.white`

---

## Ejemplo Completo
El siguiente ejemplo dibuja varias formas y muestra un mensaje:

```python
from GEEK import LCD_1inch14

lcd = LCD_1inch14()
lcd.fill(lcd.white)  # Limpia la pantalla con color blanco

# Dibujar formas
lcd.draw_circle(60, 60, 30, lcd.blue, fill=True)
lcd.draw_rectangle(100, 50, 50, 30, lcd.green, fill=True)
lcd.draw_triangle(150, 70, 170, 120, 130, 120, lcd.red)

# Mostrar texto (requiere función adicional para texto)
# lcd.draw_text(10, 10, "Hola Mundo", lcd.black)

lcd.show()
```

---

## Consejos
1. Usa colores en formato RGB565 para garantizar la compatibilidad.
2. Limpia la pantalla antes de dibujar nuevas figuras usando `lcd.fill(color)`.
3. Revisa las conexiones del hardware si experimentas problemas.

---

## Contribuir
Si tienes sugerencias o encuentras errores, no dudes en abrir un issue en el repositorio de la librería.

---

## Licencia
Esta librería está bajo la licencia MIT. Puedes usarla y modificarla libremente siempre y cuando incluyas la licencia original.

