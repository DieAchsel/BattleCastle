#Konfiguration für den Level-Bereich. 
#Diese Datei beinhaltet Parameter für Level, Levelmanager und Tile
#[kleine Info] es handelt sich hierbei teils um dynamischen Content
import re, os, glob, string
from pygame.rect import Rect
from bin.config.generalCFG import SCREEN_SIZE, GAME_DIR



LOADING_SPINNER = "CUBES"

#-----------------------------Arena-Parameter-------------------------------
#Standardschicht, auf die die Arena gezeichnet wird
ARENA_LAYER_ID = 1 #(0 ist für den Hintergrund reserviert)

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
ARENA_AREA = Rect(ARENA_X_POS, ARENA_Y_POS, (round((SCREEN_SIZE["X"] * (ARENA_WIDTH_PERCENT / 100)),0), round((SCREEN_SIZE["Y"] * (ARENA_HEIGHT_PERCENT / 100)),0)))

#DEPRECATED-- (teilweise jedoch noch genutzt, muss unbedingt entfernt werden)
ARENA_SIZE = {
    "X": ARENA_AREA.w,
    "Y": ARENA_AREA.h
    }
ARENA_POSITION = (ARENA_AREA.x,ARENA_AREA.y)
#--DEPRECATED #diese Informationen werden nun in einem Rect gespeichert, was direkt der Arenaklasse zuordbar ist


#-----------------------allgemeines Level-Verhalten-------------------------
#Ersetzt beim Levelwechsel die surfaceObjekte im Raster durch ihre TypeID.
#spart RAM, jedoch muss das Level beim erneuten Laden neu gebaut (build()) werden
IS_UNBUILDING_ON_UNLOAD = True
IS_BUILD_ON_UPDATE = True #mit jedem UpdateProzess wird ein Tile gebaut.

#------------------------------Datei-Handling-------------------------------

#jede zu lesende Variable wird hier registriert
#wenn die Ausdrücke in der Datei nicht gefunden wurden oder unzulässig sind, werden Default-Werte verwendet
#Obige Bedingung wird für jede gesuchte Variable einzeln geprüft, ausser bei gridSize und grid (die beiden Daten stehen in direkter Beziehung)

LEVEL_DIR = os.path.join(GAME_DIR, 'lvl', '')


#------------------------------DEFAULT-Werte--------------------------------
DEFAULT_LOADING_SPINNER_PATH = os.path.join(GAME_DIR, "gfx", "loadingSpinner", LOADING_SPINNER, "spinner.gif")
#Standard-Texture-Set für Tile
DEFAULT_TILE_ID = 0   #0 = unsichtbar(wird beim level.build() in die spritegroup unusedTiles verschoben)
DEFAULT_TILE_GROUP_ID = 0
#Harming-Tiles:
DEFAULT_DMG_ON_COLLISION = 10
DEFAULT_DMG_OVER_TIME = 4
#DEFAULT_LVL_CONF_PARAMETERS_DIR = ""#os.path.join(GAME_DIR, "lvl")
DEFAULT_TEXTURE_SET_PATH = os.path.join(GAME_DIR, "gfx", "tiles", "default")

DEFAULT_TILE_CONF_PARAMETERS ={
    "ID": 0, #TileID
    "textureName": "", # Dateipfad zu entsprechender Textur (die untertexturen 000[_; -; #]0, 000[_; -; #]1, etc. werden aus diesem Namen bestimmt und per regex gesucht)
    "groupID": 1, # Tilegruppe (Tiles die für verchiedene Nachbar-Konstellationen eigene tiles haben werden zu einer Gruppe zusammengefasst, wenn nicht genutzt, leerlassen oder weglassen)
    "isclippable": True,
    "isAnimated": False, #wenn flag = false, dann werden weitere Texturen _1, _2 usw genutzt um aus diesen eine zufällige zu wählen
    "dmgNeededToDestroy": -1, #Schaden der benötigt wird um tile zu zerstören (in 000 umwandeln) -1 = unendlich
    "damageOnCollision": 0,
    "damageOverTime": 0,
    "layerID": 1, # Layer ID (0 liegt hinter dem Spieler, 1 auf Höhe des Spielers, 2 vor dem Spieler, usw.)
    "playMvSlowDown": 0, # reduzierung der Geschwindigkeit des betr. spielers bei collision um angegebenen Faktor
    "playerMvManipulation": [0,0], #on collision wird die bewegungsgeschwindigkeit und richtung des betr. Spielers entsprechend der X und Y werte geändert (wird weggeschubst)
    "preferredNeighborIDs": [[000,000,000],
                            [000,000,000],
                            [000,000,000]]
    }

