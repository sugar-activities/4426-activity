# grid.py
import pygame,g,utils,random

imgs=[None]
squares=[]
# 0=empty, 1-5=shapes, 6=blue
shapes=[[(0,0,6,0,0),(0,1,5,2,0),(6,5,5,5,6),(0,3,5,4,0),(0,0,6,0,0)],\
        [(0,1,2,0),(1,5,5,2),(0,6,6,0)],\
        [(0,6,0),(1,5,2),(3,5,4),(0,6,0)],\
        [(1,2),(3,4)]]
row_ns=[]
col_ns=[]

class Square:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.v=0; self.visible=False

class RowN:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.n=0

class ColN:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.n=0

class Grid:
    def __init__(self,nr,nc,side,px,colr,bgd,x0,y0):
        self.x=x0; self.y=y0; self.nr=nr; self.nc=nc; self.side=side
        self.total=nr*nc
        w=nc*side+px; h=nr*side+px
        self.base=pygame.Surface((w,h))
        self.base.fill(bgd)
        self.top=pygame.Surface((w,h))
        self.top.set_colorkey((0,0,0))
        x1=0; x2=x1+w; y=0
        for r in range(nr+1):
            pygame.draw.line(self.top,colr,(x1,y),(x2,y),px)
            y+=side
        x=0; y1=0; y2=y1+h
        for c in range(nc+1):
            pygame.draw.line(self.top,colr,(x,y1),(x,y2),px)
            x+=side
        for i in range(1,7):
            img=utils.load_image(str(i)+'.png'); imgs.append(img)
        y=y0+px/2
        for r in range(nr):
            x=x0+px/2
            for c in range(nc):
                sq=Square(x,y); squares.append(sq)
                x+=side
            rn=RowN(x+g.sy(.3),y+side/2); row_ns.append(rn)
            y+=side
        x=x0+side/2; y+=side/2-g.sy(.3)
        for c in range(nc):
            cn=ColN(x,y); col_ns.append(cn)
            x+=side

    def setup(self):
        for sq in squares: sq.visible=False
        if not self.place_shapes(): utils.exit()
        ind=0
        for r in range(self.nr):
            n=0
            for c in range(self.nc):
                v=self.square(r,c).v
                if v>0 and v<6: n+=1
            row_ns[ind].n=n; ind+=1
            if n==0:
                for c in range(self.nc):
                    sq=self.square(r,c); sq.v=6; sq.visible=True
        ind=0
        for c in range(self.nc):
            n=0
            for r in range(self.nr):
                v=self.square(r,c).v
                if v>0 and v<6: n+=1
            col_ns[ind].n=n; ind+=1
            if n==0:
                for r in range(self.nr):
                    sq=self.square(r,c); sq.v=6; sq.visible=True
        self.count=0; self.finished=False; self.no=False; self.yes=False
        self.green=squares[0]
        self.set_mouse()
        
    def draw(self):
        g.screen.blit(self.base,(self.x,self.y))
        for sq in squares:
            if sq.visible:
                v=sq.v
                if v==0: v=6
                g.screen.blit(imgs[v],(sq.x,sq.y))
        colr=utils.CYAN
        g.screen.blit(self.top,(self.x,self.y))
        for rn in row_ns:
            utils.display_number1(rn.n,(rn.x,rn.y),g.font1,colr)
        for cn in col_ns:
            utils.display_number(cn.n,(cn.x,cn.y),g.font1,colr)
        if not self.complete() and g.ms==None:
            sq=self.green
            pygame.draw.rect(g.screen,utils.GREEN,\
                             (sq.x,sq.y,self.side,self.side),8)

    def set_mouse(self):
        sq=self.green
        pygame.mouse.set_pos((sq.x+self.side/2,sq.y+self.side/2))
        
    def check_mouse(self):
        for sq in squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+self.side,sq.y+self.side):
                self.green=sq; return

    def click(self):
        self.no=False
        for sq in squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+self.side,sq.y+self.side):
                if not sq.visible:
                    d=self.side/2; g.glow_c=sq.x+d,sq.y+d; g.ms=-1; g.glow=g.red
                    sq.visible=True
                    if sq.v==0 or sq.v==6: self.count+=1; self.no=True
                    else: g.glow=g.gold
                return True
        return False
    
    def do_yes(self):
        self.no=False
        sq=self.green
        if not sq.visible:
            d=self.side/2; g.glow_c=sq.x+d,sq.y+d; g.ms=-1; g.glow=g.red
            sq.visible=True
            if sq.v==0 or sq.v==6: self.count+=1; self.no=True
            else: g.glow=g.gold
        
    def right_click(self):
        self.no=False
        for sq in squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+self.side,sq.y+self.side):
                if not sq.visible:
                    d=self.side/2; g.glow_c=sq.x+d,sq.y+d; g.ms=-1; g.glow=g.red
                    sq.visible=True
                    if sq.v>0 and sq.v<6: self.count+=1; self.no=True
                    else: g.glow=g.gold
                return True
        return False
    
    def do_no(self):
        self.no=False
        sq=self.green
        if not sq.visible:
            d=self.side/2; g.glow_c=sq.x+d,sq.y+d; g.ms=-1; g.glow=g.red
            sq.visible=True
            if sq.v>0 and sq.v<6: self.count+=1; self.no=True
            else: g.glow=g.gold
        
    def place_shapes(self):
        for i in range(1000):
            ok=True
            for sq in squares: sq.v=0
            for ind in range(len(shapes)):
                if not self.place_shape(shapes[ind]):
                    ok=False; break
            if ok: return True
        return False
        
    def place_shape(self,shape): # eg [(1,2),(3,4)]
        h=len(shape); w=len(shape[0])
        for i in range(1000):
            r0=random.randint(0,self.nr-h)
            c0=random.randint(0,self.nc-w)
            if self.free(r0,c0,h,w):
                ind1=0
                for r in range(r0,r0+h):
                    row=shape[ind1]; ind2=0
                    for c in range(c0,c0+w):
                        self.square(r,c).v=row[ind2]
                        ind2+=1
                    ind1+=1
                return True
        return False

    def free(self,r0,c0,h,w):
        for r in range(r0,r0+h):
            for c in range(c0,c0+w):
                if self.square(r,c).v>0: return False
        return True

    def square(self,r0,c0):
        ind=0
        for r in range(self.nr):
            for c in range(self.nc):
                if r==r0 and c==c0: return squares[ind]
                ind+=1

    def row_col_ind(self,sq):
        ind=0
        for r in range(self.nr):
            for c in range(self.nc):
                if squares[ind]==sq: return (r,c)
                ind+=1

    def right(self):
        sq=self.green; r,c=self.row_col_ind(sq)
        c+=1
        if c==self.nc: c=0
        self.green=self.square(r,c)
        self.set_mouse()
    
    def left(self):
        sq=self.green; r,c=self.row_col_ind(sq)
        c-=1
        if c<0: c=self.nc-1
        self.green=self.square(r,c)
        self.set_mouse()
    
    def down(self):
        sq=self.green; r,c=self.row_col_ind(sq)
        r+=1
        if r==self.nr: r=0
        self.green=self.square(r,c)
        self.set_mouse()
    
    def up(self):
        sq=self.green; r,c=self.row_col_ind(sq)
        r-=1
        if r<0: r=self.nr-1
        self.green=self.square(r,c)
        self.set_mouse()
    
    def complete(self):
        if self.finished: return True
        n=0
        for sq in squares:
            if sq.visible:
                if sq.v>0 and sq.v<6: n+=1
        if n<25: return False
        for sq in squares: sq.visible=True # show any outstanding blue
        self.finished=True
        if self.count<3: g.count+=1; self.no=False; self.yes=True
        return True

    
        
            
