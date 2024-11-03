import pygame
import random
import player
import config
import tile_map
import torch
import torch.nn.functional as F
import numpy as np
import model
import deque

class Agent(player.Player):
    def __init__(self, images):
        super().__init__(images)
        self.grid = []
        self.training = True
        self.model = model.model()
        self.reward = 0
        if self.training == True:
            self.gamma = 0.99
            self.lr = 1e-3
            self.optimiser = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def getGrid(self, player, agents):
        # dim: (2, 11, 11)
        self.grid = np.zeros((2, 11, 11))
        tmpTile = []
        
        for row in tile_map.tile_map[self.tiley-6:self.tiley+5]:
            tmpTile.append(row[self.tilex-6:self.tilex+5])

        for i in range(11):
            for j in range(11):
                tile = tmpTile[i][j]

                if tile == '.': # wall 
                    self.grid[0][i][j] = 1
                elif tile == 'c': # candy
                    self.grid[1][i][j] = 1  
                    
        for agent in agents:
            if (
                self.tiley-6 <= agent.tiley < self.tiley+5 and 
                self.tilex-6 <= agent.tilex < self.tilex+5
            ):
                if agent == self:
                    # self grid marked as 3 
                    self.grid[1][6][6] = 3
                else:
                    # agent grid marked as 2 
                    self.grid[1][agent.tiley - self.tiley + 6][agent.tilex - self.tilex + 6] = 2

        if player:
            if (
                self.tiley-6 <= player.tiley < self.tiley+5 and 
                self.tilex-6 <= player.tilex < self.tilex+5
            ):  
                # human player grid marked as 2
                self.grid[1, player.tiley - self.tiley + 6, player.tilex - self.tiley + 6] = 2

        return self.grid
    
    def getMatrix(self, player, agents):
        self.grid = np.zeros((11, 11))

        tmpTile = []
        for row in tile_map.tile_map[self.tiley-6:self.tiley+5]:
            tmpTile.append(row[self.tilex-6:self.tilex+5])

        for i in range(11):
            for j in range(11):
                tile = tmpTile[i][j]
                if tile == '.':  # wall
                    self.grid[i][j] = 1
                elif tile == 'c':  # candy
                    self.grid[i][j] = 2

        for agent in agents:
            if (self.tiley-6 <= agent.tiley < self.tiley+5 and
                self.tilex-6 <= agent.tilex < self.tilex+5):
                if agent == self:
                    # Self grid marked as 3 (for the agent itself)
                    self.grid[6][6] = 3
                else:
                    # Agent grid marked as 4 (for other agents)
                    agent_x = agent.tilex - self.tilex + 6
                    agent_y = agent.tiley - self.tiley + 6
                    self.grid[agent_y][agent_x] = 4

        if player:
            if (self.tiley-6 <= player.tiley < self.tiley+5 and
                self.tilex-6 <= player.tilex < self.tilex+5):
                player_x = player.tilex - self.tilex + 6
                player_y = player.tiley - self.tiley + 6
                # Human player grid marked as 4
                self.grid[player_y][player_x] = 4

        return self.grid
    
    def update(self, agent_group, player=None):
        self.getGrid(None, agent_group)
        self.is_moving = True
        if self.speedx > 0: self.facing_right = True
        else: self.facing_right = False
        self.updateAnimation()

        x = torch.tensor(self.grid, dtype=torch.float32)
        action_values = self.model.forward(x)

        # up is 0, right is 1, down is two, left is 3
        if random.choice(range(1, 2)) != 1:
            direction = torch.argmax(action_values)
        else:
            direction = random.choice(range(1, 4))

        value = action_values[direction]

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
            self.getGrid(None, agent_group)
            x = torch.tensor(self.grid, dtype=torch.float32)
            next_action_values = self.model(x)
            next_value = torch.max(next_action_values)

            loss = ((self.reward + self.gamma * next_value) - value) ** 2
            loss.backward()
            self.optimiser.step()
            self.optimiser.zero_grad()

            self.reward = 0
