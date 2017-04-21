# g.py - globals
import pygame,utils,random

app='Shapes'; ver='1.0'
ver='1.1'
# new panel.png
# right arrow ok
ver='1.2'
# mouse move rather than green square
ver='1.3'
# mouse follows arrows
ver='1.4'
# fake cursor
ver='1.5'
# red & gold
ver='1.6'
# auto-finish

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(60*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global count,count_c,x0,y0,panel,panel_xy,wrong_cy
    global yes,no,smiley_cxy,red,gold,ms,glow,glow_c
    count=0; x0=sx(1); y0=sy(1); count_c=(sx(27.1),sy(20.5))
    wrong_cy=sy(21)
    panel=utils.load_image("panel.png",True); panel_xy=(sx(22.7),y0)
    yes=utils.load_image("yes.png",True); smiley_cxy=(sx(24),count_c[1])
    no=utils.load_image("no.png",True)
    red=utils.load_image("red.png",True)
    gold=utils.load_image("gold.png",True)
    ms=None; glow=None; glow_c=0,0
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
