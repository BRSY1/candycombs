import pygame
import config
import roomgen
import constants

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

candy_knife = pygame.image.load("assets/tiles/candy_knife_floor.png")
candy_knife = pygame.transform.scale(candy_knife, (config.TILE_SIZE, config.TILE_SIZE))


speed = pygame.image.load("assets/items/speed.png")
speed = pygame.transform.scale(speed, (config.TILE_SIZE, config.TILE_SIZE))

lava = pygame.image.load("assets/tiles/lava.png")
lava = pygame.transform.scale(lava, (config.TILE_SIZE, config.TILE_SIZE))

easy = pygame.image.load("assets/tiles/easy.png")
easy = pygame.transform.scale(easy, (config.TILE_SIZE, config.TILE_SIZE))

med = pygame.image.load("assets/tiles/med.png")
med = pygame.transform.scale(med, (config.TILE_SIZE, config.TILE_SIZE))

hard = pygame.image.load("assets/tiles/hard.png")
hard = pygame.transform.scale(hard, (config.TILE_SIZE, config.TILE_SIZE))

candy_knife_ui = pygame.image.load("assets/items/candy_knife.png")
candy_knife_ui = pygame.transform.scale(candy_knife_ui, (config.TILE_SIZE, config.TILE_SIZE))

speed_ui = pygame.image.load("assets/items/speed.png")
candy_knife_ui = pygame.transform.scale(speed_ui, (config.TILE_SIZE, config.TILE_SIZE))

powerUps = {
    constants.KNIFE: candy_knife_ui,
    constants.SPEED: speed_ui
}

tiles = {
    'a': floor_cracked,
    'b': floor_split_cracked,
    'c': floor_split,
    'd': floor,
    'e': easy, #easy
    'm': med, #med
    'h': hard, #hard
    'p': light_wall,
    'l': lava, #lava
    '.': dark_wall,
    't': chest_floor,
    'k': candy_knife,
    's' : speed,

    '1': light_wall, #top left
    '2': light_wall, #top right
    '3': light_wall, #bottom left
    '4': light_wall #bottom right
}