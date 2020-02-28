#generelle Imports hier einfügen
import os
import pygame
# Absoluter Pfad zum bin-Ordner
GAME_DIR = (os.path.join(os.path.dirname(os.path.dirname(__file__))))
#Fenster-Auflösung
SCREEN_SIZE = {
    #"X": 1280,
    #"Y": 720
    "X" : 500,
    "Y" : 500
}

FPS = 60


#-------------------------------------Render-Optionen--------------------------------------------------

#SMOOTH_SCALE wählt genutzte Methode zum Skalieren von Oberflächen, True für Smoothscale Methode
#Smoothscale liefert ein besseres Ergebnis als scale, ist aber auch langsamer
#weitere Infos hier: https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale
SMOOTH_SCALE = True 
#SmoothScale Beschleunigung 
SMOOTH_SCALE_ACCELERATION = 'AUTO' #'AUTO', 'GENERIC' (Ohne Bescheunigung), 'MMX' (mit MMX Instruktionen), 'SSE' (MMX + SSE Erweiterung)
#Zum Release sollte für SMOOTH_SCALE_FILTER 'AUTO' genutzt werden, um den unterstützten Modus automatisch zu ermitteln

#--------------------------------------Image-Optionen--------------------------------------------------

#
COLORKEY = (0,255,0)#giftgrün (wird normalerweise nicht verwendet)
MISSING_TEXTURE_COLOR = (255,0,0) # Anstelle von fehlenden Texturen wird diese Farbe angezeigt



