from bin.config.levelCFG import ARENA_AREA
from bin.config.playerCFG import *
import glob


# Class for playable Characters
class Player(pygame.sprite.Sprite):
    """Constructor"""

    def __init__(self, playerChar, isLookingToTheRight):
        super().__init__()

        # Sequences
        self.rtRun = []
        self.ltRun = []
        self.rtJump = []
        self.ltJump = []
        self.rtHurt = []
        self.ltHurt = []
        self.rtDeath = []
        self.ltDeath = []
        self.rtAttack1Seq = []
        self.ltAttack1Seq = []

        self.frameInSequence = 0

        self.characterImageDir = CHARACTERS[playerChar]
        self.init_sequences()

        # Damit sich beide opponenten initial ansehen wird hier die Blick-Richtung festgelegt
        if isLookingToTheRight:
            startImage = self.rtStand
            self.right = True
            self.left = False
        else:
            startImage = self.ltStand
            self.right = False
            self.left = True

        # todo load image
        self.image = startImage
        self.rect = self.image.get_rect()

        # Player Speed
        self.speed_x = 0
        self.speed_y = 0

        self.level = None

    def go_left(self):
        self.speed_x = -RUNNING_SPEED
        self.left = True
        self.right = False

    def go_right(self):
        self.speed_x = RUNNING_SPEED
        self.left = False
        self.right = True

    def stop(self):
        self.speed_x = 0

    def jump(self):
        #self.rect.y += 2
        #list_hit_platform = pygame.sprite.spritecollide(self, self.level.platformlist, False)
        #self.rect.y -= 2
        #if (len(list_hit_platform)) > 0 or self.rect.bottom >= SCREEN_SIZE["Y"]:
        self.speed_y = -JUMP_HEIGHT

    def gravity(self):
        """Effect of gravity"""
        if self.speed_y == 0:
            self.speed_y = 1
        else:
            self.speed_y += 1.3

        if self.rect.y >= SCREEN_SIZE["Y"] - self.rect.height and self.speed_y >= 0:
            self.speed_y = 0
            self.rect.y = SCREEN_SIZE["Y"] - self.rect.height

    def update(self):
        # todo gravity
        self.gravity()
        # Moving
        self.rect.x += self.speed_x
        # Jumping
        self.rect.y += self.speed_y

        if self.rect.x < 0:
            self.rect.x = SCREEN_SIZE["X"]
            #self.rect.x = ARENA_AREA.x
        elif self.rect.x > SCREEN_SIZE["X"]:
            self.rect.x = 0
            #self.rect.x = ARENA_AREA.y


        # Animation sequence
        if self.frameInSequence + 1 >= FRAMES_PER_SEQUENCE:
            self.frameInSequence = 0

        # Running to the left animation
        if self.left and self.speed_x != 0:
            self.set_animation_sequence(self.ltRun)
        # Running to the right animation
        elif self.right and self.speed_x != 0:
            self.set_animation_sequence(self.rtRun)
        # Jumping to the left animation
        elif self.left and self.speed_y != 0:
            self.set_animation_sequence(self.ltJump)
        # Jumping to the right animation
        elif self.right and self.speed_y != 0:
            self.set_animation_sequence(self.rtJump)
        # TODO -> see comments below
        # Attack to the left animation

        # Attack to the left animation

        # Hurt looking to the left

        # Hurt looking to the right

        # Death looking to the left

        # Death looking to the right

        # Stand looking to the left
        if self.left and self.speed_x == 0 and self.speed_y == 0:
            self.image = self.ltStand
        # Stand looking to the right
        elif self.right and self.speed_x == 0 and self.speed_y == 0:
            self.image = self.rtStand



    def init_sequences(self):
        """Initialize animation sequences"""
        # Attack animation sequence
        for image in self.get_images_from_dir('Attack1', 'LT'):
            self.ltAttack1Seq.append(pygame.image.load(image))

        for image in self.get_images_from_dir('Attack', 'RT'):
            self.rtAttack1Seq.append(pygame.image.load(image))

        # Death animation sequence
        for image in self.get_images_from_dir('Death', 'LT'):
            self.ltDeath.append(pygame.image.load(image))

        for image in self.get_images_from_dir('Death', 'RT'):
            self.rtDeath.append(pygame.image.load(image))

        # Hurt animation sequence
        for image in self.get_images_from_dir('Hurt', 'LT'):
            self.ltHurt.append(pygame.image.load(image))

        for image in self.get_images_from_dir('Hurt', 'RT'):
            self.rtHurt.append(pygame.image.load(image))

        # Jump animation sequence
        for image in self.get_images_from_dir('Jump', 'LT'):
            self.ltJump.append(pygame.image.load(image))

        for image in self.get_images_from_dir('Jump', 'RT'):
            self.rtJump.append(pygame.image.load(image))

        # Run sequence
        for image in self.get_images_from_dir('Run', 'LT'):
            self.ltRun.append(pygame.image.load(image))

        for image in self.get_images_from_dir('Run', 'RT'):
            self.rtRun.append(pygame.image.load(image))

        # Stand Image
        self.ltStand = pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'StandLT.png'))

        self.rtStand = pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'StandRT.png'))

    def get_images_from_dir(self, sequenceDir, sequenceDirection):
        """Returns the List of paths, of Images in an specific sequence directory (sequenceDir),
         in one direction (sequenceDirection = Left(LT) or Right(RT))"""
        listImagePath = glob.glob(os.path.join(self.characterImageDir, sequenceDir, '') +
                                  sequenceDirection + '[0-9][0-9].png')
        listImagePath.sort()
        return listImagePath

    def set_animation_sequence(self, listOfImages):
        """Calculates the frames per Image and set an image every (Calculated Frame)"""
        #self.image.blit(listOfImages[self.frameInSequence // (FRAMES_PER_SEQUENCE // len(listOfImages))], (0,0))
        self.image = listOfImages[self.frameInSequence // (FRAMES_PER_SEQUENCE // len(listOfImages))]
        self.frameInSequence += 1

