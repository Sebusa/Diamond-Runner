import pygame, datos, random
#Información adquirada de datos
def recortar(imagen,pos,size): return imagen.subsurface(pos[0],pos[1],size[0],size[1])
def info_player(imagen):
    pd = []
    for i in range(4): pd.append(recortar(imagen,[datos.psize*i,0],[datos.psize,datos.psize]))
    jumping = [recortar(imagen,[0,datos.psize],[datos.psize,datos.psize]),recortar(imagen,[0,datos.psize*2],[datos.psize,datos.psize])]
    wp = []
    for i in range(1,4): wp.append(recortar(imagen,[datos.psize*i,datos.psize],[datos.psize,datos.psize]))
    wp.append(recortar(imagen,[datos.psize*2,datos.psize],[datos.psize,datos.psize]))
    sp = []
    for i in range(1,4): sp.append(recortar(imagen,[datos.psize*i,datos.psize*2],[datos.psize,datos.psize]))
    sp.append(recortar(imagen,[datos.psize*2,datos.psize*2],[datos.psize,datos.psize]))
    bombb =  imagen.subsurface(0,datos.psize*3,int(datos.psize/2),int(datos.psize/4))
    blueb = imagen.subsurface(int(datos.psize/2),datos.psize*3,int(datos.psize/2),int(datos.psize/8))
    bullets = [blueb,bombb]
    salud = []
    for i in range(6): salud.append(recortar(imagen,[datos.psize,datos.psize*3+(int((datos.psize*i)/2))],[datos.psize*2+4,int(datos.psize/2)]))
    return [pd,wp,jumping,sp,salud,bullets]
def info_world(imagen1,imagen2):
    enemigos = []
    for y in range(7):
        e = []
        if y >5: limit = 4
        else: limit = 3
        for x in range(limit): e.append(recortar(imagen1,[datos.size*x,datos.size*y],[datos.size,datos.size]))
        enemigos.append(e)
    fireball = []
    for i in range(3): fireball.append(recortar(imagen2,[datos.size*i,datos.size],[datos.size,datos.size]))
    enemigos[-1].append(fireball)
    plasma = []
    for i in range(3): plasma.append(recortar(imagen2,[datos.size*i,0],[datos.size,datos.size]))
    enemigos[1].append(plasma)

    auxcoin = []
    for i in range(4): auxcoin.append(recortar(imagen2,[datos.size*i,datos.size*2],[datos.size,datos.size]))
    coins = [auxcoin[0],auxcoin[2],auxcoin[3],auxcoin[2],auxcoin[1],auxcoin[2],auxcoin[3],auxcoin[2]]

    boosters = []
    for i in range(1,4): boosters.append(recortar(imagen2,[datos.size*i,datos.size*3],[datos.size,datos.size]))
    return [enemigos,coins,boosters]
def monster_creator(estado,imagenes,pos):
    if estado == 0:
        monster = Eyebat(pos,imagenes)
        dado = random.randrange(100)
        if dado<25:
            monster.velx = 3
            monster.flip = False
            monster.estados['0'] = 1
            monster.estados['x'] = 0
        elif dado<50:
            monster.velx = -3
            monster.flip = True
            monster.estados['0'] = 1
            monster.estados['x'] = 1
        elif dado<75:
            monster.vely = 3
            monster.estados['0'] = 0
            monster.estados['y'] = 0
        else:
            monster.vely = -3
            monster.estados['0'] = 0
            monster.estados['y'] = 1
    elif estado == 1: monster = Saurus(pos,imagenes)
    elif estado == 2:
        monster = Slime(pos[0],imagenes,pos[1])
        dado = random.randrange(100)
        if dado<50:
            monster.velx = 1
            monster.flip = False
            monster.estados['x'] = 1
        else:
            monster.velx = -1
            monster.flip = True
            monster.estados['x'] = 0
    elif estado == 3: monster = Ghost(pos,imagenes)
    elif estado == 4: monster = Frog(pos,imagenes)
    return monster

