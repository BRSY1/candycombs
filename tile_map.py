import pygame
import config
import roomgen

myMap = roomgen.generate_map(100,16,8,8)

tile_map = myMap.grid

dark_wall = pygame.image.load("assets/tiles/dark_wall.png")
dark_wall = pygame.transform.scale(dark_wall, (config.TILE_SIZE, config.TILE_SIZE))
light_wall = pygame.image.load("assets/tiles/light_wall.png")
light_wall = pygame.transform.scale(light_wall, (config.TILE_SIZE, config.TILE_SIZE))

tiles = {
    'a': light_wall,
    'b': dark_wall,
    '.': dark_wall
}