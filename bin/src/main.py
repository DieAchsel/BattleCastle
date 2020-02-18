from bin.src.classPlayer import *


game_folder = os.path.dirname(__file__)

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720



# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load(os.path.join('../img/bg/02', '02Full.png'))

# Caption and Icon
pygame.display.set_caption("Battle Castle")
icon = pygame.image.load(os.path.join('../img/icon', 'castle.png'))
pygame.display.set_icon(icon)

# Create the player
player = Player()





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

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player.go_left()
        if event.key == pygame.K_RIGHT:
            player.go_right()
        if event.key == pygame.K_UP:
            player.jump()

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and player.change_x < 0:
            player.stop()
        if event.key == pygame.K_RIGHT and player.change_x > 0:
            player.stop()



        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()








    # update Screen
    pygame.display.update()