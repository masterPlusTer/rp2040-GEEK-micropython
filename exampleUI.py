import display
from sd_helpers import mount_sd, get_sd_info
from interfaceUI import draw_interface   # si guardaste la función en ui.py; ajusta el import a tu archivo real

# Init display y rotación
display.init_display()
display.fill_screen(0x0000)
display.set_rotation(1)  # o la que uses

# Montar SD y recoger info
sd_info = None
try:
    sd, mp = mount_sd()                # /sd por defecto
    sd_info = get_sd_info(mp, sd_obj=sd)
except Exception as e:
    print("SD ERROR:", e)
    sd_info = None

# Pintar UI con datos de la SD
draw_interface(sd_info)
