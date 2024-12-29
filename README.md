intentando incluir todo lo necesario para poder controlar el RP2040-GEEK. 

Hasta ahora estoy trabajando en la parte del display, ya hay una interface novato friendly para empezar a dibujar formas , figuras y escribir texto.

He logrado corregir el temita de los colores, por algun motivo el codigo de ejemplo proporcionado por Waveshare venia con el display inicializado en BRG ( si, no es un typo, BRG, primero azul, luego rojo y luego verde) yo no se si esto fue por un error o si habia detras una intencion muy bien orquestada para dominarnos a todos, quizas sea lo segundo pero era muy incomodo trabajar con los colores asi, ademas me parecia un desperdicio de recursos tener que estar convirtiendo a nivel de bits cada vez que habia que hacer algo con los colores, entonces aqui esta, RGB como Dios manda.

TO DO LIST:
integrar un modulo para trabajar con la tarjeta SD aunque no prometo nada porque ya he estado intentandolo por todos los medios y no hay con que darle...

este dispositivo es muy vistoso pero programarlo es una pesadilla, y lo que funciona en micropython no funciona en circuitpython y se hace imposible integrar en un unico programa todo lo que el RP2040-GEEK tiene para ofrecer.

por ahora esto es lo que hay. 
me voy a poner a adaptar esto mismo para circuit python ya que alli quizas si sea posible mostrar en el display datos de la sd ... en fin...
en principio con descargar todo este paquete y subirlo a la raiz del RP2040-GEEK en micropython deberia funcionar.

En el main.py hay varios ejemplos de funciones posibles , descomenta y comenta lineas y mira lo que pasa, ademas hay un intento de documentacion mas abajo.... 
esto esta en construccion, sepan disculpar el desorden...

################################################################################################################################################################


# Librería para el Control de Pantalla en RP2040-GEEK

Esta librería ha sido desarrollada para controlar la pantalla, dibujar gráficos y escribir texto en el dispositivo RP2040-GEEK utilizando el lenguaje de programación MicroPython. A continuación, se explica el uso de cada módulo y sus funciones.

## Módulos Importados
La librería se divide en varios módulos principales:

### 1. `display`
Este módulo maneja la inicialización y configuración de la pantalla del RP2040-GEEK.

- **`init_display()`**: Inicializa el display. Debe llamarse antes de cualquier otra operación en la pantalla.
- **`fill_screen(color)`**: Llena toda la pantalla con un color dado. El color debe proporcionarse en formato RGB565.
- **`set_rotation(rotation)`**: Configura la rotación de la pantalla. Los valores posibles son 0 (normal), 1 (90 grados), 2 (180 grados) y 3 (270 grados).

### 2. `draw`
Este módulo proporciona funciones para dibujar en la pantalla, como píxeles, líneas, círculos y polígonos.

- **`draw_pixel(x, y, color)`**: Dibuja un píxel en las coordenadas `(x, y)` con el color especificado en formato RGB565.
- **`draw_line(x0, y0, x1, y1, color)`**: Dibuja una línea entre los puntos `(x0, y0)` y `(x1, y1)` con el color especificado en formato RGB565.
- **`draw_rectangle(x0, y0, x1, y1, color, filled=False)`**: Dibuja un rectángulo. Si `filled=True`, el rectángulo se rellena con el color dado.
- **`draw_circle(x, y, radius, color, filled=False)`**: Dibuja un círculo. Si `filled=True`, el círculo se rellena con el color dado.
- **`draw_polygon(color, filled=False, *vertices)`**: Dibuja un polígono usando una lista de vértices. Si `filled=True`, el polígono se rellena.

### 3. `write`
Este módulo proporciona funciones para escribir texto en la pantalla.

- **`text(x, y, text, color, bg_color, size=8)`**: Dibuja un texto en la posición `(x, y)` usando la fuente especificada. El tamaño de la fuente puede ajustarse a 8x8, 10x10 o 12x12, con un valor predeterminado de 8x8.