class Jugador(pygame.sprite.Sprite):
    def __init__(self,imagenes,sounds):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.sonidos = sounds
        #salto,quieto(1:izq,0:der),moves,mouse,escaleras,inmune,bala
        self.estados = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        self.imgx = 0
        self.imgy = 0
        self.county = 1
        self.flip = False
        self.image = imagenes[self.imgx][self.imgy]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.salud = 6
        self.velx = 0
        self.vely = 0
        self.mapa = ""
        self.transcurso = 0

        self.sounds = [0,0,0]
        self.gravedad = [0,0,1]
        self.obstaculos = []
        self.escaleras = []
        self.balas = []
        self.enemigos = []
        self.monedas = 0

        self.quit = False
        self.skip = False
        self.boss = 0
    def update(self,objetos,enemigos):
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgx][self.imgy],True,False)
        else: self.image = self.imagenes[self.imgx][self.imgy]

        if self.mapa == datos.tutorial:
            if self.rect.right>datos.ancho and self.velx>0:
                  if self.transcurso == 1:
                      self.rect.right = datos.ancho
                      self.velx = 0
                      self.estados['2'] = 0
                  else:
                      for x in objetos: x.rect.x -= datos.ancho
                      for e in enemigos[0]: e.limitx -= datos.ancho
                      for e in enemigos[1]:
                          e.limites[0] -= datos.ancho
                          e.limites[1] -= datos.ancho
                      self.rect.x = 0
                      self.velx = 0
                      self.transcurso = 1
            if self.rect.left<0 and self.velx<0:
              if self.transcurso == 0:
                  self.rect.left = 0
                  self.velx = 0
                  self.estados['2'] = 0
              else:
                  for x in objetos: x.rect.x += datos.ancho
                  for e in enemigos[0]: e.limitx += datos.ancho
                  for e in enemigos[1]:
                      e.limites[0] += datos.ancho
                      e.limites[1] += datos.ancho
                  self.rect.x = datos.ancho
                  self.velx = 0
                  self.transcurso = 0
        if self.mapa == datos.mundouno:
            if self.rect.right>datos.ancho and self.velx>0:
                  if self.transcurso == 4 or self.transcurso == 8 or self.transcurso == 18 or self.transcurso == 22:
                      self.rect.right = datos.ancho
                      self.velx = 0
                      self.estados['2'] = 0
                  else:
                      for x in objetos: x.rect.x -= datos.ancho
                      for e in enemigos[1]:
                          e.limites[0] -= datos.ancho
                          e.limites[1] -= datos.ancho
                      self.rect.x = 0
                      self.velx = 0
                      self.transcurso += 1
            if self.rect.left<0 and self.velx<0:
              if self.transcurso == 1 or self.transcurso == 5 or self.transcurso == 11 or self.transcurso == 17 or self.transcurso == 21:
                  self.rect.left = 0
                  self.velx = 0
                  self.estados['2'] = 0
              else:
                  for x in objetos: x.rect.x += datos.ancho
                  for e in enemigos[1]:
                      e.limites[0] += datos.ancho
                      e.limites[1] += datos.ancho
                  self.rect.x = datos.ancho
                  self.velx = 0
                  self.transcurso -= 1
            if self.rect.top<0 and self.vely<0:
                if self.transcurso < 5 or self.transcurso == 13 or self.transcurso == 17 or self.transcurso > 17 or self.estados['4'] == 0:
                    self.gravedad[2] = 1
                    self.estados['0'] = 0
                    self.rect.top = 0
                    self.vely = 0
                else:
                    for x in objetos: x.rect.y += datos.alto
                    enemigos[0].empty()
                    self.rect.y = datos.alto
                    self.vely = 0
                    self.transcurso -= 4
            if self.rect.bottom>datos.alto and self.vely>0:
              if self.transcurso == 9 or self.transcurso == 13 or self.transcurso == 17 or self.transcurso == 18:
                  self.gravedad[2] = 0
                  self.rect.bottom = datos.alto
                  self.vely = 0
              else:
                  for x in objetos: x.rect.y -= datos.alto
                  enemigos[0].empty()
                  self.rect.y = 0
                  self.vely = 0
                  self.transcurso += 4
        if self.mapa == datos.mundodos:
            if self.rect.right>datos.ancho and self.velx>0:
                  if self.transcurso == 2 or self.transcurso == 6 or self.transcurso == 10 or self.transcurso == 15 or self.transcurso == 12:
                      self.rect.right = datos.ancho
                      self.velx = 0
                      self.estados['2'] = 0
                  else:
                      for x in objetos: x.rect.x -= datos.ancho
                      for e in enemigos[2]: e.rect.x -= datos.ancho
                      self.rect.x = 0
                      self.velx = 0
                      self.transcurso += 1
            if self.rect.left<0 and self.velx<0:
              if self.transcurso == 1 or self.transcurso == 5 or self.transcurso == 9 or self.transcurso == 13 or self.transcurso == 11:
                  self.rect.left = 0
                  self.velx = 0
                  self.estados['2'] = 0
              else:
                  for x in objetos: x.rect.x += datos.ancho
                  self.rect.x = datos.ancho
                  for e in enemigos[2]: e.rect.x += datos.ancho
                  self.velx = 0
                  self.transcurso -= 1
            if self.rect.top<0 and self.vely<0:
                if self.transcurso <= 2 or self.estados['4'] == 0:
                    self.gravedad[2] = 1
                    self.estados['0'] = 0
                    self.rect.top = 0
                    self.vely = 0
                else:
                    for x in objetos: x.rect.y += datos.alto
                    enemigos[0].empty()
                    enemigos[2].empty()
                    self.rect.y = datos.alto
                    self.vely = 0
                    self.transcurso -= 4
            if self.rect.bottom>datos.alto and self.vely>0:
                  for x in objetos: x.rect.y -= datos.alto
                  for e in enemigos[0]: e.limity -= datos.alto
                  enemigos[0].empty()
                  enemigos[2].empty()
                  self.rect.y = 0
                  self.vely = 0
                  self.transcurso += 4

        self.rect.x += self.velx
        horizontal = pygame.sprite.spritecollide(self,self.obstaculos,False)
        for obj in horizontal:
            if self.velx>0:
                if self.rect.right>obj.rect.left:
                    self.rect.right = obj.rect.left
                    self.estados['2'] = 0
                    self.velx = 0
            else:
                if self.rect.left<obj.rect.right:
                    self.rect.left = obj.rect.right
                    self.velx = 0
                    self.estados['2'] = 0
        self.rect.y += self.vely
        vertical = pygame.sprite.spritecollide(self,self.obstaculos,False)
        if len(vertical) == 0: self.gravedad[2] = 1
        else:
            for obj in vertical:
                if self.vely>0:
                    if self.rect.bottom > obj.rect.top:
                        self.rect.bottom = obj.rect.top
                        self.gravedad[2] = 0
                        self.estados['0'] = 0
                        self.vely = 0
                else:
                    if self.rect.top < obj.rect.bottom:
                        self.rect.top = obj.rect.bottom
                        self.gravedad[2] = 1
                        self.estados['0'] = 0
                        self.vely = 0

        #escaleras
        if self.estados['4'] == 1:
                escalcol = pygame.sprite.spritecollide(self,self.escaleras,False)
                if len(escalcol)>0:
                    for e in escalcol:
                        if self.rect.top < e.rect.top and self.vely < 0:
                            self.rect.top = e.rect.top
                            self.vely = 0
                        if self.rect.right > e.rect.right or self.rect.left < e.rect.left:
                            self.estados['4'] = 0
        self.caida(1)
    def insert_img(self):
        #Animaciones jugador
        if self.monedas == 12:
            self.imgx = 0
            self.imgy = 2
        elif self.salud == 0:
            self.imgx = 0
            self.imgy = 3
        elif self.estados['0'] == 1 or self.gravedad[-1] == 1 and self.estados['4'] == 0:
            if self.estados['0'] == 1:
                if self.sounds[0] == 0:
                    self.sonidos[0].play()
                    self.sounds[0] += 1
            if self.estados['3'] == 1:
                if self.sounds[1] == 0:
                    self.sonidos[1].play()
                    self.sounds[1] +=1
                self.imgx = 2
                self.imgy = 1
            else:
                self.imgx = 2
                self.imgy = 0
            if self.estados['1'] == 1: self.flip = True
            else: self.flip = False
        elif self.estados['2'] == 0:
            if self.estados['3'] == 1:
                if self.sounds[1] == 0:
                    self.sonidos[1].play()
                    self.sounds[1] +=1
                self.imgx = 0
                self.imgy = 1
            else:
                self.imgx = 0
                self.imgy = 0
            if self.estados['1'] == 1: self.flip = True
            else: self.flip = False
        else:
            if self.estados['0'] == 1:
                if self.estados['3'] == 1:
                    if self.sounds[1] == 0:
                        self.sonidos[1].play()
                        self.sounds[0] +=1
                    self.imgx = 2
                    self.imgy = 1
                else:
                    self.imgx = 2
                    self.imgy = 0
            elif self.estados['3'] == 1:
                if self.sounds[1] == 0:
                    self.sonidos[1].play()
                    self.sounds[1] +=1
                self.imgx = 3
            else: self.imgx = 1
            if self.estados['2'] == 1: self.flip = True
            elif self.estados['2'] == 2: self.flip = False
            if self.county == 40:
                self.county = 1
                self.imgy = 0
            else:
                if self.county%10 == 0: self.imgy += 1
                self.county +=1
        if self.estados['0'] == 0: self.sounds[0] = 0
        if self.estados['3'] == 0: self.sounds[1] = 0
    def player_motion(self):
        if self.estados['4'] == 1:
            self.estados['0'] = 0
            self.vely = -5
        if self.estados['0'] == 1:
            self.vely = int((1/4)*self.gravedad[0]*(self.gravedad[1]**2))
            self.gravedad[1] -= 1
            if self.gravedad[1] == 0: self.gravedad[0] = 0
            elif self.gravedad[1] < 0: self.gravedad[0] = 1
            if self.gravedad[1] == -14:
                    self.estados['0'] = 0
                    if self.gravedad[2] == 0:self.vely = 0
                    self.gravedad[0] = 0
                    self.gravedad[1] = 0
        if self.estados['2'] == 1: self.velx = -5
        elif self.estados['2'] == 2: self.velx = 5
        else:
            self.estados['2'] = 0
            self.velx = 0
    def caida(self,fuerza):
        if self.vely <= 25:
            if self.vely == 0: self.vely = 1
            else: self.vely += fuerza
