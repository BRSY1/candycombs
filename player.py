import pygame
from pygame import sprite
import config
import tile_map

class Player(sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        # images
        # r: powerUp indices (e.g. default: 0, knife: 1)
        # c: standing: 0, walking: 1, ...
        self.images = [list(map(pygame.image.load, row)) for row in images]
        self.images = [list(map(lambda img: pygame.transform.scale(img, (128, 128)), row)) for row in self.images]
        self.image = self.images[0][0]
        
        self.rect = self.image.get_rect() 
        self.rect.topleft = (tile_map.CENTERX * config.TILE_SIZE, tile_map.CENTERY * config.TILE_SIZE)

        self.speedx = 0
        self.speedy = 0

        self.tilex = (self.rect.x + config.TILE_SIZE // 4) // config.TILE_SIZE
        self.tiley = (self.rect.y + config.TILE_SIZE // 2) // config.TILE_SIZE

        self.facing_right = True
        self.is_moving = False
        self.animate_speed = 0.1
        self.animate_frame = 0
        self.candy = 10
        self.speed = 10
        self.powerUpIndex = -1
    
    def updateAnimation(self):
        # use an if statement to handle the case where the default animation is used for a special powerup
        animationIndex = self.powerUpIndex + 1 if self.powerUpIndex + 1 < len(self.images) else 0

        if self.is_moving:
            self.animate_frame += self.animate_speed
            self.image = self.images[animationIndex][0] if int(self.animate_frame) % 2 else self.images[animationIndex][1]

        else:
            self.image = self.images[animationIndex][0]
            self.animate_frame = 0
        
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def moveLeft(self):
        self.rect.x += -5 * config.SPEED
        self.is_moving = True
        if self.facing_right:
            self.facing_right = False
        
    def moveRight(self):
        self.rect.x += 5 * config.SPEED
        self.is_moving = True
        if not self.facing_right:
            self.facing_right = True
        
    def moveUp(self):
        self.rect.y += -5 * config.SPEED
        self.is_moving = True

    def moveDown(self):
        self.rect.y += 5 * config.SPEED
        self.is_moving = True

    def stop(self):
        self.is_moving = False