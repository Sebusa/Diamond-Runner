import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (pos['x'], pos['y'], self.image.get_width(), self.image.get_height())
        self.x = pos['x']
        self.y = pos['y']
        self.speed = {'x': 0, 'y': 0, 'max': 5, 'momentum': 0.5}
        self.HEALTH = 6

    def update(self):
        self.x += 0
        self.y += 0
        self.rect.center = (self.x, self.y)