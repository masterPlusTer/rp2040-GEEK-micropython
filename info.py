import board
import digitalio
import time
import gc
import os

# Información de la memoria
def memory_info():
    free_memory = gc.mem_free()
    total_memory = gc.mem_alloc() + gc.mem_free()
    return {
        'free_memory_kb': free_memory / 1024,
        'total_memory_kb': total_memory / 1024
    }

# Información de la memoria flash
def flash_info():
    flash_size_mb = 4  # Tamaño correcto de la memoria flash para tu placa
    return {
        'flash_size_mb': flash_size_mb
    }

# Información de la frecuencia del CPU
def clock_info():
    return {
        'cpu_frequency': 'No disponible'
    }

# Información de temperatura
def temperature_info():
    return {'temperature_celsius': 'No disponible'}

# Información del voltaje de entrada
def read_vsys():
    return {'voltage_vsys': 'No disponible'}

# Tiempo de ejecución
def uptime_info():
    return {'uptime_seconds': time.monotonic()}

# Información de RTC
def rtc_info():
    return {
        'rtc_year': 'No disponible',
        'rtc_month': 'No disponible',
        'rtc_day': 'No disponible',
        'rtc_hour': 'No disponible',
        'rtc_minute': 'No disponible',
        'rtc_second': 'No disponible',
        'rtc_datetime': 'No disponible'
    }

# Información del firmware del RP2040
def rp2040_firmware_info():
    return {'rp2040_firmware': 'CircuitPython'}

# Información de la batería
def battery_info():
    return {'battery_level': 'No disponible'}

# Información de interrupciones
def interrupt_info():
    return {'interrupt_count': 0}

# Información del sistema de archivos
def filesystem_info():
    fs_info = os.statvfs('/')
    total_size = fs_info[0] * fs_info[1]  # Tamaño total del sistema de archivos
    free_size = fs_info[0] * fs_info[3]   # Espacio libre en el sistema de archivos
    used_size = total_size - free_size   # Espacio usado en el sistema de archivos
    return {
        'fs_total': total_size,
        'fs_free': free_size,
        'fs_used': used_size
    }

# Información del chip
def chip_info():
    return {'chip_id': 'No disponible'}

# Información del estado de los pines
def pin_info():
    return {'pin_info': 'No disponible'}

# Uso de almacenamiento por directorio
def storage_usage_info():
    files = os.listdir('/')
    return {'number_of_files': len(files)}

# Listar todos los archivos en el directorio raíz y sus tamaños
def list_files():
    files = os.listdir('/')
    for file in files:
        try:
            # Para obtener el tamaño del archivo, usamos os.stat() y verificamos el índice correcto
            file_stat = os.stat(file)
            size = file_stat[6]  # Tamaño del archivo
            print(f"Archivo: {file}, Tamaño: {size / (1024):.2f} KB")
        except Exception as e:
            print(f"No se pudo obtener el tamaño de {file}: {e}")

# Obtener información general del sistema
def system_info():
    info = {
        'board': board.board_id,
        'version': 'CircuitPython',
        'frequency': clock_info()['cpu_frequency'],
        'memory': memory_info(),
        'flash': flash_info(),
        'temperature': temperature_info(),
        'voltage': read_vsys(),
        'uptime': uptime_info(),
        'rtc': rtc_info(),
        'rp2040_firmware': rp2040_firmware_info(),
        'battery': battery_info(),
        'interrupt': interrupt_info(),
        'filesystem': filesystem_info(),
        'chip': chip_info(),
        'pins': pin_info(),
        'storage_usage': storage_usage_info()
    }
    return info

# Imprimir información del sistema
def print_system_info_extended():
    info = system_info()
    
    print("Sistema CircuitPython:")
    print(f"Placa: {info['board']}")
    print(f"Versión de CircuitPython: {info['version']}")
    print(f"Frecuencia del CPU: {info['frequency']}")
    
    print("Información de memoria RAM:")
    print(f"Memoria libre: {info['memory']['free_memory_kb']:.2f} KB")
    print(f"Memoria total: {info['memory']['total_memory_kb']:.2f} KB")
    
    print("Información de la memoria flash:")
    print(f"Tamaño de flash: {info['flash']['flash_size_mb']:.2f} MB")
    
    print("Información de temperatura:")
    print(f"Temperatura: {info['temperature']['temperature_celsius']}")
    
    print("Voltaje de entrada:")
    print(f"Voltaje Vsys: {info['voltage']['voltage_vsys']}")
    
    print("Tiempo de ejecución:")
    print(f"Uptime: {info['uptime']['uptime_seconds']:.2f} segundos")
    
    print("RTC:")
    print(f"Fecha y hora: {info['rtc']['rtc_datetime']}")
    print(f"Año: {info['rtc']['rtc_year']}")
    print(f"Mes: {info['rtc']['rtc_month']}")
    print(f"Día: {info['rtc']['rtc_day']}")
    print(f"Hora: {info['rtc']['rtc_hour']}")
    print(f"Minuto: {info['rtc']['rtc_minute']}")
    print(f"Segundo: {info['rtc']['rtc_second']}")
    
    print("Firmware del RP2040:")
    print(f"Firmware RP2040: {info['rp2040_firmware']}")
    
    print("Información de la batería:")
    print(f"Nivel de batería: {info['battery']['battery_level']}")
    
    print("Información de interrupciones:")
    print(f"Conteo de interrupciones: {info['interrupt']['interrupt_count']}")
    
    print("Sistema de archivos:")
    print(f"Tamaño total del FS: {info['filesystem']['fs_total'] / (1024 * 1024):.2f} MB")
    print(f"Espacio libre en el FS: {info['filesystem']['fs_free'] / (1024 * 1024):.2f} MB")
    print(f"Espacio usado en el FS: {info['filesystem']['fs_used'] / (1024 * 1024):.2f} MB")
    
    print("Información del chip:")
    print(f"Chip ID: {info['chip']['chip_id']}")
    
    print("Información de los pines:")
    print(info['pins'])
    
    print("Uso de almacenamiento por directorio:")
    print(f"Número de archivos: {info['storage_usage']['number_of_files']}")
    
    print("Detalles de los archivos:")
    list_files()

# Ejecutar la impresión de información extendida del sistema
print_system_info_extended()