### 4. `image`
Este módulo permite mostrar imágenes BMP en la pantalla.

- **`show_bmp(file_path, x_offset=0, y_offset=0)`**: Muestra un archivo BMP en la pantalla. El archivo BMP debe estar en formato de 24 bits (RGB888). Los valores `x_offset` y `y_offset` permiten ajustar la posición de la imagen en la pantalla.

## Uso Básico
### Inicialización de la Pantalla
Antes de comenzar a dibujar, debemos inicializar la pantalla y configurarla:
```python
import display

# Inicializar el display
display.init_display()

# Llenar la pantalla con un color (azul en este caso)
display.fill_screen(0b0000000000011111)  # Color azul (RGB565)
```

### Configuración de Colores
Los colores deben ser especificados en formato RGB565 (5 bits para el rojo, 6 bits para el verde y 5 bits para el azul). Ejemplo:
```python
red = 0b1111100000000000    # Rojo puro
green = 0b0000011111100000  # Verde puro
blue = 0b0000000000011111   # Azul puro
yellow = 0b1111111111100000 # Amarillo
black = 0b0000000000000000  # Negro
white = 0b1111111111111111  # Blanco
```

### Dibujar en la Pantalla
Usamos el módulo `draw` para dibujar formas como píxeles, líneas, rectángulos, círculos y polígonos:
```python
import draw

# Dibujar píxeles en la pantalla
draw.draw_pixel(134, 0, red)  # Esquina superior derecha
draw.draw_pixel(120, 150, blue)  # Un punto en el medio
```

### Escribir Texto
El módulo `write` se utiliza para escribir texto en la pantalla:
```python
import write

# Escribir texto en la pantalla
write.text(10, 20, 'Hola Mundo!', white, black)
```

### Mostrar una Imagen BMP
Para mostrar una imagen BMP en la pantalla, usamos el módulo `image`:
```python
import image

# Mostrar una imagen BMP desde un archivo
image.show_bmp('/RP2040-GEEK.bmp', x_offset=0, y_offset=0)
```

## Fuentes de Texto
La librería incluye tres tamaños de fuente (8x8, 10x10 y 12x12). El tamaño de la fuente puede especificarse en la función `write.text` utilizando el parámetro `size`. El valor predeterminado es 8x8, pero puede configurarse como 10x10 o 12x12 para un texto más grande:
```python
write.text(10, 60, 'Texto 10x10', white, black, size=10)
write.text(10, 100, 'Texto 12x12', white, black, size=12)
```

## Conclusión
Esta librería permite controlar la pantalla del RP2040-GEEK de manera sencilla, ofreciendo herramientas para dibujar gráficos y mostrar texto con diferentes fuentes y tamaños. Es útil para proyectos interactivos donde se necesita una interfaz visual con gráficos y texto.

## Archivos del Proyecto
Los archivos que debes incluir en tu proyecto son:
- `display.py`: Controla la pantalla y sus configuraciones.
- `draw.py`: Funciones para dibujar en la pantalla.
- `write.py`: Funciones para escribir texto en la pantalla.
- `image.py`: Función para mostrar imágenes BMP en la pantalla.


## he incluido un ejemplo de interface interfaceUI.py


recuerda que la orientacion se configura con display.set_rotation() y acepta parametros del 0 al 4 



![IMG_1882](https://github.com/user-attachments/assets/df68ff27-4022-4d0e-901a-21abf9b9b07e)
![IMG_1881](https://github.com/user-attachments/assets/cd6c3893-b11c-4a10-a58c-c938ec3d052f)
![IMG_1879](https://github.com/user-attachments/assets/e176c2e7-3a4a-4ce4-924d-26effd9efd2a)
![IMG_1878](https://github.com/user-attachments/assets/de036cd3-ae57-4a32-ad78-3d5947d1dcdc)




¡Disfruta programando tu RP2040-GEEK!


