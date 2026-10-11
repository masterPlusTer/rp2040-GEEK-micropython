# ESP32-S3-GEEK MicroPython

### Una biblioteca para controlar el ESP32-S3-GEEK sin perder completamente la paciencia en el intento.

Hasta ahora he estado trabajando principalmente en la parte del display, intentando crear una interfaz *novato friendly* para empezar a dibujar formas, figuras, escribir texto y mostrar imágenes sin tener que estudiar el funcionamiento interno del ST7789 cada vez que quiero pintar un círculo.

Aunque, dicho sea de paso, recomiendo estudiarlo. Es bastante interesante.

He logrado corregir el temita de los colores. Por algún motivo, el código de ejemplo proporcionado por Waveshare venía con el display inicializado en BRG (sí, no es un typo: primero azul, luego rojo y luego verde).

Yo no sé si esto fue un error o si había detrás una intención muy bien orquestada para dominarnos a todos. Quizás sea lo segundo.

Pero era muy incómodo trabajar con los colores así. Además, me parecía un desperdicio de recursos tener que andar convirtiendo bits cada vez que quería hacer algo tan extravagante como dibujar un cuadrado rojo.

Entonces aquí está: **RGB como Dios manda.**

Este dispositivo es muy vistoso, pero programarlo puede convertirse en una pesadilla. Lo que funciona en MicroPython no necesariamente funciona en CircuitPython, y al principio parecía imposible integrar en un solo programa todo lo que el ESP32-S3-GEEK tiene para ofrecer.

Sin embargo, después de bastante experimentar, romper código, arreglarlo, volverlo a romper y descubrir nuevas formas de insultar a una tarjeta SD, hemos avanzado bastante.

**Ahora tenemos:**

- Control del display ST7789.
- Dibujo de píxeles, líneas, rectángulos, círculos y polígonos.
- Texto con tres tamaños de fuente.
- Visualización de imágenes BMP.
- Control de la tarjeta microSD mediante SPI.
- Lectura, escritura y eliminación de archivos.
- Conexión Wi-Fi y búsqueda de redes.
- Funcionalidades de Bluetooth Low Energy.
- Inicialización de ESP-NOW.
- Una aplicación principal con menús.
- Una herramienta de diagnóstico de periféricos.

Y todo esto utilizando MicroPython, sin depender de una biblioteca externa para hablar con el controlador de la microSD.

No hemos reinventado el sistema de archivos FAT, porque tampoco era necesario llegar a semejantes extremos. MicroPython ya proporciona esa parte.

---

# TO DO LIST

~~Agregar conectividad Wi-Fi.~~  
~~Agregar soporte para la tarjeta SD.~~  
~~Conseguir leer archivos desde la SD.~~  
~~Conseguir escribir archivos en la SD.~~  
~~Conseguir borrar archivos de la SD.~~  
~~Crear una herramienta de diagnóstico.~~

**Pendiente:**

- Mejorar la interfaz gráfica y la navegación con el botón BOOT.
- Seguir optimizando las primitivas gráficas.
- Incorporar un explorador de directorios completo.
- Probar comunicaciones reales entre dos dispositivos ESP-NOW.
- Desarrollar ejemplos de comunicación BLE.
- Investigar la convivencia de Wi-Fi, ESP-NOW y Bluetooth.
- Ampliar las pruebas de los GPIO, UART e I²C.
- Continuar adaptando funcionalidades para CircuitPython.
- Ordenar y documentar todo esto un poco mejor.

La microSD merece una mención especial.

En la primera versión de este repositorio escribí que quizás intentaría integrarla, aunque no prometía nada porque ya había probado de todo y no había con qué darle.

Bueno, finalmente **la desgraciada funciona**.

Y no solamente podemos listar archivos: también podemos crearlos, leerlos, comprobar que sobreviven a un reinicio y eliminarlos.

Por ahora esto sigue en construcción. Sepan disculpar el desorden, aunque sospecho que va a continuar habiendo un poco.

---

# 1. Hardware y requisitos

Este proyecto está desarrollado para el **Waveshare ESP32-S3-GEEK**, utilizando MicroPython.

