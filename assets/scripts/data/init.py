import pygame as pg
import sys
from .Globals import *

def main():
    pg.init()

    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # Fullscreen

    while True:

        # Event handling
        for event in pg.event.get():

            # Controls
            if event.type == pg.KEYDOWN:
                pass

            if event.type == pg.KEYUP:
                pass

            # Quit
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == ESCAPE):
                pg.quit()
                sys.exit()

        screen.fill(BG)
        pg.display.update()
        CLOCK.tick(60)
