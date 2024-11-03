import pygame
from pygame import sprite
import config
import tile_map

class Player(sprite.Sprite):
    def __init__(self, images, locationx, locationy):
        super().__init__()
        # images
        # r: powerUp indices (e.g. default: 0, knife: 1, night_vision: 2, invisibility 3)
        # c: standing: 0, walking: 1, stabbing: 2
        
        self.images = [list(map(pygame.image.load, row)) for row in images]
        self.images = [list(map(lambda img: pygame.transform.scale(img, (128, 128)), row)) for row in self.images]
        self.image = self.images[0][0]
        
        self.rect = self.image.get_rect() 
        self.rect.topleft = (tile_map.CENTERX * config.TILE_SIZE, tile_map.CENTERY * config.TILE_SIZE)

        self.speedx = 0
        self.speedy = 0
        
        if not locationx:
            self.tilex = (self.rect.x + config.TILE_SIZE // 4) // config.TILE_SIZE
            self.tiley = (self.rect.y + config.TILE_SIZE // 4) // config.TILE_SIZE
            
        self.tilex = locationx
        self.tiley = locationy

        self.facing_right = True
        self.is_moving = False
        self.animate_speed = 0.1
        self.animate_frame = 0
        self.candy = 10
        self.speed = 10
        self.powerUpIndex = -1
        self.is_attacking = False
        self.lastAttackTime = -1
        self.night_vis = False
        self.is_invisible = False
    
    def updateAnimation(self):
        # use an if statement to handle the case where the default animation is used for a special powerup
        
        animationIndex = 0
        if self.powerUpIndex == 0:
            animationIndex = 1
        elif self.night_vis:
            animationIndex = 2
        elif self.is_invisible:
            animationIndex = 3


        if self.is_attacking:
            self.animate_frame += self.animate_speed
            self.image = self.images[animationIndex][0] if int(self.animate_frame) % 2 else self.images[animationIndex][2]

            if pygame.time.get_ticks() - self.lastAttackTime > config.ATTACK_INTERVAL:
                self.is_attacking = False

        elif self.is_moving:
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