La configuración actual ha sido probada con:

```text
MicroPython v1.29.0
Generic ESP32S3
ESP32-S3-GEEK
```

Otras versiones de MicroPython podrían funcionar, pero no están verificadas.

## Características utilizadas

| Componente | Uso |
|---|---|
| ESP32-S3 | Microcontrolador principal |
| ST7789 | Pantalla LCD de 240 × 135 píxeles |
| SPI | Comunicación con la pantalla y la microSD |
| MicroSD | Almacenamiento de archivos |
| Wi-Fi | Conexión y búsqueda de redes |
| BLE | Comunicación Bluetooth Low Energy |
| ESP-NOW | Comunicación inalámbrica entre dispositivos compatibles |
| BOOT | Entrada física para pruebas y futuras interfaces |
| I²C / UART | Interfaces disponibles para periféricos externos |

## Pines utilizados

### Display ST7789

| Señal | GPIO |
|---|---|
| SCK | 12 |
| MOSI | 11 |
| CS | 10 |
| DC | 8 |
| RST | 9 |

### Tarjeta microSD

| Señal | GPIO |
|---|---|
| CLK | 36 |
| MOSI | 35 |
| MISO | 37 |
| CS | 34 |

Estos son los pines utilizados por los controladores desarrollados para este proyecto.

El display y la microSD usan interfaces SPI con configuraciones diferentes, así que cada módulo debe inicializar su periférico correctamente.

---

# 2. Instalación

Antes, todos los archivos estaban amontonados en la raíz. Ahora los módulos reutilizables viven en **`/lib`**, que es donde MicroPython los busca normalmente. Un poco de orden tampoco viene mal, aunque no prometo que dure para siempre.

## Estructura del proyecto

Esta es la estructura de la versión actual del repositorio. En GitHub la carpeta raíz del proyecto contiene lo siguiente; **en la placa**, copiá la carpeta `lib` entera a `/lib` y los programas de la raíz directamente a `/`.

```text
/
├── main.py                  # Demo grafica; se ejecuta al arrancar
├── geek_app.py              # Aplicacion interactiva (REPL + ST7789)
├── exampleUI.py             # Ejemplo de interfaz
├── ESP32-S3-GEEK.bmp        # Imagen de ejemplo
├── lib/
│   ├── display.py           # Controlador ST7789
│   ├── draw.py              # Figuras y primitivas graficas
│   ├── write.py             # Texto
│   ├── image.py             # Lectura de BMP
│   ├── font_small.py
│   ├── font_medium.py
│   ├── font_large.py
│   ├── sdspi_raw.py          # Driver SD por SPI
│   ├── sd_files.py          # Archivos FAT en /sd
│   ├── connectivity.py      # Wi-Fi, BLE y ESP-NOW
│   ├── wifi_safe.py         # Wi-Fi con tiempo de espera
│   ├── geek_diagnostic.py   # Diagnostico de perifericos
│   ├── interfaceUI.py       # Modulo de interfaz experimental
│   ├── BLEandWIFIexample.py
│   ├── exampleESPNOWemisor.py
│   ├── exampleESPNOWreceptor.py
│   └── secrets.py           # SOLO ejemplo; no publicar claves reales
└── README.md                # Documentacion del repositorio
```

Los ejemplos que hoy están en `/lib` se mantienen allí para reflejar el ZIP actual; más adelante sería razonable moverlos a `examples/` dentro del repositorio. En la placa podés ejecutar cualquier ejemplo que necesites, pero no lo llames `main.py` a menos que quieras que arranque automáticamente.

## Instalación mediante Thonny

1. Instalar un firmware de MicroPython compatible con ESP32-S3 y conectar la placa por USB.
2. Seleccionar el intérprete de MicroPython en Thonny.
3. Crear `/lib` en el sistema de archivos de la placa, si todavía no existe.
4. Copiar **los archivos de `lib/` a `/lib/`** conservando sus nombres. No hace falta copiar el README ni los ejemplos para usar los controladores.
5. Copiar `geek_app.py` (y, si querés, `exampleUI.py` y la imagen BMP) a `/`.
6. Reiniciar MicroPython y ejecutar el programa que quieras.

