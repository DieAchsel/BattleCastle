#Startpunkt: hiermit wird das Spiel gestartet
#Das Eigentliche Spiel befindet sich in der Klasse BattleCastle und kann hier einfach als Objekt erstellt werden und wie ein einzelnes SpriteObjekt verwendet werden
import pygame
from bin.config.generalCFG import *
from bin.config.playerCFG import PLAYER_CONTROL
from bin.lib.BattleCastle import BattleCastle

pygame.init()

bc = BattleCastle.BattleCastle()

size = [SCREEN_SIZE["X"], SCREEN_SIZE["Y"]]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("BattleCastle" + VERSION, "BC")
pygame.display.set_icon(pygame.image.load(ICON_PATH))
clock = pygame.time.Clock()

#Main Game Loop
while True:
    # Handle Events
    print("TEST")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if event.type == pygame.KEYDOWN:
        if event.key == PLAYER_CONTROL[0]["UP"]:
            bc.player1.jump()
        if event.key == PLAYER_CONTROL[0]["RT"]:
            bc.player1.go_right()
        if event.key == PLAYER_CONTROL[0]["LT"]:
            bc.player1.go_left()
        if event.key == PLAYER_CONTROL[0]["FIRE"]:
            bc.player1.is_attack()

        if event.key == PLAYER_CONTROL[1]["UP"]:
            bc.player2.jump()
        if event.key == PLAYER_CONTROL[1]["RT"]:
            bc.player2.go_right()
        if event.key == PLAYER_CONTROL[1]["LT"]:
            bc.player2.go_left()
        if event.key == PLAYER_CONTROL[1]["FIRE"]:
            bc.player2.is_attack()

    if event.type == pygame.KEYUP:
        if event.key == PLAYER_CONTROL[0]["RT"]:
            bc.player1.stop()
        if event.key == PLAYER_CONTROL[0]["LT"]:
            bc.player1.stop()

        if event.key == PLAYER_CONTROL[1]["RT"]:
            bc.player2.stop()
        if event.key == PLAYER_CONTROL[1]["LT"]:
            bc.player2.stop()

    bc.update()

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    bc.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    clock.tick(FPS)

    pygame.display.flip()

    pygame.quit()