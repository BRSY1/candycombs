import pygame
from pygame import sprite
import config
import tile_map

class Player(sprite.Sprite):
    def __init__(self, image1, image2):
        super().__init__()
        self.image = pygame.image.load(image1)
        self.image = pygame.transform.scale(self.image, (128, 128))

        self.walking_image = pygame.image.load(image2)
        self.walking_image = pygame.transform.scale(self.walking_image, (128, 128))

        self.standing_image = self.image
        
        self.rect = self.image.get_rect() 
        self.rect.topleft = (tile_map.CENTERX * config.TILE_SIZE, tile_map.CENTERY * config.TILE_SIZE)

        self.speedx = 0
        self.speedy = 0

        self.facing_right = True
        self.is_moving = False
        self.speed = 2
        self.animate_speed = 0.1
        self.animate_frame = 0
        self.candy = 10

    def check_collision(self, prev_rect):
        # Get the tile position based on the player's current rectangle position
        new_tilex = self.rect.centerx // config.TILE_SIZE
        new_tiley = self.rect.centery // config.TILE_SIZE




    def updateAnimation(self):
        if self.is_moving:
            self.animate_frame += self.animate_speed
            self.image = self.standing_image if int(self.animate_frame) % 2 else self.walking_image
        else:
            self.image = self.standing_image
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