**Ojo con `main.py`:** MicroPython lo ejecuta automáticamente al arrancar. El `main.py` de este repositorio es una demo gráfica y no un menú de selección. Si no querés ejecutarla cada vez que reiniciás, no la copies o renombrala, por ejemplo, `graphics_demo.py`.

## ¿Hay que cambiar los imports?

No, siempre que `/lib` aparezca en `sys.path`, como ocurre normalmente en MicroPython para ESP32:

```python
import sys
print(sys.path)

import display
import draw
import write
from sd_files import SDStorage

print(display.__file__)  # Esperado: /lib/display.py
```

**No guardes otra copia de `display.py` o `draw.py` en `/`:** podría cargarse primero la versión antigua y volveríamos a jugar a la ruleta de los `ImportError` y `AttributeError`.

`write.py` necesita `font_small.py`, `font_medium.py` y `font_large.py`. La imagen BMP es un **recurso**, no un módulo: si la movés a otra carpeta, cambiá su ruta al llamar a `image.show_bmp(...)`.

## Primeras pruebas

Para ejecutar la aplicación desde Thonny:

```python
import geek_app
geek_app.main()
```

Para ejecutar el diagnóstico:

```python
import geek_diagnostic
geek_diagnostic.main()
```

`geek_diagnostic.py` está dentro de `/lib`, pero se importa por su nombre normal. Su ejecución no depende de que esté en la raíz.

## Credenciales Wi-Fi

El ZIP actual incluye `lib/secrets.py` con valores de ejemplo. **No escribas ahí credenciales reales si vas a subir ese archivo a GitHub.** Conviene mantener un `secrets_example.py` público y un `secrets.py` privado, ignorado con `.gitignore`.

En los ejemplos de conexión se importa `secrets` directamente, por lo que podés colocar tu archivo privado en `/secrets.py` de la placa. Nunca publiques contraseñas reales; si ya las publicaste, cambiá la contraseña y limpiá el historial del repositorio.

---

# 3. Librería para el control de pantalla

La biblioteca permite inicializar el ST7789, configurar la orientación y escribir datos de imagen en formato RGB565.

## Módulo `display.py`

Funciones principales:

- `init_display()`: inicializa el display.
- `fill_screen(color)`: rellena la pantalla con un color.
- `set_rotation(rotation)`: configura la orientación.
- `set_active_window(x0, y0, x1, y1)`: establece una región de escritura.
- `set_window_and_write(x0, y0, x1, y1, data)`: escribe datos RGB565 en una región.

Las coordenadas comienzan en cero.

Para una orientación horizontal de 240 × 135 píxeles:

```text
X: 0 a 239
Y: 0 a 134
```

Los valores fuera de esos límites deben recortarse o descartarse antes de enviarlos al controlador.

## Inicializar el display

```python
import display

display.init_display()
display.set_rotation(3)

display.fill_screen(0x0000)
```

La rotación se configura con:

```python
display.set_rotation(0)
display.set_rotation(1)
display.set_rotation(2)
display.set_rotation(3)
```

Los valores van de `0` a `3`.

No todas las orientaciones tienen las mismas dimensiones lógicas. Hay que tenerlo presente cuando se dibuja cerca de los bordes.

---

# 4. Colores RGB565

Finalmente tenemos colores RGB como corresponde.

RGB565 utiliza 16 bits por píxel:

- 5 bits para el rojo.
- 6 bits para el verde.
- 5 bits para el azul.

Esto permite representar 65.536 colores.

Ejemplos:

```python
red    = 0xF800
green  = 0x07E0
blue   = 0x001F

yellow = 0xFFE0
cyan   = 0x07FF
purple = 0xF81F

black  = 0x0000
white  = 0xFFFF
```

También podemos expresarlos en binario:

```python
red   = 0b1111100000000000
green = 0b0000011111100000
blue  = 0b0000000000011111
```

## Convertir RGB888 a RGB565

Si tenemos colores de 8 bits por canal, podemos convertirlos así:

