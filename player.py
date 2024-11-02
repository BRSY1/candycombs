import pygame
from pygame import sprite
import config

class Player(sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("assets/mainCharacterFrames/mainCharacterStanding1.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        
        self.locationx, self.locationy = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        self.speedx = 0
        self.speedy = 0

        self.candy = 3
        self.currentPowerup = 0

        self.facing_right = True


    def moveLeft(self):
        self.locationx += -5 * config.SPEED
        if self.facing_right == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True
    
    def moveRight(self):
        self.locationx += 5 * config.SPEED
        if self.facing_right == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False

    def moveUp(self):
        self.locationy += -5 * config.SPEED

    def moveDown(self):
        self.locationy += 5 * config.SPEED