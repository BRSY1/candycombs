import pygame

import config
import roomgen


DARK = pygame.image.load("assets/tiles/dark_wall.png")
LIGHT = pygame.image.load("assets/tiles/light_wall.png")


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        self.image = tile_type
        self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))


tileMap = roomgen.generate_map(100,16,8,8).grid
tilesGroup = pygame.sprite.Group()

for row_index, row in enumerate(tileMap):
    for col_index, tile_type in enumerate(row):
        tile_image = TILE_IMAGES.get(tile_type)
        if tile_image:
            x = col_index * config.TILE_SIZE
            y = row_index * config.TILE_SIZE
            tile = Tile(x, y, tile_image)
            tiles_group.add(tile)
