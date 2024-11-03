import pygame
import random
import player
import config
import tile_map
import torch
import torch.nn.functional as F
import model

class Agent(player.Player):
    def __init__(self, images):
        super().__init__(images)
        self.grid = []
        self.training = False
        self.model = model.model()
        self.reward = 0
        if self.training == True:
            self.epsilon = 0.95
            self.lr = 1e-3
            self.optimiser = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def updateGrid(self):
        self.grid = []
        self.tmp = tile_map.tile_map[self.tiley-6:self.tiley+5]
        for i in range(11):
            self.grid.append(self.tmp[i][self.tilex-6:self.tilex+5])

        for i in range(11):
            for j in range(11):
                if self.grid[i][j] == '.':
                    self.grid[i][j] = 0
                elif self.grid[i][j] == 'c':
                    self.grid[i][j] = 1
                else: 
                    self.grid[i][j] = 2
        

    def update(self):
        self.updateGrid()
        self.is_moving = True
        if self.speedx > 0: self.facing_right = True
        else: self.facing_right = False
        self.updateAnimation()

        x = torch.tensor(self.grid, dtype=torch.float32)
        action_values = self.model.forward(x)

        # up is 0, right is 1, down is two, left is 3
        direction = torch.argmax(action_values)
        value = torch.max(action_values)

        if direction == 0:
            self.speedy += 1
        elif direction == 1:
            self.speedx += 1
        elif direction == 2:
            self.speedy -= 1
        else:
            self.speedx -= 1

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.training == True:
            self.updateGrid()
            x = torch.tensor(self.grid, dtype=torch.float32)
            next_action_values = self.model(x)
            next_value = torch.max(next_action_values)

            loss = ((self.reward + self.epsilon * next_value) - value) ** 2
            loss.backward()
            self.optimiser.step()
            self.optimiser.zero_grad()

            self.reward = 0
