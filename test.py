import pygame
import tile_map
import constants
import config


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.handleEvent()
            self.drawTileMap()
            
    def drawTileMap(self):
        self.screen.fill((100, 100, 100))
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE
                y = row_index * config.TILE_SIZE
                self.screen.blit(tile_image, (x, y))
        pygame.display.flip()

    
if __name__ == "__main__":
    game = Game()
    game.run()