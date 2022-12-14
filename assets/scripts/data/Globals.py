import pygame as pg

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CLOCK = pg.time.Clock()

# Tiles
TILESIZE = 64
GRIDWIDTH = SCREEN_WIDTH / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE

# Colors
BLACK = (30, 36, 36)
WHITE = (250, 250, 250)
BG = (1, 23, 33, 1)

# Key bindings
UP = pg.K_w
DOWN = pg.K_s
LEFT = pg.K_a
RIGHT = pg.K_d
SPACE = pg.K_SPACE
ESCAPE = pg.K_ESCAPE

SHOOT = pg.mouse.get_pressed()

# Player