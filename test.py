import pygame
import tile_map
import constants
import config
import player
import random
import time

end_time = time.time() + 10

class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player = player.Player()

    def handleEvent(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def move(self):
        # prevx = self.player.locationx
        # prevy = self.player.locationy

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.moveLeft()
        if keys[pygame.K_RIGHT]:
            self.player.moveRight()
        if keys[pygame.K_UP]:
            self.player.moveUp()
        if keys[pygame.K_DOWN]:
            self.player.moveDown()
             
        # new_tilex = self.player.locationx // config.TILE_SIZE
        # new_tiley = self.player.locationy // config.TILE_SIZE

        # self.player.update()
        # if tile_map.tile_map[new_tiley][new_tilex] == '.':
        #     self.player.locationx = prevx
        #     self.player.locationy = prevy

        self.screen.blit(self.player.image, (config.SCREEN_HEIGHT // 2 + 100, config.SCREEN_HEIGHT // 2 - 100))

    def valuables_UI(self):
        box_position = (500, 40)
        box_width = 600
        box_height = 50
        #powerUps_file_location = ("","","","","")
        countdown_time = 10
        current_time = time.time()
        remaining_time = end_time - current_time

        time_amount = 3
        candy_collected = 10
        powerUp_index = 0

        #powerUps_image = pygame.image.load(powerUps_file_location[powerUp_index])
        #scaled_power_image = pygame.transform.scale(powerUps_image, (powerUps_image.get_width() * 4, powerUps_image.get_height() * 4))
        #self.screen.blit(scaled_power_image, (20,20))

        candy_image = pygame.image.load("assets/tiles/candy_orange.png")
        scaled_candy_image = pygame.transform.scale(candy_image, (candy_image.get_width() * 4, candy_image.get_height() * 4))
        self.screen.blit(scaled_candy_image, (20,20))
        
        font_candy = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 100)
        text = font_candy.render(f"{candy_collected}", True, (255,165,0))
        self.screen.blit(text, (160, 20))

        if (remaining_time >=0):
            bar_width = ((remaining_time/countdown_time) * box_width) -4
            pygame.draw.rect(self.screen, (0,0,0), (*box_position, box_width, box_height), 2)
            pygame.draw.rect(self.screen, (139,0,139), (box_position[0] + 2, box_position[1] + 2, bar_width, box_height-4))
            pygame.draw.rect(self.screen, (128,128,128), (box_position[0] + 2 + bar_width, box_position[1] + 2, (596 - bar_width), box_height-4))
            remaining_time = int(remaining_time)
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            font_countdown = pygame.font.Font(None, 40)
            text = font_countdown.render(f"{minutes:02}:{seconds:02}", True, (255,255,255))
            self.screen.blit(text, (770, 50))

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.drawTileMap()
            self.move()
            self.handleEvent()
            self.valuables_UI()
            pygame.display.flip()
    
    def drawTileMap(self):
        offset_x = self.player.locationx - config.SCREEN_WIDTH // 2 + config.TILE_SIZE // 2
        offset_y = self.player.locationy - config.SCREEN_HEIGHT // 2 + config.TILE_SIZE // 2
        
        self.screen.fill((100, 100, 100))
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE - offset_x
                y = row_index * config.TILE_SIZE - offset_y
                self.screen.blit(tile_image, (x, y))


if __name__ == "__main__":
    game = Game()
    game.run()