DEFAULT_LVL_CONF_PARAMETERS = {
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

DEFAULT_GRID_SIZE = {
    "X": DEFAULT_LVL_CONF_PARAMETERS["maxWidth"],
    "Y": len(DEFAULT_LVL_CONF_PARAMETERS["grid"])}

DEFAULT_TILE_SIZE = { #statische TileSize berechnet von auf DEFAULT_LVL_CONF_PARAMETERS (nnur für Fallback auf DEFAULT)
    "X": ARENA_AREA.w // DEFAULT_GRID_SIZE["X"],
    "Y": ARENA_AREA.h // DEFAULT_GRID_SIZE["Y"]
}
DEFAULT_PLAYER_STARTPOS = [[1, (len(DEFAULT_LVL_CONF_PARAMETERS["grid"]) - 1)], [len(DEFAULT_LVL_CONF_PARAMETERS["maxWidth"]) - 1, DEFAULT_LVL_CONF_PARAMETERS["maxWidth"] - 2]] #NUR FÜR FALLBACK AUF DEFAULT
#--------------------------genutzte REGEX-Ausdrücke-------------------------
DATA_CONDITIONS_LVL = {
#    "gridSize": "^gridSize=[0-9]*;[0-9]*$", #DEPRECATED
    "difficulty": "^difficulty=[0-9]$",
    "playerStartPos": "^playerStartPos=(\(\d+;\d+\))+$",
    "grid": "^GRID=(\d\;)+\d$" #hier stimmt was nicht mehr, ich hab nur ein semikolon entfernt. zudem hat die regEx negative werte glaub ich übersprungen
}

VALUE_EXTRACTION_REGEX = "" #alles was buchstaben sind mit (: oder =) angehängt
TEXTURE_ID_BLOCK_REGEX = "ID:\d+\{*\}"

DATA_CONDITIONS_TILE ={
    "ID": "ID:\d+\{",
    "groupID": "groupID=\d+", # Tilegruppe (Tiles die für verchiedene Nachbar-Konstellationen eigene tiles haben werden zu einer Gruppe zusammengefasst, wenn nicht genutzt, leerlassen oder weglassen)
    "isclippable": "isclippable=[True | False]",
    "isAnimated": "isAnimated=[True | False]", #wenn flag = false, dann werden weitere Texturen _1, _2 usw genutzt um aus diesen eine zufällige zu wählen
    "dmgNeededToDestroy": "dmgNeededToDestroy=[ -1 | \d+]", #Schaden der benötigt wird um tile zu zerstören (in 000 umwandeln) -1 = unendlich
    "damageOnCollision": "damageOnCollision=\d+",
    "damageOverTime": "damageOverTime=\d+",
    "layerID": "layerID=\d+", # Layer ID (0 liegt hinter dem Spieler, 1 auf Höhe des Spielers, 2 vor dem Spieler, usw.)
    "playMvSlowDown": "playMvSlowDown=\d+", # reduzierung der Geschwindigkeit des betr. spielers bei collision um angegebenen Faktor
    "playerMvManipulation": "playerMvManipulation=\[\d+,\d+\]", #on collision wird die bewegungsgeschwindigkeit und richtung des betr. Spielers entsprechend der X und Y werte geändert (wird weggeschubst)
    "preferredNeighborIDs": "preferredNeighborIDs=\[(\[((\d+),?){3}\]){3}\]"
    }


#-------------------------------Default Level--------------------------------
#Werte, die genutzt werden, wenn es Probleme mit dem Laden der .lvl Dateien gibt
#DIESE WERTE DÜRFEN NICHT ZUR LAUFZEIT VERÄNDERT WERDEN! ES HANDELT SICH UM FALLBACK-DATEN
DEFAULT_BG_PATH = os.path.join(GAME_DIR, "gfx", "bg", "00", "Full.png")
