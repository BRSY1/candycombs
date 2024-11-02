import pygame
import tile_map
import constants
import config


# class Game:
#     def __init__(self):
#         pygame.init()
#         self.is_running = True
#         pygame.display.set_caption("CandyCombs")
#         self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
#         self.clock = pygame.time.Clock()

#     def handleEvent(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.is_running = False

#     def run(self):
#         while self.is_running:
#             self.clock.tick(config.FPS)
#             self.handleEvent()
#             self.drawTileMap()
            
#     def drawTileMap(self):
#         self.screen.fill((100, 100, 100))
#         for row_index, row in enumerate(tile_map.tile_map):
#             for col_index, tile_type in enumerate(row):
#                 tile_image = tile_map.tiles[tile_type]
#                 x = col_index * config.TILE_SIZE
#                 y = row_index * config.TILE_SIZE
#                 self.screen.blit(tile_image, (x, y))
#         pygame.display.flip()

    
# if __name__ == "__main__":
#     game = Game()
#     game.run()

import pygame
import tile_map
import config

class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Character starting position (in tile coordinates)
        self.character_x = 5  # Starting column index
        self.character_y = 5  # Starting row index

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def handleMovement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.character_x > 0:
            self.character_x -= 1
        if keys[pygame.K_RIGHT] and self.character_x < len(tile_map.tile_map[0]) - 1:
            self.character_x += 1
        if keys[pygame.K_UP] and self.character_y > 0:
            self.character_y -= 1
        if keys[pygame.K_DOWN] and self.character_y < len(tile_map.tile_map) - 1:
            self.character_y += 1

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.handleEvent()
            self.handleMovement()
            self.drawTileMap()

    def drawTileMap(self):
        # Calculate camera offset to keep the character centered
        offset_x = self.character_x * config.TILE_SIZE - config.SCREEN_WIDTH // 2 + config.TILE_SIZE // 2
        offset_y = self.character_y * config.TILE_SIZE - config.SCREEN_HEIGHT // 2 + config.TILE_SIZE // 2
        
        self.screen.fill((100, 100, 100))
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE - offset_x
                y = row_index * config.TILE_SIZE - offset_y
                self.screen.blit(tile_image, (x, y))
        
        # Draw the character (as a simple rectangle for now)
        character_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - config.TILE_SIZE // 2,
                                      config.SCREEN_HEIGHT // 2 - config.TILE_SIZE // 2,
                                      config.TILE_SIZE, config.TILE_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 0), character_rect)  # Draw the character in red

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
