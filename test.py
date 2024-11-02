import pygame
import tile_map

import constants
import config
import roomgen
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player()


    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    self.player.moveRight()
                elif event.key == pygame.K_UP:
                    self.player.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.moveDown()
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.stopHorizontal()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.stopVertical()

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.handleEvent()

            self.player.update()
            self.drawTileMap()
            self.drawPlayer()
            pygame.display.flip() 
            
    def drawTileMap(self):
        offset_x = (config.SCREEN_WIDTH // 2) - (self.player.rect.centerx) 
        offset_y = (config.SCREEN_HEIGHT // 2) - (self.player.rect.centery)

        self.screen.fill((100, 100, 100))  # Fill the screen with a base color

        # Draw the tile map with the calculated offsets
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE + offset_x
                y = row_index * config.TILE_SIZE + offset_y
                self.screen.blit(tile_image, (x, y))

    def drawPlayer(self):
        self.screen.blit(self.player.image, self.player.rect)


if __name__ == "__main__":
    game = Game()
    game.run()