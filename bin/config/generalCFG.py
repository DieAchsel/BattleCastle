#generelle Imports hier einfügen
import os
import pygame
# Absoluter Pfad zum bin-Ordner
GAME_DIR = (os.path.join(os.path.dirname(os.path.dirname(__file__))))
#globaler Colorkey
COLORKEY = (0,255,0)#giftgrün (wird normalerweise nicht verwendet)
MISSING_TEXTURE_COLOR = (255,0,0) # Anstelle von fehlenden Texturen wird diese Farbe angezeigt
#Fenster-Auflösung
SCREEN_SIZE = {
    "X": 1280,
    "Y": 720
}


#SMOOTH_SCALE wählt genutzte Methode zum Skalieren von Oberflächen, True für Smoothscale Methode
#Smoothscale liefert ein besseres Ergebnis als scale, ist aber auch langsamer
#weitere Infos hier: https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale
SMOOTH_SCALE = True
SMOOTH_SCALE_FILTER = 'GENERIC' #'GENERIC', 'MMX', oder 'SSE' möglich




# Spezieldatentypen hier nachgucken: https://www.w3schools.com/python/python_dictionaries.asp