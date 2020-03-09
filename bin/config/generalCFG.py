#generelle Imports hier einfügen
import os
import pygame
import time



VERSION = "0.1.2"
NULL_TYPE = None
ANIMATION_INTERVAL = 30 #jedes 30te Update wird die bildsequenz iteriert
if(pygame.image.get_extended()):
    AVAILABLE_IMG_FORMAT_REGEX = "[png|gif|jpg|bmp|pcx|tga|tif|lbm|pbm|pgm|ppm|xpm]"
else:
    AVAILABLE_IMG_FORMAT_REGEX = "[BMP]"
# Absoluter Pfad zum bin-Ordner
GAME_DIR = (os.path.join(os.path.dirname(os.path.dirname(__file__))))
DEBUG_ENABLED = True
DEBUG_LEVEL = 13
DELAY_ON_DEBUG = 0 #gibt ein Delay in s (darf float sein) an, wie lang nach jeder DEBUGGING-Nachricht gewartet werden soll.
ON_DEBUG_USER_CONTINUES = False #wenn ein kontinueKey (pygame.event) angegeben ist, wird bis zur Eingabe von Enter gewartet.

LOG_FILE = True
#Wenn DEBUG_ENABLED, dann gib Debuggingmeldungen aus, je nach lvl mit angepasstem Detail
#wie detailliert sollen die Meldungen sein. bei DEBUG_LEVEL >= 12 wird je nach integrierung jede Daten-Transaktion in der Konsole ausgegeben
#Debugging-Funktion:
logOpened = bool
logFile = open(os.path.join(GAME_DIR, "DEBUG.log"), 'a')
def DEBUG(msg = "Meldung ohne Inhalt", debugLevel = 0, ObjectToPrint = NULL_TYPE):
    from bin.config.generalCFG import logOpened, logFile
    if(DEBUG_ENABLED):  
        spacing = ""  
        tabs = "    " 
        output_prefix = "DEBUGGING: " + time.strftime("%H:%M:%S") + "   "
        output = []    
        for x in range(debugLevel): #Rücke Meldungen in tieferem Layer ein
            spacing += tabs
        output.append(output_prefix + spacing + msg)
        if(ObjectToPrint != NULL_TYPE): 
            output.append(output_prefix + spacing + tabs + str(ObjectToPrint))
        if(DELAY_ON_DEBUG > 0):
            output.append(output_prefix + spacing + tabs + "Warte auf Bestätigung")
        if(debugLevel <= DEBUG_LEVEL):     
            if(DELAY_ON_DEBUG > 0):
                time.sleep(DELAY_ON_DEBUG)
            if(ON_DEBUG_USER_CONTINUES):
                output.append(output_prefix + spacing + tabs + "Nutzer-Eingabe: '" + input() + "'")
            for x in output:
                print(x)
                if(LOG_FILE):
                    logFile.write((x + "\n"))
                    logFile.flush()

                    
ICON_PATH = os.path.join(GAME_DIR, "gfx", "icon", "castle.png")
#Fenster-Auflösung
SCREEN_SIZE = {
    #"X": 1280,
    #"Y": 720
    "X": 900,
    "Y": 500
}

FPS = 60

#-------------------------------------Render-Optionen--------------------------------------------------

#SMOOTH_SCALE wählt genutzte Methode zum Skalieren von Oberflächen, True für Smoothscale Methode
#Smoothscale liefert ein besseres Ergebnis als scale, ist aber auch langsamer
#weitere Infos hier: https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale
SCALING = True # schaltet Skalierung der Tiles ein
SMOOTH_SCALE = True 
#SmoothScale Beschleunigung 
SMOOTH_SCALE_ACCELERATION = 'AUTO' #'AUTO', 'GENERIC' (Ohne Bescheunigung), 'MMX' (mit MMX Instruktionen), 'SSE' (MMX + SSE Erweiterung)
#Zum Release sollte für SMOOTH_SCALE_FILTER 'AUTO' genutzt werden, um den unterstützten Modus automatisch zu ermitteln

#--------------------------------------Image-Optionen--------------------------------------------------

#
COLORKEY = (0,255,0)#giftgrün (wird normalerweise nicht verwendet)
MISSING_TEXTURE_COLOR = (255,0,0) # Anstelle von fehlenden Texturen wird diese Farbe angezeigt



