import pygame
import config
import roomgen

myMap = roomgen.generate_map(100,16,8,8)

CENTERX = myMap.center_x
CENTERY = myMap.center_y

tile_map = myMap.grid

floor_cracked = pygame.image.load("assets/tiles/floor_cracked.png")
floor_cracked = pygame.transform.scale(floor_cracked, (config.TILE_SIZE, config.TILE_SIZE))
floor_split_cracked = pygame.image.load("assets/tiles/floor_split_cracked.png")
floor_split_cracked = pygame.transform.scale(floor_split_cracked, (config.TILE_SIZE, config.TILE_SIZE))
floor_split = pygame.image.load("assets/tiles/floor_split.png")
floor_split = pygame.transform.scale(floor_split, (config.TILE_SIZE, config.TILE_SIZE))
floor = pygame.image.load("assets/tiles/floor.png")
floor = pygame.transform.scale(floor, (config.TILE_SIZE, config.TILE_SIZE))

dark_wall = pygame.image.load("assets/tiles/dark_wall.png")
dark_wall = pygame.transform.scale(dark_wall, (config.TILE_SIZE, config.TILE_SIZE))
light_wall = pygame.image.load("assets/tiles/light_wall.png")
light_wall = pygame.transform.scale(light_wall, (config.TILE_SIZE, config.TILE_SIZE))

chest_floor = pygame.image.load("assets/tiles/chest_floor.png")
chest_floor = pygame.transform.scale(chest_floor, (config.TILE_SIZE, config.TILE_SIZE))

candy = pygame.image.load("assets/tiles/candy_orange.png")
candy = pygame.transform.scale(candy, (config.TILE_SIZE, config.TILE_SIZE))

candy_knife = pygame.image.load("assets/items/updatedCandyKnifePlain.png")
candy_knife = pygame.transform.scale(candy_knife, (config.TILE_SIZE, config.TILE_SIZE))

tiles = {
    'a': floor_cracked,
    'b': floor_split_cracked,
    'c': floor_split,
    'd': floor,
    'p': light_wall,
    '.': dark_wall,
    't': chest_floor,
    'k': candy_knife
}