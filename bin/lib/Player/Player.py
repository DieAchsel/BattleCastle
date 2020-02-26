from bin.config.playerCFG import *


# Class for playable Characters
class Player(pygame.sprite.Sprite):
    """Constructor"""

    def __init__(self, playerChar, isLookingToTheRight):
        super().__init__()

        characterImageDir = CHARACTERS[playerChar]
        self.init_sequences()

        # Damit sich beide opponenten initial ansehen wird hier die Blick-Richtung festgelegt
        if isLookingToTheRight:
            standImage = "StandRT.png"
        else:
            standImage = "StandLT.png"

        self.image = pygame.Surface([PLAYER_SIZE["X"], PLAYER_SIZE["Y"]])
        self.rect = self.image.get_rect()
        character_image = pygame.image.load(os.path.join(characterImageDir, 'Stand', standImage))
        self.image.blit(character_image, (0, 0), self.rect)

        self.speed_x = 0
        self.speed_y = 0

        self.level = None

    def go_left(self):
        self.speed_x = -RUNNING_SPEED

    def go_right(self):
        self.speed_x = RUNNING_SPEED

    def stop(self):
        self.speed_x = 0

    def jump(self):
        self.rect.y += 2
        list_hit_platform = pygame.sprite.spritecollide(self, self.level.platformlist, False)
        self.rect.y -= 2
        if (len(list_hit_platform)) > 0 or self.rect.bottom >= SCREEN_SIZE["Y"]:
            self.speed_y = -JUMP_HEIGHT

    def gravity(self):
        if self.speed_y == 0:
            self.speed_y = 1
        else:
            self.speed_y = 1.1

        if self.rect.y >= SCREEN_SIZE["Y"] - self.rect.height and self.speed_y >= 0:
            self.speed_y = 0
            self.rect.y = SCREEN_SIZE["Y"] - self.rect.height

    def update(self):
        pass

    def init_sequences(self):
        # Attack animation sequence
        self.ltAttack1Seq = [pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT01.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT02.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT03.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT04.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT05.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'LT06.png')), ]

        self.rtAttack1Seq = [pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT01.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT02.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT03.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT04.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT05.png')),
                             pygame.image.load(os.path.join(self.characterImageDir, 'Attack1', 'RT06.png')), ]

        # Death animation sequence
        self.ltDeath = [pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT01.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT02.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT03.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT04.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT05.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'LT06.png')), ]

        self.rtDeath = [pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT01.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT02.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT03.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT04.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT05.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Death', 'RT06.png')), ]

        # Hurt animation sequence
        self.ltHurt = [pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT01.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT02.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT03.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT04.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT05.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'LT06.png')), ]

        self.rtHurt = [pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT01.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT02.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT03.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT04.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT05.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Hurt', 'RT06.png')), ]

        # Jump animation sequence
        self.ltJump = [pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT01.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT02.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT03.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT04.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT05.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'LT06.png')), ]

        self.rtJump = [pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT01.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT02.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT03.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT04.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT05.png')),
                       pygame.image.load(os.path.join(self.characterImageDir, 'Jump', 'RT06.png')), ]

        # Run sequence
        self.ltRun = [pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT01.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT02.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT03.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT04.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT05.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'LT06.png')), ]

        self.rtRun = [pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT01.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT02.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT03.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT04.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT05.png')),
                      pygame.image.load(os.path.join(self.characterImageDir, 'Run', 'RT06.png')), ]

        # Stand Image
        self.ltStand = [pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT01.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT02.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT03.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT04.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT05.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'LT06.png')), ]

        self.rtStand = [pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT01.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT02.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT03.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT04.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT05.png')),
                        pygame.image.load(os.path.join(self.characterImageDir, 'Stand', 'RT06.png')), ]
