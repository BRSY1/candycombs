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
        # print(self.tilex, self.tiley)
        self.grid = []
        self.tmp = tile_map.tile_map[self.tiley-6:self.tiley+5]
        for i in range(11):
            self.grid.append(self.tmp[i][self.tilex-5:self.tilex+5])
        # print(self.grid, '\n')

    def update(self):
        self.updateGrid()
        self.is_moving = True
        if self.speedx > 0: self.facing_right = True
        else: self.facing_right = False
        self.updateAnimation()

        self.speedx += random.choice([-1, 0, 1])
        self.speedy += random.choice([-1, 0, 1])

        self.rect.x += self.speedx
        self.rect.y += self.speedy