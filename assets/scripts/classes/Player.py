import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
        self.width = width
        self.height = height
        self.jump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.rect.x + 17, self.rect.y + 11, 29, 52)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.rect.x, self.rect.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.rect.x, self.rect.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.rect.x, self.rect.y))
                else:
                    win.blit(walkLeft[0], (self.rect.x, self.rect.y))
            self.hitbox = (self.rect.x + 17, self.rect.y + 11, 29, 52)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > self.vel:
            self.rect.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.rect.x < 500 - self.width - self.vel:
            self.rect.x += self.vel
            self.left = False