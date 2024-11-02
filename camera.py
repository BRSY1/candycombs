import pygame 

import config


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target):
        x = target.rect.centerx - self.width // 2
        y = target.rect.centery - self.height // 2

        x = max(0, min(x, self.width - self.camera.width))
        y = max(0, min(y, self.height - self.camera.height))

        self.camera = pygame.Rect(x, y, self.width, self.height)