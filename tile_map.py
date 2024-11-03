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

invisibility = pygame.image.load("assets/items/invis.png")
invisibility = pygame.transform.scale(invisibility, (config.TILE_SIZE, config.TILE_SIZE))

night_vision = pygame.image.load("assets/items/night_vision.png")
night_vision = pygame.transform.scale(night_vision, (config.TILE_SIZE, config.TILE_SIZE))

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

diamond = pygame.image.load("assets/tiles/diamond.png")
diamond = pygame.transform.scale(diamond, (config.TILE_SIZE, config.TILE_SIZE))

spade = pygame.image.load("assets/tiles/spade.png")
spade = pygame.transform.scale(spade, (config.TILE_SIZE, config.TILE_SIZE))

club = pygame.image.load("assets/tiles/club.png")
club = pygame.transform.scale(club, (config.TILE_SIZE, config.TILE_SIZE))

heart = pygame.image.load("assets/tiles/heart.png")
heart = pygame.transform.scale(heart, (config.TILE_SIZE, config.TILE_SIZE))

candy_knife_ui = pygame.image.load("assets/items/candy_knife.png")
candy_knife_ui = pygame.transform.scale(candy_knife_ui, (config.TILE_SIZE, config.TILE_SIZE))

speed_ui = pygame.image.load("assets/items/speed.png")
speed_ui = pygame.transform.scale(speed_ui, (config.TILE_SIZE, config.TILE_SIZE))

#Decorations
bone = pygame.image.load("assets/decorations/bone.png")
bone = pygame.transform.scale(bone , (config.TILE_SIZE, config.TILE_SIZE))

bookshelf= pygame.image.load("assets/decorations/bookshelf.png")
bookshelf= pygame.transform.scale(bookshelf, (config.TILE_SIZE, config.TILE_SIZE))

orb = pygame.image.load("assets/decorations/orb.png")
orb = pygame.transform.scale(orb, (config.TILE_SIZE, config.TILE_SIZE))

skull = pygame.image.load("assets/decorations/skull.png")
skull = pygame.transform.scale(skull, (config.TILE_SIZE, config.TILE_SIZE))


spiderWeb= pygame.image.load("assets/decorations/skullAndBone.png")
spiderWeb= pygame.transform.scale(spiderWeb, (config.TILE_SIZE, config.TILE_SIZE))

witchesHat = pygame.image.load("assets/decorations/updatedWitchesHat.png")
witchesHat= pygame.transform.scale(witchesHat, (config.TILE_SIZE, config.TILE_SIZE))

cauldron = pygame.image.load("assets/decorations/updatedCauldron.png")
cauldron= pygame.transform.scale(cauldron, (config.TILE_SIZE, config.TILE_SIZE))



powerUps = {
    constants.KNIFE: candy_knife_ui,
    constants.SPEED: speed_ui,
    constants.INVISIBILITY: invisibility,
    constants.NIGHT_VISION: night_vision
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
    's': speed,
    'i': invisibility,
    'n': night_vision ,
    '1': diamond, #top left
    '2': spade, #top right
    '3': club, #bottom left
    '4': heart, #bottom right


    'u': bone,
    'v': bookshelf,
    'w': orb,
    'x': skull,
    'y': spiderWeb,
    'z': witchesHat,
    'Z': cauldron
    
}