```python
def rgb565(r, g, b):
    return (
        ((r & 0xF8) << 8)
        | ((g & 0xFC) << 3)
        | (b >> 3)
    )
```

Ejemplo:

```python
orange = rgb565(255, 165, 0)
```

Esto sirve cuando trabajamos con colores definidos en RGB888.

No es necesario realizar esta conversión si ya tenemos el color en RGB565.

---

# 5. Módulo `draw.py`

Este es el módulo pensado para dibujar sin tener que enviar manualmente comandos al ST7789.

La idea es que un principiante pueda comenzar a experimentar inmediatamente.

## Funciones disponibles

| Función | Descripción |
|---|---|
| `pixel(x, y, color)` | Dibuja un píxel |
| `line(x0, y0, x1, y1, color)` | Dibuja una línea |
| `rectangle(x0, y0, x1, y1, color, filled=False)` | Dibuja un rectángulo |
| `circle(x, y, radius, color, filled=False)` | Dibuja un círculo |
| `polygon(color, filled=False, *vertices)` | Dibuja un polígono |

El parámetro `filled` indica si la figura debe rellenarse.

## Ejemplo completo

```python
import display
import draw

display.init_display()
display.set_rotation(3)
display.fill_screen(0x0000)

red = 0xF800
green = 0x07E0
blue = 0x001F
yellow = 0xFFE0

# Un pixel
draw.pixel(20, 20, red)

# Una linea
draw.line(0, 0, 100, 50, green)

# Rectangulo relleno
draw.rectangle(
    10, 60,
    60, 110,
    blue,
    True
)

# Circulo
draw.circle(
    120, 65,
    30,
    yellow,
    False
)

# Poligono relleno
draw.polygon(
    red,
    True,
    (160, 20),
    (220, 40),
    (190, 110)
)
```

## Correcciones realizadas

Durante la integración aparecieron algunos problemas de compatibilidad entre el módulo `display.py` y la clase `Draw`.

Por ejemplo, algunas versiones utilizaban:

```python
display.height
```

Mientras que otras exponían:

```python
display.HEIGHT
```

Esto provocaba errores al dibujar polígonos rellenos.

Se corrigió el manejo de las dimensiones para mantener la compatibilidad con ambas interfaces.

También se revisó el algoritmo de relleno de polígonos y el recorte de las figuras en los bordes de la pantalla.

Ahora el módulo puede utilizarse mediante funciones tradicionales o mediante la clase `Draw`.

La intención es conservar la API original para no obligar a reescribir todos los ejemplos anteriores.

---

# 6. Módulo `write.py`

Este módulo permite escribir texto directamente en el ST7789.

Incluye tres tamaños de fuente:

- 8 × 8 píxeles.
- 10 × 10 píxeles.
- 12 × 12 píxeles.

## Uso

```python
import display
import write

display.init_display()
display.fill_screen(0x0000)

white = 0xFFFF
black = 0x0000

write.text(
    10, 20,
    "Hola Mundo!",
    white,
    black,
    size=8
)
```

## Distintos tamaños

```python
write.text(
    10, 40,
    "Texto 10x10",
    white,
    black,
    size=10
)

write.text(
    10, 70,
    "Texto 12x12",
    white,
    black,
    size=12
)
```

## Corrección de texto fuera de pantalla

En la versión original, si un carácter quedaba fuera de los límites, el controlador podía producir un error como este:

```text
ValueError: Window outside display:
(240, 60, 249, 69)
```

Esto sucedía porque la pantalla tiene un ancho máximo de 240 píxeles y el código intentaba escribir a partir de la coordenada `240`.

Ahora `write.py` recorta automáticamente los caracteres en los bordes.

Un texto demasiado largo no provoca una excepción: simplemente se muestra la parte que entra en la pantalla.

También se añadió soporte para saltos de línea y funciones auxiliares para calcular o limitar el ancho del texto.

**Importante:** recortar un texto no significa ajustarlo automáticamente a varias líneas.

El ajuste de texto (*word wrapping*) continúa siendo una posible mejora futura.

---

# 7. Módulo `image.py`

