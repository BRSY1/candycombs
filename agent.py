import pygame
import random
import player
import config

class Agent(player.Player):
    def __init__(self, image1, image2):
        super().__init__(image1, image2)
        
    def update(self):
        self.speedx += random.choice([-1, 0, 1])
        self.speedy += random.choice([-1, 0, 1])

        self.rect.x += self.speedx
        self.rect.y += self.speedy