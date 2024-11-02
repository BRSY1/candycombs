import pygame
from pygame import sprite
import config

class Player(sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("assets/mainCharacterFrames/mainCharacterStanding1.png")
        self.image = pygame.transform.scale(self.image, (128, 128))

        self.walking_image = pygame.image.load("assets/mainCharacterFrames/mainCharacterWalking.png")
        self.walking_image = pygame.transform.scale(self.walking_image, (128, 128))

        self.standing_image = self.image
        
        self.locationx, self.locationy = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        self.speedx = 0
        self.speedy = 0

        self.facing_right = True
        self.is_moving = False
        self.speed = 2
        self.animate_speed = 0.1
        self.animate_frame = 0
    
    def updateAnimation(self):
        if self.is_moving:
            self.animate_frame += self.animate_speed
            self.image = self.standing_image if int(self.animate_frame) % 2 else self.walking_image
        else:
            self.image = self.standing_image
            self.animate_frame = 0
        
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def moveLeft(self):
        self.locationx += -5 * config.SPEED
        self.is_moving = True
        if self.facing_right:
            self.facing_right = False
        
    def moveRight(self):
        self.locationx += 5 * config.SPEED
        self.is_moving = True
        if not self.facing_right:
            self.facing_right = True
        
    def moveUp(self):
        self.locationy += -5 * config.SPEED
        self.is_moving = True

    def moveDown(self):
        self.locationy += 5 * config.SPEED
        self.is_moving = True

    def stop(self):
        self.is_moving = False