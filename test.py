import pygame

import constants
import config


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.handle_event()
            self.screen.fill(constants.BLACK)

    
if __name__ == "__main__":
    game = Game()
    game.run()