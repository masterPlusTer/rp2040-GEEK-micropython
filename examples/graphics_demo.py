import display, draw, write
display.init_display()
display.set_rotation(1)
display.fill_screen(0)
draw.rectangle(4,4,235,130,0x07E0)
draw.rectangle(10,40,70,90,0x001F,True)
draw.circle(125,73,25,0xF800,True)
draw.polygon(0xFFE0,True,(170,105),(204,38),(232,105))
write.text(10,12,'Graphics demo',0xFFFF,0,size=10)
