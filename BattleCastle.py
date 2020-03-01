#Startpunkt: hiermit wird das Spiel gestartet
#Das Eigentliche Spiel befindet sich in der Klasse BattleCastle und kann hier einfach als Objekt erstellt werden und wie ein einzelnes SpriteObjekt verwendet werden
from bin.config.generalCFG import SCREEN_SIZE, ICON_PATH, VERSION

import pygame
from bin.lib.BattleCastle import BattleCastle

pygame.init()
size = [SCREEN_SIZE["X"], SCREEN_SIZE["Y"]]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("BattleCastle" + VERSION, "BC")
pygame.display.set_icon(pygame.image.load(ICON_PATH))
clock = pygame.time.Clock()
clock.tick(60)
bc = BattleCastle()

pygame.display.flip()

pygame.quit()