Este módulo permite mostrar imágenes BMP de 24 bits en el ST7789.

## Ejemplo

```python
import display
import image

display.init_display()

image.show_bmp(
    "/ESP32-S3-GEEK.bmp",
    x_offset=0,
    y_offset=0
)
```

El archivo debe encontrarse en una ruta accesible desde MicroPython.

La implementación integrada procesa las imágenes por filas para reducir la necesidad de reservar memoria para la imagen completa.

Esto es especialmente útil en dispositivos con recursos limitados.

Por ahora se trabaja con el formato BMP compatible con la implementación. No es un decodificador universal de imágenes.

---

# 8. Tarjeta microSD

Esta parte merece su propia sección porque fue, durante bastante tiempo, una auténtica molestia.

Inicialmente no conseguía hacer funcionar la microSD desde MicroPython.

Podía utilizar algunas funcionalidades con CircuitPython, pero integrar todo en un único programa parecía una misión bastante absurda.

Finalmente desarrollamos un controlador específico para comunicarnos con la tarjeta mediante SPI.

## Arquitectura

El soporte de almacenamiento está dividido en dos módulos:

### `sdspi_raw.py`

Controla la comunicación de bajo nivel con la tarjeta.

Se encarga de inicializarla e intercambiar comandos y bloques de datos mediante SPI.

### `sd_files.py`

Proporciona una interfaz más sencilla para trabajar con archivos.

Utiliza el sistema de archivos FAT integrado en MicroPython, a través del controlador de bloques.

Esto significa que no estamos implementando FAT32 manualmente.

Estamos controlando el acceso a la tarjeta y dejando la gestión de archivos en manos del sistema de archivos que ya proporciona MicroPython.

## Montar la tarjeta

```python
from sd_files import SDStorage

sd = SDStorage()
sd.mount()
```

La tarjeta queda montada en `/sd`.

## Listar archivos

```python
import os

print(os.listdir("/sd"))
```

## Crear un archivo

```python
with open("/sd/hola.txt", "w") as f:
    f.write("Hola desde MicroPython!")
```

## Leerlo

```python
with open("/sd/hola.txt", "r") as f:
    print(f.read())
```

## Borrarlo

```python
import os

os.remove("/sd/hola.txt")
```

## Pruebas realizadas

El controlador fue probado físicamente en el ESP32-S3-GEEK.

Se verificó que permite:

- Inicializar y montar la tarjeta.
- Listar los archivos existentes.
- Leer archivos creados previamente con CircuitPython.
- Crear archivos nuevos.
- Leer y comprobar su contenido.
- Reiniciar MicroPython y volver a leerlos.
- Eliminar archivos.
- Verificar que fueron eliminados.

En una de las pruebas se encontraron 80 elementos en la tarjeta.

También se comprobó la lectura de archivos de texto creados originalmente desde CircuitPython.

Por ejemplo:

```text
Hola, este es el archivo 39
creado desde CircuitPython.
```

**Así que sí: finalmente la SD funciona.**

No obstante, esto no significa que todas las tarjetas SD existentes hayan sido probadas.

Todavía quedan pendientes las pruebas de estrés, el manejo de errores durante escrituras interrumpidas y la compatibilidad con distintas tarjetas.

Hacé una copia de seguridad antes de experimentar con archivos importantes.

---

# 9. Administrador de archivos

El módulo `geek_app.py` incluye un administrador básico para trabajar con los archivos de la microSD.

La versión nueva permite mostrar listados paginados tanto en la pantalla como en el REPL.

## Funcionalidades

- Mostrar la cantidad de archivos.
- Recorrer las páginas del listado.
- Seleccionar archivos mediante números.
- Leer una vista previa.
- Crear archivos de texto.
- Borrar archivos con confirmación.
- Mostrar mensajes en el display.

## Ejecutar la aplicación

```python
import geek_app

geek_app.main()
```

Desde Thonny aparece un menú similar a este:

```text
GEEK CONTROL

1 SD files
2 WiFi scan
3 Connect WiFi
4 BLE / ESP-NOW
5 Graphics
6 Diagnostic
0 Quit
```

