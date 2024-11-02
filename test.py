import pygame
import tile_map
import constants
import config
import player


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = player.Player()

    def handleEvent(self):
        prevx = self.player.locationx
        prevy = self.player.locationy

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
        
        new_tilex = self.player.locationx // config.TILE_SIZE
        new_tiley = self.player.locationy // config.TILE_SIZE

        if tile_map.tile_map[new_tiley][new_tilex] == '.':
            self.player.locationx = prevx
            self.player.locationy = prevy

        self.player.update()
        self.screen.blit(self.player.image, (self.player.locationx, self.player.locationy))

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.drawTileMap()
            self.handleEvent()
            pygame.display.flip()
    
    def drawTileMap(self):
        self.screen.fill((100, 100, 100))
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE
                y = row_index * config.TILE_SIZE
                self.screen.blit(tile_image, (x, y))


if __name__ == "__main__":
    game = Game()
    game.run()