#HauptProgramm:
#Hier wird pygame initialisiert und
#die Sprite-gruppen auf die Display-Oberfläche gezeichnet.
#
#DesWeiteren befindet sich hier die Spielschleife. in der sämtliche Klassen geupdated werden
#from bin.lib.Player.Player import *
import pygame
from bin.config.generalCFG import *
# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_SIZE["X"], SCREEN_SIZE["Y"]))

#Stellt SmoothScale Filter für Skalierungen ein
if(SMOOTH_SCALE & SMOOTH_SCALE_ACCELERATION != 'AUTO'):
    pygame.transform.set_smoothscale_backend(SMOOTH_SCALE_ACCELERATION)

# Background
background = pygame.image.load(os.path.join(GAME_DIR, 'gfx', 'bg', '02', '02Full.png'))

# Caption and Icon
pygame.display.set_caption("Battle Castle")
icon = pygame.image.load(os.path.join(GAME_DIR, 'gfx', 'icon', 'castle.png'))
pygame.display.set_icon(icon)

# Create the player
#player = Player()





# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Exit Condition
running = True
#Main Game Loop
while running:

    # Set Bacjground
    screen.blit(background, (0, 0))

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  #  if event.type == pygame.KEYDOWN:
 #       if event.key == pygame.K_LEFT:
            #player.go_left()
#        if event.key == pygame.K_RIGHT:
            #player.go_right()
#        if event.key == pygame.K_UP:
            #player.jump()

#    if event.type == pygame.KEYUP:
 #       if event.key == pygame.K_LEFT and player.change_x < 0:
  #          player.stop()
   #     if event.key == pygame.K_RIGHT and player.change_x > 0:
    #        player.stop()



        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()








    # update Screen
    pygame.display.update()