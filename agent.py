import pygame
import random
import player
import config
import tile_map

class Agent(player.Player):
    def __init__(self, image1, image2):
        super().__init__(image1, image2)
        self.grid = [[0 for i in range(11)] for j in range(11)]

    def updateGrid(self):
        self.grid = tile_map.tile_map[self.y-5:self.y+5, self.x-5:self.x+5]
        print(self.grid)
        
    def update(self):
        self.speedx += random.choice([-1, 0, 1])
        self.speedy += random.choice([-1, 0, 1])

        self.rect.x += self.speedx
        self.rect.y += self.speedy