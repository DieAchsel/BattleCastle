#generelle Imports hier einfügen
import os
import pygame


VERSION = "0.1.1"
NULL_TYPE = 0
ANIMATION_INTERVAL = 30 #jedes 30te Update wird die bildsequenz iteriert
if(pygame.image.get_extended()):
    AVAILABLE_IMG_FORMAT_REGEX = "[png|gif|jpg|bmp|pcx|tga|tif|lbm|pbm|pgm|ppm|xpm]"
else:
    AVAILABLE_IMG_FORMAT_REGEX = "[BMP]"
# Absoluter Pfad zum bin-Ordner
GAME_DIR = (os.path.join(os.path.dirname(os.path.dirname(__file__))))
DEBUG_ENABLED = True
DEBUG_LEVEL = 9
#Wenn DEBUG_ENABLED, dann gib Debuggingmeldungen aus, je nach lvl mit angepasstem Detail
#wie detailliert sollen die Meldungen sein. bei DEBUG_LEVEL >= 9 wird nach möglichkeit jede Daten-Transaktion in der Konsole ausgegeben
#Debugging-Funktion:
def DEBUG(msg = "Meldung ohne Inhalt", debugLevel = 0, ObjectToPrint = NULL_TYPE):
    if(DEBUG_ENABLED):
        if(debugLevel >= DEBUG_LEVEL):
            tabs = ""
            for x in range(debugLevel):
                #Rücke Meldungen in tieferem Layer ein
                tabs += "    "
            output = "DEBUGGING: " + tabs + msg

            if(ObjectToPrint != NULL_TYPE): 
                objectOutput = "\nEnthaltenes Objekt:\n" + str(ObjectToPrint)
                output += objectOutput
            print(output)
#Wenn DEBUG_ENABLED, gib diese Nachricht aus:

DEBUG("********************Debugging Aktiv********************\nSpiel-Version = " + str(VERSION) + "\nSpielverzeichnis = " + GAME_DIR + "\nDebug-Level = " + str(DEBUG_LEVEL) + "\n\n\n")


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



