import sys
import os
import random
import board
import adafruit_sdcard
import storage
import busio
import digitalio



#brillo del display




valor = str(random.randint(10, 100))


# playing with adafruit_sdcard, storage, os y other modules


# Configurar los pines para la interfaz SPI
sck = board.SD_SCK  # Pin para el reloj (SCK)
mosi = board.SD_MOSI  # Pin para MOSI
miso = board.SD_MISO  # Pin para MISO
cs = board.SD_CS  # Pin para el chip select (CS)


# Connect to the card and mount the filesystem.
spi = busio.SPI(sck, mosi, miso)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
sys.path.append("/sd")
sys.path.append("/sd/lib")


# Obtener información sobre el sistema de archivos de la tarjeta SD
statvfs = os.statvfs("/sd")
# Acceder a los valores utilizando índices
block_size = statvfs[0]
fragment_size = statvfs[1]
total_blocks = statvfs[2]
free_blocks = statvfs[3]
available_blocks = statvfs[4]
reserved_blocks = statvfs[5]
free_inodes = statvfs[6]
total_inodes = statvfs[7]
filesystem_id = statvfs[8]

# Calcular el tamaño total en gigabytes
total_size = (block_size * total_blocks) / (1024 ** 3)

# Calcular el espacio libre en gigabytes
free_size = (block_size * available_blocks) / (1024 ** 3)

# Calcular el espacio utilizado en gigabytes
used_size = total_size - free_size

# Imprimir información
print("Tamaño total de la tarjeta SD:", round(total_size, 5), "GB")
print("Espacio libre en la tarjeta SD:", round(free_size, 5), "GB")
# Convertir a megabytes si el tamaño es pequeño
if used_size < 1:
    used_size_mb = used_size * 1024
    print("Espacio utilizado en la tarjeta SD:", round(used_size_mb, 2), "MB")
else:
    print("Espacio utilizado en la tarjeta SD:", round(used_size, 2), "GB")
# Escribir datos en un archivo de texto en la tarjeta SD

cantidad = str(len(os.listdir("/sd")))


def escribir_archivo():
    # Abrir el archivo en modo escritura
    archivo = open("/sd/archivo" + valor + ".txt", "w")

    # Escribir datos en el archivo
    archivo.write("¡Hola, mundo!")
    archivo.write(
        "\nEste es un ejemplo de escritura en archivo"
        + valor
        + ".txt en la tarjeta SD."
    )
    archivo.write(
        "\n en este momento hay aproximadamente "
        + cantidad
        + " archivos en este directorio"
    )

    # Cerrar el archivo
    archivo.close()


# Leer datos de un archivo de texto en la tarjeta SD
def leer_archivo():
    # Abrir el archivo en modo lectura
    archivo = open("/sd/archivo" + valor + ".txt", "r")

    # Leer el contenido del archivo
    contenido = archivo.read()

    # Cerrar el archivo
    archivo.close()

    # Imprimir el contenido del archivo
    print("Contenido del archivo:")
    print(contenido)


# Llamar a las funciones para escribir y leer el archivo
escribir_archivo()
leer_archivo()


def listar_archivos():
    directorio = "/sd"  # Ruta del directorio en la tarjeta SD

    # Obtener la lista de archivos en el directorio
    archivos = os.listdir("/sd").pop()

    # Imprimir la lista de archivos
    print("Se acaba de crear el siguiente archivo en ", directorio + ":")

    print(archivos)

    print("\n En el directorio hay aproximadamente " + cantidad + " archivos")


# Llamar a la función para listar los archivos
listar_archivos()


# Escribe tu código aquíimport os


def abrir_archivo(nombre_archivo):
    ruta_archivo = "/sd/" + nombre_archivo

    # Verificar si el archivo existe
    """if not os.path.exists(ruta_archivo):
        print("Elarchivo no existe.")
        return"""

    # Leer el contenido del archivo
    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.read()

    # Imprimir el contenido actual del archivo
    print("Contenido actual del archivo:")
    print(contenido)

    # Solicitar al usuario que ingrese el nuevo contenido
    nuevo_contenido = input("Ingrese el nuevo contenido del archivo: ")

    # Escribir el nuevo contenido en el archivo
    with open(ruta_archivo, "w") as archivo:
        archivo.write(nuevo_contenido)

    print("El archivo se ha actualizado correctamente.")


# Llamar a la función para abrir un archivo existente y editar su contenido
nombre_archivo = input("Ingrese el nombre del archivo a editar: ")
abrir_archivo(nombre_archivo)
# Escribe tu código aquí :-)