Al elegir la opción `1`, se abre el administrador de archivos.

## Navegación

```text
N = siguiente pagina
P = pagina anterior
Numero = abrir archivo
L = listar todos
C = crear archivo
D = borrar archivo
B = volver
```

Para abrir un archivo solamente hay que escribir su número.

Ya no es necesario recordar el nombre completo.

La pantalla ST7789 muestra la página actual del listado y puede presentar una vista previa del contenido.

Por ahora los comandos se introducen desde Thonny.

El objetivo futuro es permitir la navegación mediante el botón BOOT, utilizando pulsaciones cortas y largas.

También queda pendiente implementar navegación por subdirectorios.

---

# 10. Wi-Fi

El ESP32-S3 incluye conectividad Wi-Fi.

Se incorporó una implementación con control de tiempo de espera para evitar que el programa quede bloqueado indefinidamente cuando una red no responde.

## Módulo `wifi_safe.py`

La implementación actual usa la clase `WiFi`: `connect()` recibe el timeout en **milisegundos** y devuelve la tupla de configuración de red. Ejemplo:

```python
from wifi_safe import WiFi

wifi = WiFi()
config = wifi.connect(
    "MI_RED",
    "MI_PASSWORD",
    timeout_ms=15000
)

print(config)  # Tupla IP, mascara, gateway, DNS
```

## Desconectar

```python
wifi.disconnect()
```

## Credenciales

Para los ejemplos que utilizan un archivo de configuración, se puede crear `/secrets.py` **en la placa** (sin publicarlo):

```python
WIFI_SSID = "MI_RED"
WIFI_PASSWORD = "MI_PASSWORD"
```

No publiques este archivo con tus contraseñas reales en GitHub. El `lib/secrets.py` incluido actualmente es un ejemplo, no un lugar donde convenga guardar claves que luego vas a subir al repositorio.

## Pruebas realizadas

Se verificó que el ESP32-S3-GEEK puede:

- Inicializar Wi-Fi.
- Buscar puntos de acceso.
- Detectar redes cercanas.
- Conectarse a una red.
- Obtener una dirección IP.

También se integraron controles de timeout para evitar esperas infinitas.

El manejo de todas las posibles desconexiones todavía necesita más pruebas.

---

# 11. Bluetooth Low Energy

El ESP32-S3 dispone de Bluetooth Low Energy, o BLE.

MicroPython proporciona acceso a esta funcionalidad mediante el módulo `bluetooth`.

## Ejemplo básico

```python
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

print("BLE:", ble.active())
```

Esto inicializa la pila Bluetooth.

**Pero inicializar BLE no es lo mismo que comprobar una conexión real.**

En las pruebas de diagnóstico conseguimos realizar una búsqueda BLE y recibir 77 anuncios de dispositivos cercanos.

Esto confirma que el dispositivo puede recibir anuncios BLE.

Quedan pendientes ejemplos completos de:

- Servicios GATT.
- Características.
- Lectura y escritura.
- Notificaciones.
- Conexión entre dispositivos.

No hay que confundir BLE con Bluetooth Classic. El ESP32-S3 no ofrece Bluetooth Classic.

---

# 12. ESP-NOW

ESP-NOW es un protocolo de comunicación inalámbrica utilizado por dispositivos Espressif.

Permite intercambiar mensajes entre dispositivos compatibles sin necesidad de establecer una conexión TCP/IP convencional.

Es especialmente interesante para sensores, controles remotos y proyectos con varios microcontroladores.

## Ejemplo de inicialización

```python
import network
import espnow

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

print("ESP-NOW inicializado")
```

## Limitaciones importantes

Wi-Fi y ESP-NOW utilizan la radio de 2,4 GHz del ESP32-S3.

Esto no significa que sean incompatibles ni que resulte imposible utilizarlos simultáneamente.

Sin embargo, **hay que prestar especial atención a la configuración del canal**.

Cuando el dispositivo está conectado a un punto de acceso Wi-Fi, el canal de esa conexión condiciona las comunicaciones ESP-NOW.

