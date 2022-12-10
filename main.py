import pygame,random,json
import funciones, datos, collider
#hago los mundos
def tile_maker(archivo):
    with open(archivo) as data: info = json.load(data)
    width = info['width']
    height = info['height']

    stuff = []
    for item in info['layers']:
        datos = item['data']
        mapa = []
        for i in range(0,len(datos),width): mapa.append(datos[i:i+width])
        stuff.append(mapa)
    set = info['tilesets']
    data.close()
    return [stuff,[width,height]]
def tile_cut(imagen):
    tmatriz = []
    x = 0
    y = 0
    for i in range(16):
        for j in range(20):
            tmatriz.append(funciones.recortar(imagen,[x,y],[64,64]))
            x += 64
        x = 0
        y += 64
    return tmatriz

def gameover(player):
    fin = False
    if player.estados['1'] == 1: player.flip = True
    else: player.flip = False
    player.insert_img()
    player.update(scrolling,[eyebats,slimes])
    pantalla.fill([1,23,33,1])
    enemigos.empty()
    fondo.draw(pantalla)
    intangibles.draw(pantalla)
    jugadores.draw(pantalla)
    pantalla.blit(pygame.image.load(datos.GAMEOVER),(0,0))
    gamesfx[0].play()
    while not fin:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: fin = True
def victory(player):
    fin = False
    if player.estados['1'] == 1: player.flip = True
    else: player.flip = False
    player.insert_img()

    player.update(scrolling,[eyebats,slimes])
    pantalla.fill([1,23,33,1])
    fondo.draw(pantalla)
    intangibles.draw(pantalla)
    jugadores.draw(pantalla)
    pantalla.blit(pygame.image.load(datos.WIN),(0,0))
    gamesfx[1].play()
    while not fin:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: fin = True

def agrupar():
    scrolling.add(obstaculos)
    scrolling.add(escaleras)
    scrolling.add(intangibles)
    scrolling.add(trampas)
    scrolling.add(fondo)
    scrolling.add(lava)
    scrolling.add(vulnerables)
    scrolling.add(slimes)
    scrolling.add(sauruses)
    scrolling.add(eyebats)
    scrolling.add(ghosts)
    scrolling.add(enemigos)
    scrolling.add(frogs)
    scrolling.add(balas_aliadas)
    scrolling.add(balas_enemigas)
    scrolling.add(boosters)
    scrolling.add(monedas)
def vaciar():
    obstaculos.empty()
    enemigos.empty()
    escaleras.empty()
    fondo.empty()
    vulnerables.empty()
    intangibles.empty()
    lava.empty()
    trampas.empty()
    slimes.empty()
    sauruses.empty()
    frogs.empty()
    eyebats.empty()
    ghosts.empty()
    monedas.empty()
    boosters.empty()
    balas_enemigas.empty()
    balas_aliadas.empty()

def inicio():
    fin = False
    pantalla.fill([0,0,0])
    fuente = pygame.font.SysFont("Impact",50)
    while not fin:
        if player.skip == True: fin = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                player.quit = True
            if event.type == pygame.KEYDOWN:
                if player.skip == False:
                    if event.key == pygame.K_p: player.skip = True
            info = 'DIAMOND RUNNER'
            text = 'Press P to continue'
            texto1 = fuente.render(info,True,[255,255,255])
            texto2 = fuente.render(text,True,[255,255,255])
            pantalla.blit(texto1,[350,220])
            pantalla.blit(texto2,[320,400])
            pygame.display.flip()

def barrahp(personaje,pantalla):
    largo = 100
    ancho = 20
    calculo = int((personaje.salud*100)/25)
    borde = pygame.Rect(14*datos.size,10,largo,ancho)
    rectangulo = pygame.Rect(14*datos.size,10,calculo,ancho)
    pygame.draw.rect(pantalla,[255,255,255],borde)
    pygame.draw.rect(pantalla,[255,0,0],rectangulo)
