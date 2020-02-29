#Konfiguration für den Level-Bereich. 
#Diese Datei beinhaltet Parameter für Level, Levelmanager und Tile
#[kleine Info] es handelt sich hierbei teils um dynamischen Content
import re, os, glob, string
from pygame.rect import Rect
from bin.config.generalCFG import SCREEN_SIZE, GAME_DIR


#-----------------------------Arena-Parameter-------------------------------
#Standardschicht, auf die die Arena gezeichnet wird
DEFAULT_LAYER_ID = 1 #(0 ist für den Hintergrund reserviert)

#Größe und Position der Arena
    #Die Arena-Area wird mit relativen Größen (in beziehung zu SCREEN_SIZE in generalCFG.py) positioniert
        #Bei Breiten unter 100% wird die PlayArea zentriert
        #Bei Höhen unter 100% erhält die StatusArea ( über statusAreaCFG.py in Beziehung mit ARENA_HEIGHT_PERCENT) einen eigenen Bereich
        #Bei Höhen von 100% erhält die StatusArea ( über statusAreaCFG.py in Beziehung mit ARENA_HEIGHT_PERCENT) einen Bereich im nächsten Layer und der statusArea-Hintergrund wird deaktiviert
ARENA_HEIGHT_PERCENT = 80 #Bei Größen unter 100% wird der freie Bereich (unten angefügt) für die StatusArea genutzt
ARENA_WIDTH_PERCENT = 100 #Bei Größen unter 100% wird Arena auf der Display-Surface zentriert
#Position auf der Display-Surface
ARENA_X_POS = round(((SCREEN_SIZE["X"]/100) * (100 - ARENA_WIDTH_PERCENT)),0)
ARENA_Y_POS = 0
#Rect mit sämtlichen Informationen (in Pixel übersetzt) für Programm-Zugriff
ARENA_AREA = Rect(ARENA_X_POS, ARENA_Y_POS, round((SCREEN_SIZE["X"] * (ARENA_WIDTH_PERCENT / 100)),0), round((SCREEN_SIZE["Y"] * (ARENA_HEIGHT_PERCENT / 100)),0))

#DEPRECATED--
ARENA_SIZE = {
    "X": SCREEN_SIZE["X"]*1.0,
    "Y": SCREEN_SIZE["Y"]* 0.95
    }
ARENA_POSITION = (0,0)
#--DEPRECATED

#-----------------------------Tile-Parameter--------------------------------
#Standard-tile-typ, wenn kein tile-typ zugeordnet werden kann (sollte nicht passieren)
DEFAULT_TILE_ID = 0   #0 = unsichtbar(wird beim level.build() in die spritegroup unusedTiles verschoben)

TILE_ID_RANGE_MAP = {
    "harmful_collidable": {"first": 51, "last": 100},
    "collidable": {"first": 1, "last": 50},
    "empty": 0,
    "uncollidable": {"first": -50, "last": -1},
    "harmful_uncollidable": {"first": -100, "last": -51}
}

#Standard-Texture-Set für Tile
DEFAULT_TEXTURE_SET_PATH = os.path.join(GAME_DIR, "gfx", "tiles", "default")

#Harming-Tiles:
DEFAULT_DMG_ON_COLLISION = 10
DEFAULT_DMG_OVER_TIME = 4

#-----------------------allgemeines Level-Verhalten-------------------------
#Ersetzt beim Levelwechsel die surfaceObjekte im Raster durch ihre TypeID. 
#spart RAM, jedoch muss das Level beim erneuten Laden neu gebaut (build()) werden
IS_UNBUILDING_ON_UNLOAD = True
IS_BUILD_ON_UPDATE = True #mit jedem UpdateProzess wird ein Tile gebaut. 
#------------------------------Datei-Handling-------------------------------
#RegEx Ausdrücke zum Parsen der .lvl Dateien
#jede zu lesende Variable wird hier registriert
#wenn die Ausdrücke in der Datei nicht gefunden wurden oder unzulässig sind, werden Default-Werte verwendet
#Obige Bedingung wird für jede gesuchte Variable einzeln geprüft, ausser bei gridSize und grid (die beiden Daten stehen in direkter Beziehung)
DATA_CONDITIONS = {
#    "gridSize": "^gridSize=[0-9]*;[0-9]*$",
    "difficulty": "^difficulty=[0-9]$",
    "playerStartPos": "^playerStartPos=(\(\d+;\d+\))+$",
    "grid": "^GRID=(([\d+|-\d+]+)+)$" #hier stimmt was nicht mehr, ich hab nur ein semikolon entfernt. zudem hat die regEx negative werte glaub ich übersprungen
}
LEVEL_DIR = os.path.join(GAME_DIR, 'lvl', '')

#-------------------------------Default Level--------------------------------
#Werte, die genutzt werden, wenn es Probleme mit dem Laden der .lvl Dateien gibt
DEFAULT_TEXTURE_PATH = os.path.join(GAME_DIR, "gfx", "tiles", "00")
DEFAULT_BG_PATH = os.path.join(GAME_DIR, "gfx", "bg", "00", "Full.png")
DEFAULT_DIFFICULTY = 0



#In zukunft ein defaultGrid anhand der oberen defaultinformationen generieren
DEFAULT_LVL = { 
    "title" : "default Level",
    "difficulty" : 0,
    "grid": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
    "maxWidth" : 32}

DEFAULT_TILE_SIZE = {
"X": ARENA_AREA.w // DEFAULT_LVL["maxWidth"],
"Y": ARENA_AREA.h // len(DEFAULT_LVL["grid"])
}
DEFAULT_PLAYER_STARTPOS = [[1, (len(DEFAULT_LVL["grid"]) - 1)], [len(DEFAULT_LVL["maxWidth"]) - 1, DEFAULT_LVL["maxWidth"] - 2]]