import pygame
import config
import roomgen

myMap = roomgen.generate_map(100,16,8,8)

tile_map = myMap.grid

floor_cracked = pygame.image.load("assets/tiles/floor_cracked.png")
floor_cracked = pygame.transform.scale(floor_cracked, (config.TILE_SIZE, config.TILE_SIZE))
floor_split_cracked = pygame.image.load("assets/tiles/floor_split_cracked.png")
floor_split_cracked = pygame.transform.scale(floor_split_cracked, (config.TILE_SIZE, config.TILE_SIZE))
floor_split = pygame.image.load("assets/tiles/floor_split.png")
floor_split = pygame.transform.scale(floor_split, (config.TILE_SIZE, config.TILE_SIZE))
floor = pygame.image.load("assets/tiles/floor_split.png")
floor = pygame.transform.scale(floor, (config.TILE_SIZE, config.TILE_SIZE))

dark_wall = pygame.image.load("assets/tiles/dark_wall.png")
dark_wall = pygame.transform.scale(dark_wall, (config.TILE_SIZE, config.TILE_SIZE))
light_wall = pygame.image.load("assets/tiles/wall_light.png")
light_wall = pygame.transform.scale(light_wall, (config.TILE_SIZE, config.TILE_SIZE))

tiles = {
    'a': floor_cracked,
    'b': floor_split_cracked,
    'c': floor_split,
    'd': floor,
    '.': dark_wall
}