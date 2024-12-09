# GEEK.py:  Intento de interfaz novato friendly para controlar el rp2040 - GEEK (en construccion)
## Introducción
La librería **GEEK.py** está diseñada para facilitar el control de pantallas LCD en dispositivos basados en el microcontrolador RP2040, como la Raspberry Pi Pico. Incluye funciones avanzadas para dibujar figuras, mostrar imágenes BMP y realizar operaciones de bajo nivel con el display.

Esta guía está orientada a usuarios principiantes y proporciona instrucciones claras sobre cómo empezar a usar la librería.

---

## Requisitos

### Hardware
- Microcontrolador - rp2040-GEEK de Waveshare.


- Conexiones SPI configuradas según los pines especificados:
  - **BL (Backlight)**: Pin 25
  - **DC (Data/Command)**: Pin 8
  - **CS (Chip Select)**: Pin 9
  - **SCK (Serial Clock)**: Pin 10
  - **MOSI (Master Out, Slave In)**: Pin 11
  - **RST (Reset)**: Pin 12

### Software
- MicroPython instalado en el RP2040 - GEEK.
- Librería **GEEK.py**.

---

## Instalación
1. **Descargar la librería**:
   Copia el archivo `GEEK.py` en tu dispositivo RP2040 utilizando herramientas como Thonny o cualquier editor compatible con MicroPython.

2. **Probar la configuración inicial**:
   Abre el entorno de desarrollo y escribe el siguiente código para verificar que la pantalla esté funcionando:

   ```python
   from GEEK import LCD_1inch14
   
   LCD = LCD_1inch14()
   LCD.draw_pixel(10, 10, lcd.red)  # Dibuja un pixel rojo en (10, 10)
   LCD.show()
   ```

---

## Uso de la Librería

### Inicialización de la Pantalla

Para inicializar la pantalla, crea una instancia de la clase `LCD_1inch14`:

```python
from GEEK import LCD_1inch14

LCD = LCD_1inch14()
```

### Dibujar Figuras

La librería proporciona múltiples funciones para dibujar:

#### Píxel
```python
LCD.draw_pixel(x, y, color)
```
Dibuja un píxel en la posición `(x, y)` con el color especificado.

#### Línea
```python
LCD.draw_line(x1, y1, x2, y2, color)
```
Dibuja una línea entre los puntos `(x1, y1)` y `(x2, y2)`.

#### Círculo
```python
LCD.draw_circle(x0, y0, radius, color, fill=False)
```
Dibuja un círculo con centro en `(x0, y0)` y radio `radius`. Usa `fill=True` para rellenarlo.

#### Cuadrado
```python
LCD.draw_square(x0, y0, side, color, fill=False)
```
Dibuja un cuadrado con esquina superior izquierda en `(x0, y0)` y lado de longitud `side`.

#### Rectángulo
```python
LCD.draw_rectangle(x0, y0, width, height, color, fill=False)
```
Dibuja un rectángulo con esquina superior izquierda en `(x0, y0)` y dimensiones `width` x `height`.

#### Triángulo
```python
LCD.draw_triangle(x1, y1, x2, y2, x3, y3, color, fill=False)
```
Dibuja un triángulo conectando los puntos `(x1, y1)`, `(x2, y2)` y `(x3, y3)`.

#### Forma Genérica
```python
LCD.draw_shape(points, color, fill=False)
```
Dibuja una figura definida por la lista de puntos `points`.

### Mostrar Imágenes BMP

La librería permite cargar y mostrar imágenes BMP.

```python
.drLCDaw_bmp('imagen.bmp')
```
Asegúrate de que el archivo BMP esté en la memoria del dispositivo y sea de 24 bits.

---

## Colores
Los colores deben especificarse en formato RGB565. Algunos colores predefinidos son:

- **Rojo**: `LCD.red`
- **Verde**: `LCD.green`
- **Azul**: `LCD.blue`
- **Negro**: `LCD.black`

---

## Ejemplo Completo
El siguiente ejemplo dibuja varias formas y muestra un mensaje:

```python
from GEEK import LCD_1inch14

LCD = LCD_1inch14()
LCD.fill(lcd.white)  # Limpia la pantalla con color blanco

# Dibujar formas
LCD.draw_circle(60, 60, 30, lcd.blue, fill=True)
LCD.draw_rectangle(100, 50, 50, 30, lcd.green, fill=True)
LCD.draw_triangle(150, 70, 170, 120, 130, 120, lcd.red)

# Mostrar texto (requiere función adicional para texto)
# LCD.draw_text(10, 10, "Hola Mundo", lcd.black)

LCD.show()
```

---

## Consejos
1. Usa colores en formato RGB565 para garantizar la compatibilidad.
2. Limpia la pantalla antes de dibujar nuevas figuras usando `LCD.fill(color)`.
3. Revisa las conexiones del hardware si experimentas problemas.

---

## Contribuir
Si tienes sugerencias o encuentras errores, no dudes en abrir un issue en el repositorio de la librería.

---

## Licencia
Esta librería está bajo la licencia MIT. Puedes usarla y modificarla libremente siempre y cuando incluyas la licencia original.

