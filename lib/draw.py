"""Primitive graphics using the bundled display driver, no dependencies."""
import display

def pixel(x,y,color):
    display.pixel(x,y,color)

def line(x1,y1,x0,y0,color):
    """Original API argument order retained (end point, start point)."""
    x0=int(x0);y0=int(y0);x1=int(x1);y1=int(y1)
    if y0 == y1:
        display.fill_rect(x0,y0,x1,y1,color);return
    if x0 == x1:
        display.fill_rect(x0,y0,x1,y1,color);return
    dx=abs(x1-x0);dy=abs(y1-y0)
    sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1
    err=dx-dy
    while True:
        pixel(x0,y0,color)
        if x0==x1 and y0==y1: break
        e2=err*2
        if e2 > -dy: err-=dy;x0+=sx
        if e2 < dx: err+=dx;y0+=sy

def rectangle(x0,y0,x1,y1,color,filled=False):
    if filled:
        display.fill_rect(x0,y0,x1,y1,color)
    else:
        line(x0,y0,x1,y0,color)
        line(x0,y1,x1,y1,color)
        line(x0,y0,x0,y1,color)
        line(x1,y0,x1,y1,color)

def circle(x0,y0,radius,color,filled=False):
    x0=int(x0);y0=int(y0);r=int(radius)
    if r<0: raise ValueError('negative radius')
    x=r;y=0;err=1-r
    while x>=y:
        if filled:
            display.fill_rect(x0-x,y0+y,x0+x,y0+y,color)
            display.fill_rect(x0-x,y0-y,x0+x,y0-y,color)
            display.fill_rect(x0-y,y0+x,x0+y,y0+x,color)
            display.fill_rect(x0-y,y0-x,x0+y,y0-x,color)
        else:
            for xx,yy in ((x,y),(-x,y),(x,-y),(-x,-y),(y,x),(-y,x),(y,-x),(-y,-x)):
                pixel(x0+xx,y0+yy,color)
        y+=1
        if err<0:err+=2*y+1
        else:x-=1;err+=2*(y-x)+1

def polygon(color,filled=False,*vertices):
    if len(vertices)<3: raise ValueError('at least 3 vertices required')
    if not filled:
        for i in range(len(vertices)):
            ax,ay=vertices[i]; bx,by=vertices[(i+1)%len(vertices)]
            line(ax,ay,bx,by,color)
        return
    low=max(0,min(v[1] for v in vertices))
    high=min(display.HEIGHT-1,max(v[1] for v in vertices))
    for y in range(low,high+1):
        intersections=[]
        for i in range(len(vertices)):
            x1,y1=vertices[i];x2,y2=vertices[(i+1)%len(vertices)]
            if y1==y2:continue
            if (y1<=y<y2) or (y2<=y<y1):
                intersections.append(x1+(y-y1)*(x2-x1)/(y2-y1))
        intersections.sort()
        for i in range(0,len(intersections)-1,2):
            a=int(intersections[i]+0.999999)
            b=int(intersections[i+1])
            if a<=b:display.fill_rect(a,y,b,y,color)
