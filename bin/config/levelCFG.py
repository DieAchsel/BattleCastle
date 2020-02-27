#Konfiguration für den Level-Bereich. 
#Dieser beinhaltet Level, Levelmanager und Tile
#[kleine Info] es handelt sich hierbei teils um dynamischen Content
from pygame.rect import Rect
from bin.config.generalCFG import SCREEN_SIZE
DEFAULT_LAYER_ID = 1 #Die Standardschicht, auf die ein Tile gezeichnet werden soll (0 ist für den Hintergrund)
DEFAULT_TILE_SIZE = {
    "X": 64,
    "Y": 64
    }
DEFAULT_GRID_SIZE = {
    "X": 32,
    "Y": 32
    }
#Größe und Position der Arena
#Die Arena-Area wird mit relativen Größen (in beziehung zu SCREEN_SIZE in generalCFG.py) positioniert
#Bei Breiten unter 100% wird die PlayArea zentriert
#Bei Höhen unter 100% erhält die StatusArea ( über statusAreaCFG.py in Beziehung mit ARENA_HEIGHT_PERCENT)
ARENA_HEIGHT_PERCENT = 80 #der Rest geht an den Statusbereich über
ARENA_WIDTH_PERCENT = 100
ARENA_X_POS = round((SCREEN_SIZE["X"]/100) * (100 - ARENA_WIDTH_PERCENT), 0)
ARENA_Y_POS = 0
ARENA_AREA = Rect(ARENA_X_POS, ARENA_Y_POS, SCREEN_SIZE["X"] * (ARENA_WIDTH_PERCENT / 100), SCREEN_SIZE["Y"] * (ARENA_HEIGHT_PERCENT / 100))

#DEPRECATED--
ARENA_SIZE = {
    "X": SCREEN_SIZE["X"]*1.0,
    "Y": SCREEN_SIZE["Y"]* 0.95
    }
ARENA_POSITION = (0,0)
#--DEPRECATED

DEFAULT_DMG_ON_COLLISION = 10
DEFAULT_DMG_OVER_TIME = 4