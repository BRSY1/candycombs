import pygame
from pygame import sprite

class Player(sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("assets/mainCharacterFrames/mainCharacterStanding1.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        
        self.rect = self.image.get_rect()
        self.locationx, self.locationy = 100, 100

        self.speedx = 0
        self.speedy = 0

        self.facing_right = True
    
    def update(self):
        self.locationx += self.speedx
        self.locationy += self.speedy

    def moveLeft(self):
        self.speedx = -5
        if self.facing_right == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = True
    
    def moveRight(self):
        self.speedx = 5
        if self.facing_right == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False

    def moveUp(self):
        self.speedy = -5

    def moveDown(self):
        self.speedy = 5

    def stopHorizontal(self):
        self.speedx = 0

    def stopVertical(self):
        self.speedy = 0