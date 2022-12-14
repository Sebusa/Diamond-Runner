import configparser

#Leer el archivo
archivo = configparser.ConfigParser()
archivo.read('Recursos/datos.txt')
secciones = archivo.sections()

#Propiedades de la pantalla
ancho = int(archivo.get('pantalla','ancho'))
alto = int(archivo.get('pantalla','alto'))
FPS = int(archivo.get('pantalla','fps'))
size = int(archivo.get('recursos','size'))
psize = int(archivo.get('recursos','player_size'))

#jugador y componentes
playerimg = archivo.get('recursos','playerimg')
enemyimg = archivo.get('recursos','enemyimg')
itemimg = archivo.get('recursos','itemimg')
tilesimg = archivo.get('recursos','tiles')
GAMEOVER = archivo.get('recursos','GO')
WIN = archivo.get('recursos','WIN')

#Sonido
jump = archivo.get('sounds','jumping')
shoot = archivo.get('sounds','shoot')
pickup = archivo.get('sounds','pickup')
coin = archivo.get('sounds','coin')
gameover = archivo.get('sounds','gameover')
enemyhit = archivo.get('sounds','edeath')
playerhit = archivo.get('sounds','hit')
win = archivo.get('sounds','win')
explosion = archivo.get('sounds','explosion')
newlife = archivo.get('sounds','newlife')

#musica
tutorialsong = archivo.get('sounds','tutorial')
bg1 = archivo.get('sounds','one')
bg2 = archivo.get('sounds','two')
boss1 = archivo.get('sounds','boss1')
boss2 = archivo.get('sounds','boss2')

#mapas
tutorial = archivo.get('mapas','tutorial')
mundouno = archivo.get('mapas','one')
mundodos = archivo.get('mapas','two')
tiles = archivo.get('mapas','tiles')
