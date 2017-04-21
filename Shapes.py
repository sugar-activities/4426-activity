#!/usr/bin/python
# Shapes.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,gtk,sys,buttons,load_save,grid

class Shapes:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((128,0,0))
        self.grid.draw()
        buttons.draw()
        g.screen.blit(g.panel,g.panel_xy)
        utils.display_number(g.count,g.count_c,g.font2,utils.CREAM)
        if self.grid.yes: utils.centre_blit(g.screen,g.yes,g.smiley_cxy)
        if self.grid.no or self.grid.count>2:
            utils.centre_blit(g.screen,g.no,g.smiley_cxy)
        if self.grid.count>0 and not self.grid.yes:
            utils.display_number(self.grid.count,(g.smiley_cxy[0],g.wrong_cy),\
                                 g.font1,utils.RED)
        if g.ms<>None: utils.centre_blit(g.screen,g.glow,g.glow_c)

    def glow(self):
        if g.ms<>None:
            if g.ms==-1: # start glow
                g.ms=pygame.time.get_ticks()
            else:
                d=pygame.time.get_ticks()-g.ms
                if d>500: # delay in ms
                    g.ms=None # turn glow off
                    g.redraw=True
        
    def do_click(self):
        return self.grid.click()

    def do_button(self,bu):
        if bu=='new': self.grid.setup()

    def do_key(self,key):
        if key==263 or key==32: self.do_button('new'); return
        if key==262 or key==275: self.grid.right(); return
        if key==260 or key==276: self.grid.left(); return
        if key==264 or key==273: self.grid.up(); return
        if key==258 or key==274: self.grid.down(); return
        if key==pygame.K_x or key==259: self.grid.do_yes(); return
        if key==pygame.K_o or key==265: self.grid.do_no(); return

    def buttons_setup(self):
        buttons.Button('new',(g.sx(29.9),g.count_c[1]))

    def flush_queue(self):
        while gtk.events_pending(): gtk.main_iteration()
        for event in pygame.event.get(): pass

    def run(self):
        g.init()
        self.grid=grid.Grid(8,8,g.sy(2.4),2,(212,212,175),utils.CREAM,g.x0,g.y0)
        if not self.journal: utils.load()
        # setup before retrieve
        self.grid.setup()
        load_save.retrieve()
        self.buttons_setup()
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    self.grid.check_mouse()
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==3:
                        g.ms=None
                        self.grid.right_click()
                    if event.button==1:
                        g.ms=None
                        if self.do_click():
                            pass
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                elif event.type == pygame.KEYDOWN:
                    g.ms=None
                    self.do_key(event.key); g.redraw=True
            if not going: break
            self.glow()
            if g.redraw:
                self.display()
                if not self.journal: # not on XO
                    if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Shapes()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
