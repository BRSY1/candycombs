import pygame
from pygame import sprite

import config

class Player(sprite.Sprite):
    def __init__(self): 
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))
        
        self.rect = self.image.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))

        self.speedx = 0
        self.speedy = 0
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def moveLeft(self):
        self.speedx = -5
    
    def moveRight(self):
        self.speedx = 5

    def moveUp(self):
        self.speedy = -5

    def moveDown(self):
        self.speedy = 5

    def stopHorizontal(self):
        self.speedx = 0

    def stopVertical(self):
        self.speedy = 0