def bossfight(archivo,bossimg,player,infoworld):
    if archivo == datos.mundouno:
        boss = funciones.Bigbat([8,4],bossimg)
        boss.obstaculos = obstaculos
        dado = random.randrange(100)
        if dado<25:
            boss.velx = 5
            boss.flip = False
            boss.estados['0'] = 1
            boss.estados['x'] = 0
        elif dado<50:
            boss.velx = -5
            boss.flip = True
            boss.estados['0'] = 1
            boss.estados['x'] = 1
        elif dado<75:
            boss.vely = 5
            boss.estados['0'] = 0
            boss.estados['y'] = 0
        else:
            boss.vely = -5
            boss.estados['0'] = 0
            boss.estados['y'] = 1
        song = datos.boss1
    elif archivo == datos.mundodos:
        song = datos.boss2
        boss = funciones.Skeleton([2,8],bossimg,obstaculos)
        boss.velx = 4
    jefes = pygame.sprite.Group()
    jefes.add(boss)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(3)
    fin = False
    while not fin:
        if boss.salud == 0:
            fin = True
        if player.salud == 0:
            fin = True
            pygame.mixer.music.stop()
            gameover(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                player.quit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.estados['2'] = 1
                    player.estados['1'] = 1
                if event.key == pygame.K_d:
                    player.estados['2'] = 2
                    player.estados['1'] = 0
                if archivo == datos.tutorial:
                    if player.skip == False:
                        if event.key == pygame.K_p: player.skip = True
                if player.estados['0'] == 0:
                    if event.key == pygame.K_SPACE:
                        if player.gravedad[2] == 0:
                            player.estados['0'] = 1
                            player.gravedad[1] = 12
                            player.gravedad[0] = -1
                for escal in escaleras:
                    if player.rect.top >= escal.rect.top and player.rect.top <= escal.rect.bottom:
                        if player.rect.right <= escal.rect.right and player.rect.left >= escal.rect.left:
                            if player.estados['4'] == 0:
                                if event.key == pygame.K_w: player.estados['4'] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: player.estados['2'] = 0
                if event.key == pygame.K_w: player.estados['4'] = 0
                player.vely = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    player.estados['3'] = 1
                    if player.estados['6'] == 0: bimg = info_player[-1][0]
                    else: bimg = info_player[-1][1]
                    bala = funciones.Bala([player.rect.x,player.rect.y+int(datos.psize/2)],bimg,0,player.flip)
                    if player.flip == False: bala.velx = 12
                    else: bala.velx = -12
                    bala.obstaculos = obstaculos
                    balas_aliadas.add(bala)
            if event.type == pygame.MOUSEBUTTONUP: player.estados['3'] = 0
        #movimientos del jugador
        player.player_motion()
        player.insert_img()

        lavacol = pygame.sprite.spritecollide(player,lava,False)
        if len(lavacol)>0:
            for l in lavacol:
                if player.rect.bottom >= l.rect.top+24 and player.vely > 0:
                    player.salud = 0
                    break
        for g in vulnerables:
            if g.time < 0:
                if g.estado == 0:
                    e = funciones.monster_creator(0,infoworld[0][1],[int(g.rect.x/datos.size),int(g.rect.y/datos.size)])
                    e.obstaculos = obstaculos
                    eyebats.add(e)
                    enemigos.add(e)
                elif g.estado == 1:
                    e = funciones.monster_creator(3,infoworld[0][2],[int(g.rect.x/datos.size),int(g.rect.y/datos.size)])
                    ghosts.add(e)
                g.time = 270
            elif g.time > 250: g.count = 0
            else: g.count = 1
            g.time -= 1
            if g.salud == 1:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,vulnerables,True)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
            else:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,vulnerables,False)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
                        g.salud -= 1
        for enemy in eyebats:
            time = random.randrange(200)
            if time <= 0:
                pos = enemy.rect.center
                bullet = funciones.Bala(pos,infoworld[0][1][-1],2,False)
                bullet.vely = 6
                balas_enemigas.add(bullet)
                scrolling.add(balas_enemigas)
        for enemy in ghosts:
            if enemy.estados['1'] != 0:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,ghosts,True)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
        for enemy in enemigos:
            if player.estados['6'] == 0:
                if enemy.salud == 1:
                    for bala in balas_aliadas:
                        colisiones = pygame.sprite.spritecollide(bala,enemigos,True)
                        if len(colisiones) == 1:
                            balas_aliadas.remove(bala)
                            worldsfx[1].play()
                else:
                    for bala in balas_aliadas:
                        colisiones = pygame.sprite.spritecollide(bala,enemigos,False)
                        if len(colisiones) == 1:
                            balas_aliadas.remove(bala)
                            enemy.salud -= 1
                            worldsfx[1].play()
            elif player.estados['6'] == 1:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,enemigos,True)
                    if len(colisiones) > 0:
                        balas_aliadas.remove(bala)
                        worldsfx[3].play()
        enemycol = pygame.sprite.spritecollide(player,enemigos,False)
        if len(enemycol) >0:
            if player.estados['5'] == 0:
                sounds[-1].play()
                player.estados['5'] += 1
        bosscol = pygame.sprite.spritecollide(player,jefes,False)
        if len(bosscol) >0:
            if player.estados['5'] == 0:
                sounds[-1].play()
                player.salud -= 1
                player.estados['5'] += 1
        ghostcol = pygame.sprite.spritecollide(player,ghosts,False)
        if len(ghostcol) >0:
            if player.estados['5'] == 0:
                sounds[-1].play()
                player.salud -= 1
                player.estados['5'] += 1
        for bala in balas_aliadas:
            if bala.rect.left < 0: balas_aliadas.remove(bala)
            if bala.rect.right > datos.ancho: balas_aliadas.remove(bala)
            ricochet = pygame.sprite.spritecollide(bala,balas_enemigas,True)
            if len(ricochet)>0: balas_aliadas.remove(bala)
            colisiones = pygame.sprite.spritecollide(bala,obstaculos,False)
            if len(colisiones)>0: balas_aliadas.remove(bala)
            if boss.salud > 1:
                colboss = pygame.sprite.spritecollide(bala,jefes,False)
                if len(colboss) > 0:
                    balas_aliadas.remove(bala)
                    boss.salud -= 1
            else:
                colboss = pygame.sprite.spritecollide(bala,jefes,True)
                if len(colboss) > 0:
                    balas_aliadas.remove(bala)
                    boss.salud -= 1
        for bala in balas_enemigas:
            if bala.rect.left < 0: balas_aliadas.remove(bala)
            if bala.rect.right > datos.ancho: balas_aliadas.remove(bala)
            if bala.rect.bottom > datos.alto: balas_enemigas.remove(bala)
            colisiones = pygame.sprite.spritecollide(bala,jugadores,False)
            if len(colisiones)>0:
                if player.estados['5'] == 0:
                    balas_enemigas.remove(bala)
                    sounds[-1].play()
                    player.salud -= 1
                    player.estados['5'] += 1
            colisiones = pygame.sprite.spritecollide(bala,obstaculos,False)
            if len(colisiones)>0: balas_enemigas.remove(bala)
        #inmunidad del jugador trase ser sido golpeado
        if player.estados['5'] == 50: player.estados['5'] = 0
        elif player.estados['5'] != 0: player.estados['5'] += 1

        jugadores.update(scrolling,[eyebats,slimes,ghosts])
        balas_aliadas.update()
        balas_enemigas.update()
        salud.update(player.salud-1)
        enemigos.update()
        jefes.update()
        ghosts.update()
        vulnerables.update()

        pantalla.fill([1,23,33,1])
        fondo.draw(pantalla)
        balas_aliadas.draw(pantalla)
        balas_enemigas.draw(pantalla)
        intangibles.draw(pantalla)
        vulnerables.draw(pantalla)
        jugadores.draw(pantalla)

        enemigos.draw(pantalla)
        ghosts.draw(pantalla)
        jefes.draw(pantalla)
        salud.draw(pantalla)
        barrahp(boss,pantalla)
        pygame.display.flip()
        reloj.tick(60)

