#generelle Imports hier einfügen
import os
import pygame
# Absoluter Pfad zum bin-Ordner
GAME_DIR = (os.path.join("..", os.path.dirname(__file__)))

#Fenster-Auflösung
screenSize = {
    "X": 1280,
    "Y": 720}
#globaler Colorkey
COLORKEY = (0,255,0)#giftgrün (wird normalerweise nicht verwendet)
MISSING_TEXTURE_COLOR = (255,0,0) # Anstelle von fehlenden Texturen wird diese Farbe angezeigt
#Folgende Variablen vllt in playerConfig einfügen
playerSize = {
    "X": 7,
    "Y": 14}
player1Keys = {
    "UP": "W",
    "DN": "S",
    "RT": "D",
    "LT": "A",
    "aimRT": "E", 
    "aimLT": "Q",
    "FIRE": "lALT"}
player2Keys = {
    "UP": "NUM8",
    "DN": "NUM5",
    "RT": "NUM6",
    "LT": "NUM4",
    "aimRT": "NUM9", 
    "aimLT": "NUM7",
    "FIRE": "NUM,"}
runningSpeed = 50 #Laufgeschwindigkeit der Charaktere
fallingSpeedMultiplier = 1.0
jumpHeight = 20 #Skalierung der Map wird aufgerechnet


# Spezieldatentypen hier nachgucken: https://www.w3schools.com/python/python_dictionaries.asp