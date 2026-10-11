"""RGB565 bitmap text with lazily loaded bundled fonts."""
import display
_FONTS = {8:('font_small','font_8x8'),10:('font_medium','font_10x10'),
          12:('font_large','font_12x12'),20:('font_xlarge','font_20x20')}
_current_size = None
_current_font = None

def _font(size):
    global _current_size,_current_font
    if size not in _FONTS: raise ValueError('font size must be 8, 10, 12 or 20')
    if _current_size != size:
        module_name,attr = _FONTS[size]
        module = __import__(module_name)
        _current_font = getattr(module,attr)
        _current_size = size
    return _current_font

def draw_char(x,y,char,color,bg_color,size=8):
    font=_font(size)
    bitmap=font.get(char)
    if bitmap is None:return
    buf=bytearray(size*size*2)
    for r,row in enumerate(bitmap):
        for c in range(size):
            rgb=color if row & (1 << (size-1-c)) else bg_color
            i=2*(r*size+c)
            buf[i]=(rgb>>8)&255;buf[i+1]=rgb&255
    display.set_window_and_write(x,y,x+size-1,y+size-1,buf)

def text(x,y,text,color,bg_color,size=8):
    _font(size)
    for i,ch in enumerate(str(text)):
        x0=x+i*size
        if x0 >= display.WIDTH:break
        if x0+size<=0:continue
        draw_char(x0,y,ch,color,bg_color,size)