class Barra(pygame.sprite.Sprite):
    def __init__(self,imagenes,pos):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.image = imagenes[pos]
        self.rect = self.image.get_rect()
        self.rect.x = 8
        self.rect.y = 8
    def update(self,pos):
        self.image = self.imagenes[pos]
class Bala(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes,estado,flip):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.estado = estado
        self.flip = flip
        self.posimg = [0,1]
        if self.estado == 0: self.image = self.imagenes
        else: self.image = self.imagenes[self.posimg[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
        self.damage = 0
    def update(self):
        self.rect.y += self.vely
        self.rect.x += self.velx
        if self.estado == 1:
            if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.posimg[0]],True,False)
            else: self.image = self.imagenes[self.posimg[0]]
            if self.posimg[1] == 30:
                self.posimg[1] = 1
                self.posimg[0] = 0
            else:
                if self.posimg[1]%10 == 0: self.posimg[0] += 1
                self.posimg[1] += 1
class Booster(pygame.sprite.Sprite):
    def __init__(self,pos,imagen,estado):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.estado = estado
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
#Generadores
class Vulnerable(pygame.sprite.Sprite):
    def __init__(self,imagenes,pos,estado):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.count = 1
        self.image = self.imagenes[self.count]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.salud = 3
        self.time = random.randrange(250)
        self.estado = estado
    def update(self):
        self.image = self.imagenes[self.count]

