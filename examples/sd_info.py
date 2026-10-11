from sd_helpers import mount_sd, get_sd_info
from interfaceUI import draw_interface
import display
display.init_display()
display.set_rotation(1)
try:
    sd,where=mount_sd()
    data=get_sd_info(where,sd)
    print(data)
    draw_interface(data)
except OSError as error:
    print('SD error:',error)
    draw_interface(None)