También resulta posible combinar funcionalidades Wi-Fi, BLE y ESP-NOW, pero hay que tener en cuenta la coexistencia de radio y las limitaciones del firmware.

No voy a prometer que todo funciona simultáneamente en cualquier combinación, porque todavía estamos probándolo.

## Estado actual

Se comprobó que ESP-NOW puede inicializarse correctamente desde MicroPython.

Todavía falta verificar el envío y recepción de mensajes entre dos placas.

Así que, por ahora:

**ESP-NOW inicializa. La comunicación real sigue pendiente.**

---

# 13. Diagnóstico de hardware

Se añadió `geek_diagnostic.py`, una pequeña herramienta para comprobar los subsistemas principales del dispositivo.

## Ejecutar

```python
import geek_diagnostic

geek_diagnostic.main()
```

La aplicación muestra resultados en el REPL y utiliza el display para algunas pruebas visuales.

## Funciones verificadas

| Prueba | Resultado observado |
|---|---|
| Display ST7789 | Secuencia gráfica ejecutada |
| Memoria | Aproximadamente 1,9 MiB de heap libre |
| Botón BOOT | Pulsación detectada |
| MicroSD | Lectura, escritura y borrado correctos |
| Wi-Fi | Búsqueda y conexión correctas |
| BLE | Recepción de anuncios |
| ESP-NOW | Inicialización correcta |
| I²C / UART | Pendiente de pruebas con hardware externo |

Uno de los diagnósticos devolvió:

```text
SYSTEM : OK 1910 KB
BOOT BTN : OK pressed
SD R/W/DEL : OK 80 items
WIFI : OK 192.168.2.90
BLE SCAN : OK 77 ads
ESP NOW : OK init only
I2C/UART : SKIP no device
```

La dirección IP corresponde a la red utilizada durante esa prueba. No es una dirección fija del dispositivo.

**Estas pruebas no garantizan que todos los periféricos funcionen en cualquier circunstancia.**

Algunas verifican operaciones completas y otras solamente inicialización.

Por ejemplo, el envío real de paquetes ESP-NOW continúa pendiente.

---

# 14. Ejemplo gráfico completo

Este ejemplo combina inicialización, dibujo y escritura de texto.

```python
import display
import draw
import write

BLACK = 0x0000
WHITE = 0xFFFF
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
YELLOW = 0xFFE0

display.init_display()
display.set_rotation(3)
display.fill_screen(BLACK)

# Titulo
write.text(
    5, 5,
    "ESP32-S3-GEEK",
    WHITE,
    BLACK,
    size=10
)

# Rectangulo
draw.rectangle(
    5, 30,
    65, 75,
    RED,
    True
)

# Circulo
draw.circle(
    110, 70,
    28,
    GREEN,
    False
)

# Triangulo
draw.polygon(
    BLUE,
    True,
    (160, 35),
    (230, 60),
    (190, 110)
)

# Texto inferior
write.text(
    5, 120,
    "Hello MicroPython!",
    YELLOW,
    BLACK,
    size=8
)
```

No hace falta crear un framebuffer enorme ni estudiar todo el protocolo del ST7789 para comenzar a dibujar.

Naturalmente, si después querés entender cómo funciona, el código está ahí para leerlo.

Esa es justamente la idea.

---

# 15. Problemas conocidos y soluciones

## `ImportError: no module named 'write'`

El archivo `write.py` no se encuentra en la ruta de importación de MicroPython.

Verificar que esté guardado en `/lib` en la placa, junto con:

```text
font_small.py
font_medium.py
font_large.py
```

## `AttributeError: 'module' object has no attribute 'height'`

Este error apareció por una incompatibilidad entre las interfaces de `draw.py` y `display.py`.

Se corrigió el acceso a las dimensiones de la pantalla.

Utilizar versiones compatibles de ambos archivos.

## `ValueError: Window outside display`

Ocurría cuando el código intentaba escribir fuera de los límites del ST7789.

El módulo `write.py` fue modificado para recortar los caracteres que exceden los bordes.

Las coordenadas válidas dependen de la orientación configurada.

## No aparecen los archivos de la SD en pantalla

