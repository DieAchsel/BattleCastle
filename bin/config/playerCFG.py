from pygame.constants import *
from bin.config.generalCFG import *
# Dir with Images of all playable Characters
PLAYER_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gfx', 'char')

# Dictionary whit playable Characters
CHARACTERS = {
    1: os.path.join(PLAYER_IMAGES_DIR, '01_Woodcutter'),
    2: os.path.join(PLAYER_IMAGES_DIR, '02_GraveRobber'),
    3: os.path.join(PLAYER_IMAGES_DIR, '03_SteamMan')
}

PLAYER_SIZE = {
    "X": 30,
    "Y": 30}

#In zukunft soll man aus dem Menü Tastenbelegungen ändern können. dazu sollten die Tastenbelegungen ggfs in eine .txt ausgelagert werden
PLAYER_CONTROL = [{
    "UP": K_w,
    "DN": K_s,
    "RT": K_d,
    "LT": K_a,
    "AIM_RT": K_e,
    "AIM_LT": K_q,
    "FIRE": K_LALT
}, {
    "UP": K_KP8,
    "DN": K_KP5,
    "RT": K_KP6,
    "LT": K_KP4,
    "AIM_RT": K_KP9,
    "AIM_LT": K_KP7,
    "FIRE": K_KP_PERIOD}]

# Laufgeschwindigkeit der Charaktere
RUNNING_SPEED = 5

FALLING_SPEED_MULTIPLIER = 1.0

# Skalierung der Map wird aufgerechnet
JUMP_HEIGHT = 20

# Sequence Frames

# Spezieldatentypen hier nachgucken: https://www.w3schools.com/python/python_dictionaries.asp
FRAMES_PER_SEQUENCE = 18
