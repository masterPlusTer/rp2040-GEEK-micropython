import display, image
display.init_display()
display.set_rotation(1)
display.fill_screen(0)
# Copy assets/RP2040-GEEK.bmp to /RP2040-GEEK.bmp on the board first.
image.show_bmp('/RP2040-GEEK.bmp')
