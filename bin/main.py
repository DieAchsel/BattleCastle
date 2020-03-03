#HauptProgramm:
#Hier wird pygame initialisiert und
#die Sprite-gruppen auf die Display-Oberfläche gezeichnet.
#
#Desweiteren befindet sich hier die Spielschleife. in der sämtliche Klassen geupdated werden
from bin.lib.Player.Player import *
# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_SIZE["X"], SCREEN_SIZE["Y"]))

#Stellt SmoothScale Filter für Skalierungen ein
if SMOOTH_SCALE != 'AUTO' and SMOOTH_SCALE_ACCELERATION != 'AUTO':
    pygame.transform.set_smoothscale_backend(SMOOTH_SCALE_ACCELERATION)

# Background
background = pygame.image.load(os.path.join(GAME_DIR, 'gfx', 'bg', 'default', 'Full.png'))

# Caption and Icon
pygame.display.set_caption("Battle Castle")
icon = pygame.image.load(os.path.join(GAME_DIR, 'gfx', 'icon', 'castle.png'))
pygame.display.set_icon(icon)

# Create the player
player = Player(2, True)
player2 = Player(3, False)

player.rect.x = 200
player.rect.y = SCREEN_SIZE["Y"] - player.rect.height

player2.rect.x = 400
player2.rect.y = SCREEN_SIZE["Y"] - player.rect.height

active_sprite_list = pygame.sprite.Group()
active_sprite_list.add(player)
active_sprite_list.add(player2)



# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Main Game Loop
while True:

    # Set Background
    screen.blit(background, (0, 0))

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == PLAYER_CONTROL[0]["UP"]:
                player.jump()
            if event.key == PLAYER_CONTROL[0]["RT"]:
                player.go_right()
            if event.key == PLAYER_CONTROL[0]["LT"]:
                player.go_left()
            if event.key == PLAYER_CONTROL[0]["FIRE"]:
                player.is_attack()

            if event.key == PLAYER_CONTROL[1]["UP"]:
                player2.jump()
            if event.key == PLAYER_CONTROL[1]["RT"]:
                player2.go_right()
            if event.key == PLAYER_CONTROL[1]["LT"]:
                player2.go_left()
            if event.key == PLAYER_CONTROL[1]["FIRE"]:
                player2.is_attack()

        if event.type == pygame.KEYUP:
            if event.key == PLAYER_CONTROL[0]["RT"]:
                player.stop()
            if event.key == PLAYER_CONTROL[0]["LT"]:
                player.stop()
            if event.key == PLAYER_CONTROL[0]["FIRE"]:
                player.not_attack()

            if event.key == PLAYER_CONTROL[1]["RT"]:
                player2.stop()
            if event.key == PLAYER_CONTROL[1]["LT"]:
                player2.stop()
            if event.key == PLAYER_CONTROL[1]["FIRE"]:
                player2.not_attack()

    active_sprite_list.update()




    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    active_sprite_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT





    # Limit to 60 frames per second
    clock.tick(FPS)
    # update Screen
    pygame.display.update()