class Invisible(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0]*datos.size,size[1]*datos.size])
        self.image.fill([1,23,33,1])
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
class Estatico(pygame.sprite.Sprite):
    def __init__(self,pos,imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
class Dinamico(pygame.sprite.Sprite):
    def __init__(self,imagenes,pos,limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.limite = limite*10
        self.img = [0,1]
        self.image = self.imagenes[self.img[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
    def update(self):
        self.image = self.imagenes[self.img[0]]
        if self.img[1] == self.limite:
            self.img[1] = 1
            self.img[0] = 0
        else:
            if self.img[1]%10 == 0: self.img[0] += 1
            self.img[1] += 1
#Enemigos
class Slime(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes,limites):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.imgy = [0,1]
        self.flip = False
        self.limites = [limites[0]*datos.size,limites[1]*datos.size]
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.estados = {'x':0}
        self.velx = 0
        self.salud = 4
    def update(self):
        self.rect.x += self.velx
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
        else: self.image = self.imagenes[self.imgy[0]]
        if self.imgy[1] == 30:
            self.imgy[1] = 1
            self.imgy[0] = 0
        else:
            if self.imgy[1]%10 == 0: self.imgy[0] += 1
            self.imgy[1] += 1
        if self.rect.right>self.limites[1] and self.velx>0:
            self.rect.right = self.limites[1]
            self.estados['x'] = 0
            self.velx = 0
        if self.rect.left<self.limites[0] and self.velx<0:
            self.estados['x'] = 1
            self.rect.left = self.limites[0]
            self.velx = 0

        if self.estados['x'] == 1:
            self.velx = 1
            self.flip = False
        else:
            self.velx = -1
            self.flip = True
class Saurus(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes[:4]
        self.fireball = imagenes[3]
        self.imgy = [0,1]
        self.cont = 0
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.estados = {'1':0,'2':0}
        self.flip = False
        self.salud = 2
        self.obstaculos = []
    def update(self):
        if self.estados['2'] == 0:
            if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
            else: self.image = self.imagenes[self.imgy[0]]
            if self.imgy[1] == 30:
                self.imgy[1] = 1
                self.imgy[0] = 0
            else:
                if self.imgy[1]%10 == 0: self.imgy[0] += 1
                self.imgy[1] += 1
        else:
            if self.flip == True: self.image = pygame.transform.flip(self.fireball,True,False)
            else: self.image = self.imagenes[3]
            if self.cont == 10:
                self.estados['2'] = 0
                self.cont = 0
            else: self.cont +=1
class Eyebat(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes[:3]
        self.plasmas = imagenes[1]
        self.imgy = [0,1]
        self.imgp = [0,0]
        self.flip = False
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.limity = pos[0]*datos.size+400
        self.velx = 0
        self.vely = 0
        self.estados= {'0':3,'x':3,'y':3,'3':3}
        self.salud = 1
        self.obstaculos = []
        self.time = random.randrange(30,100)
    def update(self):
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
        else: self.image = self.imagenes[self.imgy[0]]
        if self.imgy[1] == 30:
            self.imgy[1] = 1
            self.imgy[0] = 0
        else:
            if self.imgy[1]%10 == 0: self.imgy[0] += 1
            self.imgy[1] += 1
        if self.rect.bottom>self.limity-200 and self.vely>0:
            self.estados['3'] = 1
            self.rect.bottom = self.limity-200
            self.vely = 0
        colisiones = pygame.sprite.spritecollide(self,self.obstaculos,False)
        for b in colisiones:
            self.estados['3']=1
            if self.rect.right > b.rect.left and self.velx>0 :
                self.rect.right = b.rect.left
                self.velx=0
            if self.rect.left < b.rect.right and self.velx<0:
                self.rect.left = b.rect.right
                self.velx=0
            if self.rect.bottom > b.rect.top and self.vely>0:
                self.rect.bottom = b.rect.top
                self.vely=0
            if self.rect.top < b.rect.bottom and self.vely<0:
                self.rect.top = b.rect.bottom
                self.vely=0

        if self.estados['3'] == 1:
            self.estados['3'] = 0
            moneda = random.randrange(100)
            if moneda<50:
                self.estados['x'] = 0
                self.vely = 0
                dado = random.randrange(100)
                if dado<50:
                    self.velx = 3
                    self.flip = False
                else:
                    self.velx = -3
                    self.flip = True
            else:
                self.estados['y'] = 0
                self.velx = 0
                dado = random.randrange(100)
                if dado<50: self.vely = 3
                else: self.vely = -3
        self.rect.x += self.velx
        self.rect.y += self.vely
class Ghost(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.imgy = [0,1]
        self.flip = False
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.estados = {'x':0,'1':0}
        self.velx = 0
        self.salud = 1
    def update(self):
        if self.estados['1'] == 0:
            if random.randrange(200) <= 0:
                self.estados['1'] = 1
                self.velx = 0
        elif self.estados['1'] <= 70: self.estados['1'] += 1
        else:
            self.estados['1'] = 0
            if random.randrange(100) < 50: self.estados['x'] = 1
            else: self.estados['x'] = 0

        self.rect.x += self.velx
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
        else: self.image = self.imagenes[self.imgy[0]]
        if self.imgy[1] == 30:
            self.imgy[1] = 1
            self.imgy[0] = 0
        else:
            if self.imgy[1]%10 == 0: self.imgy[0] += 1
            self.imgy[1] += 1
        if self.estados['1'] == 0:
            if self.estados['x'] == 1:
                self.velx = 1
                self.flip = False
            else:
                self.velx = -1
                self.flip = True
class Frog(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.estados = {'s':0}
        self.count = [0,0]
        self.image = self.imagenes[self.count[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.flip = False
        self.gravedad = [0,0,1]
        self.velx = 0
        self.vely = 0
        self.salud = 2
        self.obstaculos = []
    def update(self):
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.count[0]],True,False)
        else: self.image = self.imagenes[self.count[0]]
        if self.estados['s'] == 0:
            if random.randrange(150) <= 0:
                self.gravedad[1] = 12
                self.gravedad[0] = -1
                self.estados['s'] = 1
        else:
            self.vely = int((1/4)*self.gravedad[0]*(self.gravedad[1]**2))
            if self.count[0] == 0:
                if random.randrange(100) < 50:
                    self.velx = 4
                    self.flip = False
                else:
                    self.velx = -4
                    self.flip = True
                self.count[0] = 1

            self.rect.x += self.velx
            horizontal = pygame.sprite.spritecollide(self,self.obstaculos,False)
            for obj in horizontal:
                if self.velx>0:
                    if self.rect.right>obj.rect.left:
                        self.rect.right = obj.rect.left
                        self.velx = 0
                else:
                    if self.rect.left<obj.rect.right:
                        self.rect.left = obj.rect.right
                        self.velx = 0
            self.rect.y += self.vely
            vertical = pygame.sprite.spritecollide(self,self.obstaculos,False)
            if len(vertical) == 0: self.gravedad[2] = 1
            else:
                for obj in vertical:
                    if self.vely>0:
                        if self.rect.bottom > obj.rect.top:
                            self.rect.bottom = obj.rect.top
                            self.gravedad[2] = 0
                            self.estados['s'] = 0
                            self.vely = 0
                            self.count[0] = 0
                            self.gravedad[0] = 0
                            self.gravedad[1] = 0
                    else:
                        if self.rect.top < obj.rect.bottom:
                            self.rect.top = obj.rect.bottom
                            self.gravedad[2] = 1
                            self.vely = 0
                            self.count[0] = 2

            self.gravedad[1] -= 1
            if self.gravedad[1] >= 0: self.count[0] = 1
            if self.gravedad[1] == 0: self.gravedad[0] = 0
            elif self.gravedad[1] < 0: self.gravedad[0] = 1
        if self.gravedad[2] == 1: self.caida(1)
    def caida(self,fuerza): self.vely += fuerza

class Bigbat(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes[:3]
        self.plasmas = imagenes[1]
        self.imgy = [0,1]
        self.imgp = [0,0]
        self.flip = False
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.velx = 0
        self.vely = 0
        self.estados= {'0':3,'x':3,'y':3,'3':3}
        self.salud = 25
        self.obstaculos = []
        self.time = random.randrange(30,100)
    def update(self):
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
        else: self.image = self.imagenes[self.imgy[0]]
        if self.imgy[1] == 30:
            self.imgy[1] = 1
            self.imgy[0] = 0
        else:
            if self.imgy[1]%10 == 0: self.imgy[0] += 1
            self.imgy[1] += 1
        if self.rect.bottom>440 and self.vely>0:
            self.estados['3'] = 1
            self.rect.bottom = 440
            self.vely = 0
        if self.rect.top<0 and self.vely<0:
            self.estados['3'] = 1
            self.rect.bottom = 0
            self.vely = 0
        colisiones = pygame.sprite.spritecollide(self,self.obstaculos,False)
        for b in colisiones:
            self.estados['3']=1
            if self.rect.right > b.rect.left and self.velx>0 :
                self.rect.right = b.rect.left
                self.velx=0
            if self.rect.left < b.rect.right and self.velx<0:
                self.rect.left = b.rect.right
                self.velx=0
            if self.rect.bottom > b.rect.top and self.vely>0:
                self.rect.bottom = b.rect.top
                self.vely=0
            if self.rect.top < b.rect.bottom and self.vely<0:
                self.rect.top = b.rect.bottom
                self.vely=0

        if self.estados['3'] == 1:
            self.estados['3'] = 0
            moneda = random.randrange(100)
            if moneda<50:
                self.estados['x'] = 0
                self.vely = 0
                dado = random.randrange(100)
                if dado<50:
                    self.velx = 5
                    self.flip = False
                else:
                    self.velx = -5
                    self.flip = True
            else:
                self.estados['y'] = 0
                self.velx = 0
                dado = random.randrange(100)
                if dado<50: self.vely = 5
                else: self.vely = -5
        self.rect.x += self.velx
        self.rect.y += self.vely
class Skeleton(pygame.sprite.Sprite):
    def __init__(self,pos,imagenes,obstaculos):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = imagenes
        self.imgy = [0,1]
        self.flip = False
        self.image = self.imagenes[self.imgy[0]]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*datos.size
        self.rect.y = pos[1]*datos.size
        self.obstaculos = obstaculos
        self.velx = 4
        self.flip = False
        self.salud = 25
    def update(self):
        if self.flip == True: self.image = pygame.transform.flip(self.imagenes[self.imgy[0]],True,False)
        else: self.image = self.imagenes[self.imgy[0]]
        if self.imgy[1] == 30:
            self.imgy[1] = 1
            self.imgy[0] = 0
        else:
            if self.imgy[1]%10 == 0: self.imgy[0] += 1
            self.imgy[1] += 1

        colision = pygame.sprite.spritecollide(self,self.obstaculos,False)
        if len(colision) != 0:
            for c in colision:
                if self.rect.right>c.rect.left and self.velx>0:
                    self.rect.right = c.rect.left
                    self.flip = True
                    self.velx = 0
                if self.rect.left<c.rect.right and self.velx<0:
                    self.flip = False
                    self.rect.left = c.rect.right
                    self.velx = 0
        if self.flip == False: self.velx = 4
        else: self.velx = -4
        self.rect.x += self.velx
