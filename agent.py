import pygame
import random
import player
import config

class Agent(player.Player):
    def __init__(self, image1, image2):
        super().__init__(image1, image2)
        
    def update(self):
        self.is_moving = True
        if self.speedx > 0: prev_dir = True
        else: prev_dir = False # true is right
        self.speedx += random.choice([-1, 0, 1])
        self.speedy += random.choice([-1, 0, 1])

        if self.speedx < 0 and prev_dir == True or self.speedx > 0 and prev_dir == False:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.speedx
        self.rect.y += self.speedy