import pygame
import tile_map
import constants
import config
import player
import random


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


    def drawCandybar(self):
        font = pygame.font.Font(None, 36)
        candy_collected = 10
        candy_bar_width = candy_collected * 10
        candy_bar_height = 40
        candy_bar_position = (20,20)
        pygame.draw.rect(self.screen, (255,165,0), (candy_bar_position[0] + 2, candy_bar_position[1] + 2, candy_bar_width, candy_bar_height-4))
        text = font.render(f"Candy: {candy_collected}", True, (255,255,255))
        self.screen.blit(text, (candy_bar_position[0] + 5 ,candy_bar_position[1] + 7))


    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.drawTileMap()
            self.move()
            self.handleEvent()
            self.drawCandybar()
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


#def draw_bar(screen, coins_collected, max_coins):
#    pygame.draw.rect(screen, BLACK, (*BAR_POS, BAR_WIDTH, BAR_HEIGHT), 2)  # Border
#    fill_width = (coins_collected / max_coins) * (BAR_WIDTH - 4)  # -4 for padding
#    pygame.draw.rect(screen, GREEN, (BAR_POS[0] + 2, BAR_POS[1] + 2, fill_width, BAR_HEIGHT - 4))  # Filled portion
#    text = font.render(f"Coins: {coins_collected}/{max_coins}", True, BLACK)
#    screen.blit(text, (BAR_POS[0] + 5, BAR_POS[1] - 25))  # Above the bar


if __name__ == "__main__":
    game = Game()
    game.run()