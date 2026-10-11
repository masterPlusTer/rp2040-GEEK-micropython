"""Simple SD status screen designed for 240x135 landscape."""
import display, draw, write
WHITE=0xFFFF;BLACK=0;BLUE=0x001F;GREEN=0x07E0;RED=0xF800;YELLOW=0xFFE0

def draw_interface(sd_info=None):
    display.fill_screen(BLACK)
    draw.rectangle(0,0,display.WIDTH-1,17,BLUE,True)
    write.text(5,4,'RP2040-GEEK',WHITE,BLUE,size=8)
    if sd_info is None:
        write.text(8,30,'SD not mounted',RED,BLACK,size=10)
        return
    write.text(8,26,'SD STATUS: OK',GREEN,BLACK,size=10)
    write.text(8,43,'Size: %.1f MiB'%sd_info['capacidad_total_mb'],WHITE,BLACK,size=8)
    write.text(8,54,'Free: %.1f MiB'%sd_info['espacio_libre_mb'],WHITE,BLACK,size=8)
    write.text(8,65,'Used: %.1f MiB'%sd_info['espacio_usado_mb'],WHITE,BLACK,size=8)
    write.text(8,79,'Files:',YELLOW,BLACK,size=8)
    for i,name in enumerate(sd_info.get('archivos',[])[:4]):
        write.text(8,90+i*10,str(name)[:27],WHITE,BLACK,size=8)
