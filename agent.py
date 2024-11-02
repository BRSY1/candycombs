import pygame
import random
import player
import config

class Agent(player.Player):
    def __init__(self, image1, image2):
        super().__init__(image1, image2)
        
    def update(self):
        self.rect.x += random.choice([-1 * config.SPEED, 0, 1 * config.SPEED])
        self.rect.y += random.choice([-1 * config.SPEED, 0, 1 * config.SPEED])