#Parameter und Variablen zu leveln
#es handelt sich hierbei um dynamischen Content
from bin.config.generalCFG import SCREEN_SIZE
DEFAULT_LAYER_ID = 1 #Die Standardschicht, auf die ein level gezeichnet werden soll
DEFAULT_TILE_SIZE = {
    "X": 64,
    "Y": 64}
DEFAULT_GRID_SIZE = {
    "X": 32,
    "Y": 32}
ARENA_SIZE = {
    "X": SCREEN_SIZE["X"]*1.0,
    "Y": SCREEN_SIZE["Y"]* 0.95}

DEFAULT_DMG_ON_COLLISION = 10
DEFAULT_DMG_OVER_TIME = 4