Las primeras versiones del administrador mostraban solamente el número de archivos en el display y los nombres completos en Thonny.

La interfaz posterior añade un listado paginado en pantalla.

Para seleccionar archivos todavía se utiliza el REPL.

## La SD no monta

Revisar:

- Que la tarjeta esté correctamente insertada.
- Que el controlador esté copiado a la placa.
- Que los pines SPI sean correctos.
- Que la tarjeta tenga un sistema de archivos FAT compatible.
- Que ningún otro programa esté utilizando simultáneamente el periférico de forma incompatible.

No formatees una tarjeta que contiene información importante sin antes guardar una copia de seguridad.

## Wi-Fi no conecta

Comprobar SSID, contraseña, cobertura y compatibilidad de la red.

El ESP32-S3 utiliza Wi-Fi de 2,4 GHz.

Utilizar un timeout para evitar que el programa espere indefinidamente.

## `ImportError` tras mover los archivos a `/lib`

Comprobá `sys.path` y confirmá que `/lib` está incluida. Revisá que no hayan quedado archivos duplicados en la raíz y reiniciá MicroPython después de mover los módulos.

## `MemoryError`

No todas las operaciones tienen las mismas necesidades de memoria.

Evitar cargar imágenes o archivos grandes enteros cuando pueden procesarse por partes.

Se recomienda utilizar lecturas parciales y liberar objetos temporales cuando dejan de ser necesarios.

---

# 16. Filosofía del proyecto

Mi intención no es crear una biblioteca gigantesca con veinte dependencias para poder dibujar una línea.

Quiero algo sencillo, comprensible y que se pueda modificar.

Una biblioteca que permita utilizar el ESP32-S3-GEEK sin tener que empezar desde cero, pero que al mismo tiempo deje ver cómo funciona todo.

Si quiero dibujar un círculo, quiero poder dibujarlo.

Y si mañana quiero abrir `draw.py` para entender el algoritmo, también quiero poder hacerlo.

Lo mismo con la tarjeta SD.

En lugar de esconder toda la comunicación detrás de una biblioteca externa, tenemos nuestro propio controlador SPI, y podemos estudiar qué ocurre cuando el microcontrolador inicializa la tarjeta, lee un sector o escribe datos.

Eso para mí es parte de la diversión.

**Este proyecto sigue siendo experimental.**

Hay funciones que están probadas en hardware real, otras que necesitan más pruebas y algunas que todavía están en desarrollo.

No prometo que todo funcione siempre, pero al menos ahora, cuando algo no funciona, tenemos mejores herramientas para averiguar por qué.

Y considerando cómo empezó todo esto, ya es bastante.

---

# 17. Conclusión

Empecé intentando controlar una pequeña pantalla.

Después quise dibujar figuras.

Después escribir texto.

Después mostrar imágenes.

Después apareció el problema de la microSD.

Y ahora resulta que estamos trabajando con Wi-Fi, BLE, ESP-NOW, controladores SPI y un pequeño administrador de archivos.

En algún momento habrá que decidir dónde termina esto, aunque sospecho que todavía falta bastante.

Por ahora, **el ESP32-S3-GEEK funciona con MicroPython y ya podemos aprovechar una buena parte de su hardware desde una sola aplicación**.

El resto sigue en construcción.

Se aceptan sugerencias, correcciones y contribuciones.

Y si encuentran alguna conspiración internacional relacionada con el orden BRG de los colores, por favor avisen.

Quiero saber si finalmente teníamos razón.



![IMG_1882](https://github.com/user-attachments/assets/df68ff27-4022-4d0e-901a-21abf9b9b07e)
![IMG_1881](https://github.com/user-attachments/assets/cd6c3893-b11c-4a10-a58c-c938ec3d052f)
![IMG_1879](https://github.com/user-attachments/assets/e176c2e7-3a4a-4ce4-924d-26effd9efd2a)
![IMG_1878](https://github.com/user-attachments/assets/de036cd3-ae57-4a32-ad78-3d5947d1dcdc)




¡Disfruta programando tu RP2040-GEEK!