def load_map(archivo,imagen,infoworld,generadores):
    mapa_info = tile_maker(archivo)
    width = mapa_info[1][0]
    height = mapa_info[1][1]
    data = mapa_info[0]
    matriz = tile_cut(imagen)
    intangible = data[0]
    for i in range(height):
        for j in range(width):
            if intangible[i][j] != 0 :
                posmap = intangible[i][j]
                obj = funciones.Estatico([j,i],matriz[posmap-1])
                intangibles.add(obj)
    if archivo == datos.tutorial:
        stuff = collider.tutorial()
        for i in stuff[0]:
            obstaculos.add(i)
        escaleras.add(stuff[1])
        ladders = data[1]
        font = data[2]
        for i in range(height):
            for j in range(width):
                if ladders[i][j] != 0 :
                    posmap = ladders[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if font[i][j] != 0 :
                    posmap = font[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    fondo.add(obj)

        coin = funciones.Dinamico(infoworld[1],stuff[2],8)
        monedas.add(coin)
        for s in stuff[3]:
            sa = funciones.monster_creator(1,infoworld[0][-1],s)
            enemigos.add(sa)
        estado = random.randrange(3)
        bo = funciones.Booster(stuff[4],infoworld[2][estado],estado)
        boosters.add(bo)
    if archivo == datos.mundouno:
        stuff = collider.mundouno()
        obstaculos.add(stuff[0])
        escaleras.add(stuff[1])
        lava.add(stuff[2])
        ladders = data[1]
        magma = data[2]
        font = data[3]
        for i in range(height):
            for j in range(width):
                if ladders[i][j] != 0 :
                    posmap = ladders[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if magma[i][j] != 0 :
                    posmap = magma[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if font[i][j] != 0 :
                    posmap = font[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    fondo.add(obj)

        for g in stuff[3]:
            generador = funciones.Vulnerable(generadores[0],g,0)
            vulnerables.add(generador)
        for s in stuff[4]:
            sa = funciones.monster_creator(1,infoworld[0][6],s)
            sauruses.add(sa)
            enemigos.add(sauruses)
        for l in stuff[5]:
            sli = funciones.monster_creator(2,infoworld[0][0],l)
            slimes.add(sli)
            enemigos.add(sli)
        for c in stuff[6]:
            coin = funciones.Dinamico(infoworld[1],c,8)
            monedas.add(coin)
        for b in stuff[7]:
            estado = random.randrange(3)
            bo = funciones.Booster(b,infoworld[2][estado],estado)
            boosters.add(bo)
    if archivo == datos.mundodos:
        stuff = collider.mundodos()
        obstaculos.add(stuff[0])
        escaleras.add(stuff[1])
        lava.add(stuff[2])
        trampas.add(stuff[3])
        ladders = data[1]
        magma = data[2]
        traps = data[3]
        font = data[4]
        for i in range(height):
            for j in range(width):
                if ladders[i][j] != 0 :
                    posmap = ladders[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if magma[i][j] != 0 :
                    posmap = magma[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if traps[i][j] != 0 :
                    posmap = traps[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    intangibles.add(obj)
        for i in range(height):
            for j in range(width):
                if font[i][j] != 0 :
                    posmap = font[i][j]
                    obj = funciones.Estatico([j,i],matriz[posmap-1])
                    fondo.add(obj)

        for g in stuff[4]:
            generador = funciones.Vulnerable(generadores[0],g,0)
            vulnerables.add(generador)
        for g in stuff[5]:
            generador = funciones.Vulnerable(generadores[1],g,1)
            vulnerables.add(generador)
        for s in stuff[6]:
            sa = funciones.Frog(s,infoworld[0][3])
            frogs.add(sa)
            sa.obstaculos = obstaculos
            enemigos.add(sa)
        for c in stuff[7]:
            coin = funciones.Dinamico(infoworld[1],c,8)
            monedas.add(coin)
        for b in stuff[8]:
            estado = random.randrange(3)
            bo = funciones.Booster(b,infoworld[2][estado],estado)
            boosters.add(bo)
def world(player,imagen,archivo,infoworld,generadores):
    fin = False
    load_map(archivo,imagen,infoworld,generadores)
    if archivo == datos.tutorial: player.mapa = datos.tutorial
    if archivo == datos.mundouno: player.mapa = datos.mundouno
    if archivo == datos.mundodos: player.mapa = datos.mundodos
    agrupar()
    fuente = pygame.font.Font(None,32)
    while not fin:
        if archivo == datos.tutorial:
            if player.monedas == 1:
                fin = True
        if archivo == datos.mundouno:
            if player.transcurso == 20: player.boss = 1
        if archivo == datos.mundodos:
            if player.transcurso == 12: player.boss = 1
        if player.skip == True: fin = True
        if player.salud == 0:
            fin = True
            pygame.mixer.music.stop()
            gameover(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                player.quit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.estados['2'] = 1
                    player.estados['1'] = 1
                if event.key == pygame.K_d:
                    player.estados['2'] = 2
                    player.estados['1'] = 0
                if archivo == datos.tutorial or archivo == datos.mundouno:
                    if player.skip == False:
                        if event.key == pygame.K_p: player.skip = True
                if player.estados['0'] == 0:
                    if event.key == pygame.K_SPACE:
                        if player.gravedad[2] == 0:
                            player.estados['0'] = 1
                            player.gravedad[1] = 12
                            player.gravedad[0] = -1
                for escal in escaleras:
                    if player.rect.top >= escal.rect.top and player.rect.top <= escal.rect.bottom:
                        if player.rect.right <= escal.rect.right and player.rect.left >= escal.rect.left:
                            if player.estados['4'] == 0:
                                if event.key == pygame.K_w: player.estados['4'] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d: player.estados['2'] = 0
                if event.key == pygame.K_w: player.estados['4'] = 0
                player.vely = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    player.estados['3'] = 1
                    if player.estados['6'] == 0: bimg = info_player[-1][0]
                    else: bimg = info_player[-1][1]
                    bala = funciones.Bala([player.rect.x,player.rect.y+int(datos.psize/2)],bimg,0,player.flip)
                    if player.flip == False: bala.velx = 12
                    else: bala.velx = -12
                    bala.obstaculos = obstaculos
                    balas_aliadas.add(bala)
            if event.type == pygame.MOUSEBUTTONUP: player.estados['3'] = 0
        #movimientos del jugador
        player.player_motion()
        player.insert_img()

        if player.boss != 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            eyebats.empty()
            monedas.empty()
            slimes.empty()
            sauruses.empty()
            if archivo == datos.mundouno: bossfight(archivo,infoworld[0][4],player,infoworld)
            elif archivo == datos.mundodos: bossfight(archivo,infoworld[0][5],player,infoworld)
            fin = True

        lavacol = pygame.sprite.spritecollide(player,lava,False)
        if len(lavacol)>0:
            for l in lavacol:
                if player.rect.bottom >= l.rect.top+24 and player.vely > 0:
                    break
        trampacol = pygame.sprite.spritecollide(player,trampas,False)
        if len(trampacol)>0:
            for t in trampacol:
                if player.rect.bottom >= t.rect.top+24 and player.vely > 0:
                    if player.estados['5'] == 0:
                        player.salud -= 1
                        player.estados['5'] += 1
                    break
                if player.rect.top <= t.rect.bottom-24 and player.vely < 0:
                    if player.estados['5'] == 0:
                        sounds[-1].play()
                        player.estados['5'] += 1
                    break
        for g in vulnerables:
            if g.time < 0:
                if g.estado == 0:
                    e = funciones.monster_creator(0,infoworld[0][1],[int(g.rect.x/datos.size),int(g.rect.y/datos.size)])
                    e.obstaculos = obstaculos
                    eyebats.add(e)
                    enemigos.add(e)
                elif g.estado == 1:
                    e = funciones.monster_creator(3,infoworld[0][2],[int(g.rect.x/datos.size),int(g.rect.y/datos.size)])
                    ghosts.add(e)
                g.time = 270
            elif g.time > 250: g.count = 0
            else: g.count = 1
            g.time -= 1
            if g.salud == 1:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,vulnerables,True)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
            else:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,vulnerables,False)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
                        g.salud -= 1
        for enemy in sauruses:
            time = random.randrange(150)
            if time <= 0:
                pos = enemy.rect.center
                enemy.estados['2'] = 1
                if random.randrange(100) < 50: enemy.flip = False
                else: enemy.flip = True
                bullet = funciones.Bala(pos,infoworld[0][6][4],1,enemy.flip)
                if bullet.flip == False: bullet.velx = 6
                else: bullet.velx = -6
                balas_enemigas.add(bullet)
                scrolling.add(balas_enemigas)
        for enemy in eyebats:
            time = random.randrange(200)
            if time <= 0:
                pos = enemy.rect.center
                bullet = funciones.Bala(pos,infoworld[0][1][3],2,False)
                bullet.vely = 6
                balas_enemigas.add(bullet)
                scrolling.add(balas_enemigas)
        for enemy in ghosts:
            if enemy.estados['1'] != 0:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,ghosts,True)
                    if len(colisiones) == 1:
                        balas_aliadas.remove(bala)
                        worldsfx[1].play()
        for enemy in enemigos:
            if player.estados['6'] == 0:
                if enemy.salud == 1:
                    for bala in balas_aliadas:
                        colisiones = pygame.sprite.spritecollide(bala,enemigos,True)
                        if len(colisiones) == 1:
                            balas_aliadas.remove(bala)
                            worldsfx[1].play()
                else:
                    for bala in balas_aliadas:
                        colisiones = pygame.sprite.spritecollide(bala,enemigos,False)
                        if len(colisiones) == 1:
                            balas_aliadas.remove(bala)
                            enemy.salud -= 1
                            worldsfx[1].play()
            elif player.estados['6'] == 1:
                for bala in balas_aliadas:
                    colisiones = pygame.sprite.spritecollide(bala,enemigos,True)
                    if len(colisiones) > 0:
                        balas_aliadas.remove(bala)
                        worldsfx[3].play()
        enemycol = pygame.sprite.spritecollide(player,enemigos,False)
        if len(enemycol) >0:
            if player.estados['5'] == 0:
                sounds[-1].play()
                player.estados['5'] += 1
        ghostcol = pygame.sprite.spritecollide(player,ghosts,False)
        if len(ghostcol) >0:
            if player.estados['5'] == 0:
                sounds[-1].play()
                player.estados['5'] += 1
        for bala in balas_aliadas:
            if bala.rect.left < 0: balas_aliadas.remove(bala)
            if bala.rect.right > datos.ancho: balas_aliadas.remove(bala)
            ricochet = pygame.sprite.spritecollide(bala,balas_enemigas,True)
            if len(ricochet)>0: balas_aliadas.remove(bala)
            colisiones = pygame.sprite.spritecollide(bala,obstaculos,False)
            if len(colisiones)>0: balas_aliadas.remove(bala)
        for bala in balas_enemigas:
            if bala.rect.left < 0: balas_aliadas.remove(bala)
            if bala.rect.right > datos.ancho: balas_aliadas.remove(bala)
            if bala.rect.bottom > datos.alto: balas_enemigas.remove(bala)
            colisiones = pygame.sprite.spritecollide(bala,jugadores,False)
            if len(colisiones)>0:
                if player.estados['5'] == 0:
                    balas_enemigas.remove(bala)
                    sounds[-1].play()
                    player.estados['5'] += 1
            colisiones = pygame.sprite.spritecollide(bala,obstaculos,False)
            if len(colisiones)>0: balas_enemigas.remove(bala)
        #inmunidad del jugador trase ser sido golpeado
        if player.estados['5'] == 50: player.estados['5'] = 0
        elif player.estados['5'] != 0: player.estados['5'] += 1

        coincol = pygame.sprite.spritecollide(player,monedas,True)
        if len(coincol) == 1:
            player.monedas += 1
            worldsfx[0].play()
        boostercol = pygame.sprite.spritecollide(player,boosters,True)
        if len(boostercol)>0:
            for b in boostercol:
                if b.estado == 0:
                    sounds[2].play()
                    if player.salud < 6: player.salud += 1
                elif b.estado == 1:
                    player.salud = 6
                    worldsfx[2].play()
                elif b.estado == 2:
                    sounds[2].play()
                    player.estados['6'] = 1

        jugadores.update(scrolling,[eyebats,slimes,ghosts])
        balas_aliadas.update()
        balas_enemigas.update()
        salud.update(player.salud-1)
        monedas.update()
        enemigos.update()
        ghosts.update()
        vulnerables.update()

        pantalla.fill([1,23,33,1])
        fondo.draw(pantalla)
        balas_aliadas.draw(pantalla)
        balas_enemigas.draw(pantalla)
        intangibles.draw(pantalla)
        vulnerables.draw(pantalla)
        jugadores.draw(pantalla)

        monedas.draw(pantalla)
        enemigos.draw(pantalla)
        ghosts.draw(pantalla)
        boosters.draw(pantalla)
        salud.draw(pantalla)
        pantalla.blit(infoworld[1][4],(120,-10))
        info = 'x'+str(player.monedas)
        texto = fuente.render(info,True,[255,255,255])
        pantalla.blit(texto,[170,15])
        pygame.display.flip()
        reloj.tick(60)

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([datos.ancho,datos.alto])
    reloj = pygame.time.Clock()

    #Imagenes & sfx
    playerimg = pygame.image.load(datos.playerimg)
    enemyimg = pygame.image.load(datos.enemyimg)
    itemimg = pygame.image.load(datos.itemimg)
    tilesimg = pygame.image.load(datos.tilesimg)
    sounds = [pygame.mixer.Sound(datos.jump),pygame.mixer.Sound(datos.shoot),pygame.mixer.Sound(datos.pickup),pygame.mixer.Sound(datos.playerhit)]
    worldsfx = [pygame.mixer.Sound(datos.coin),pygame.mixer.Sound(datos.enemyhit),pygame.mixer.Sound(datos.newlife),pygame.mixer.Sound(datos.explosion)]
    gamesfx = [pygame.mixer.Sound(datos.gameover),pygame.mixer.Sound(datos.win)]

    #Grupos
    jugadores = pygame.sprite.Group()
    salud = pygame.sprite.Group()

    obstaculos = pygame.sprite.Group()
    escaleras = pygame.sprite.Group()
    intangibles = pygame.sprite.Group()

    trampas = pygame.sprite.Group()
    fondo = pygame.sprite.Group()
    lava = pygame.sprite.Group()
    vulnerables = pygame.sprite.Group()

    slimes = pygame.sprite.Group()
    sauruses = pygame.sprite.Group()
    eyebats = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()
    frogs = pygame.sprite.Group()

    enemigos = pygame.sprite.Group()

    balas_aliadas = pygame.sprite.Group()
    balas_enemigas = pygame.sprite.Group()
    boosters = pygame.sprite.Group()
    monedas = pygame.sprite.Group()

    scrolling = pygame.sprite.Group()

    #Información del mundo
    info_player = funciones.info_player(playerimg)#jugador
    info_world = funciones.info_world(enemyimg,itemimg)#mundos

    #Información del jugador
    player = funciones.Jugador(info_player,sounds)
    jugadores.add(player)
    barra_salud = funciones.Barra(info_player[-2],player.salud-1)
    salud.add(barra_salud)
    player.enemigos = enemigos
    player.obstaculos = obstaculos
    player.escaleras = escaleras

    for e in enemigos: e.obstaculos = obstaculos

    #Generadores del juego
    gen1 = [funciones.recortar(tilesimg,[datos.size*16,datos.size*2],[datos.size,datos.size]),funciones.recortar(tilesimg,[datos.size*17,datos.size*2],[datos.size,datos.size])]
    gen2 = [funciones.recortar(tilesimg,[datos.size*16,datos.size*2],[datos.size,datos.size]),funciones.recortar(tilesimg,[datos.size*18,datos.size*2],[datos.size,datos.size])]
    #generador = funciones.Vulnerable(eyegen,[14,3],1)
    #vulnerables.add(generador)
    inicio()
    if player.salud != 0 and player.quit == False:
        player.rect.x = datos.size
        player.rect.y = datos.size*8
        player.transcurso = 0
        pygame.mixer.music.load(datos.tutorialsong)
        pygame.mixer.music.play(3)
        pygame.mixer.music.set_volume(0.6)
        player.skip = False
        world(player,tilesimg,datos.tutorial,info_world,[gen1,gen2])
    if player.salud != 0 and player.quit == False:
        vaciar()
        player.transcurso = 1
        player.rect.x = 0
        player.rect.y = datos.size*2
        pygame.mixer.music.unload()
        pygame.mixer.music.load(datos.bg1)
        pygame.mixer.music.play(3)
        player.skip = False
        world(player,tilesimg,datos.mundouno,info_world,[gen1,gen2])
    if player.salud != 0 and player.quit == False:
        vaciar()
        player.transcurso = 1
        player.rect.x = 0
        player.rect.y = datos.size*6
        pygame.mixer.music.unload()
        pygame.mixer.music.load(datos.bg2)
        pygame.mixer.music.play(3)
        player.skip = False
        player.boss = 0
        world(player,tilesimg,datos.mundodos,info_world,[gen1,gen2])
    if player.salud != 0 and player.quit == False: victory(player)
