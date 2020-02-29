from pygame.rect import Rect
from bin.config.generalCFG import SCREEN_SIZE
from bin.config.levelCFG import ARENA_HEIGHT_PERCENT, ARENA_WIDTH_PERCENT, ARENA_AREA

#Größe und Position der StatusArea
STATUS_HEIGHT_PERCENT = 100 - ARENA_HEIGHT_PERCENT
STATUS_WIDTH_PERCENT = 100 #mit ARENA_WIDTH_PERCENT an Arena koppelbar
STATUS_X_POS = round(((SCREEN_SIZE["X"] / 100) * (100 - STATUS_WIDTH_PERCENT)),0)
STATUS_Y_POS = ARENA_AREA.bottom
STATUS_AREA = Rect(STATUS_X_POS, STATUS_Y_POS, round((SCREEN_SIZE["X"] * (STATUS_WIDTH_PERCENT / 100)),0), round((SCREEN_SIZE["Y"] * (STATUS_HEIGHT_PERCENT / 100)),0))

if(STATUS_HEIGHT_PERCENT == 0):    #Wechsle Layer wenn auf Layer 1 kein Platz mehr
    DEFAULT_LAYER = 2
    HAS_BACKGROUND = False
else:
    DEFAULT_LAYER = 1
    HAS_BACKGROUND = True

BG_RASTERSIZE = [32,32] #hier eine Rechnung ermitteln, die die rastergröße anhand der texturgroße der tiles ermittelt