import pygame
import tile_map
import constants
import config
import player
import random
import time
import agent

end_time = time.time() + 200

class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player = player.Player("assets/mainCharacterFrames/mainCharacterStanding1.png", "assets/mainCharacterFrames/mainCharacterWalking.png")
        self.agent1 = agent.Agent("assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png")
        self.agent2 = agent.Agent("assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png")

        self.agent_group = []
        self.agent_group.append(self.agent1) # can make this a for loop
        self.agent_group.append(self.agent2)
        
        self.offsetx = 0
        self.offsety = 0
        self.candyGenerationCounter = 0
        self.lastCandyGenerationTime = 0
        self.candies = []

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.player.stop()

    def is_walkable(self, tilex, tiley):
        # Check bounds
        if tiley < 0 or tiley >= len(tile_map.tile_map) or tilex < 0 or tilex >= len(tile_map.tile_map[0]):
            return False  # Out of bounds (collision)



        return (tile_map.tile_map[tiley][tilex] != '.'     )  # Check if the tile is walkable

    def move(self):

        # Store the previous position
        prevx = self.player.rect.x
        prevy = self.player.rect.y
    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.moveLeft()
        if keys[pygame.K_RIGHT]:
            self.player.moveRight()
        if keys[pygame.K_UP]:
            self.player.moveUp()
        if keys[pygame.K_DOWN]:
            self.player.moveDown()
        if keys[pygame.K_SPACE]:
            for agent in self.agent_group:
                if self.player.tilex == agent.tilex and self.player.tiley == agent.tiley:
                    candy_stolen = agent.candy // 5
                    agent.candy -= candy_stolen
                    self.player.candy += candy_stolen

        
        self.player.tilex = (self.player.rect.x + config.TILE_SIZE // 4) // config.TILE_SIZE
        self.player.tiley = (self.player.rect.y + config.TILE_SIZE // 2) // config.TILE_SIZE

        # Check for collision with walls
        if not self.is_walkable(self.player.tilex, self.player.tiley):
            # Revert to previous position if not walkable
            self.player.rect.x = prevx
            self.player.rect.y = prevy
        else:
            # If the position is walkable, update the previous position
            prevx = self.player.rect.x
            prevy = self.player.rect.y

        currPos = (self.player.tiley, self.player.tilex)
        if currPos in self.candies:
            self.player.candy += 1
            self.candies.remove(currPos)

        # Draw the player centered on the screen
        player_draw_x = config.SCREEN_WIDTH // 2 - self.player.rect.width // 2
        player_draw_y = config.SCREEN_HEIGHT // 2 - self.player.rect.height // 2
        self.screen.blit(self.player.image, (player_draw_x, player_draw_y))
          # Draw rectangle outline with a width of 2 pixels


    def createVignetteEffect(self):
        visionSurface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        visionSurface.fill((0,0,0,240))
        center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2) 
        for radius in range(config.VISION_RADIUS, 0, -30):
            alpha = int(240 * (radius / config.VISION_RADIUS)) 
            pygame.draw.circle(visionSurface, (0,0,0,0 + alpha), center, radius)
        self.screen.blit(visionSurface, (0, 0))

    def valuables_UI(self):
        box_position = ((config.SCREEN_WIDTH/2)-300, 40)
        box_width = (config.SCREEN_WIDTH/2) - 200 
        box_height = 50
        #powerUps_file_location = ("","","","","")
        countdown_time = 200
        current_time = time.time()
        remaining_time = end_time - current_time

        time_amount = 3
        candy_collected = self.player.candy
        powerUp_index = 0

        candy_ui = pygame.image.load("assets/ui/candy.png")
        scaled_candy_ui = pygame.transform.scale(candy_ui, (candy_ui.get_width() * 12, candy_ui.get_height() * 12)) 
        self.screen.blit(scaled_candy_ui, (0,0))

        candy_image = pygame.image.load("assets/tiles/candy_orange.png")
        scaled_candy_image = pygame.transform.scale(candy_image, (candy_image.get_width() * 4, candy_image.get_height() * 4))
        self.screen.blit(scaled_candy_image, (2,2))
        
        font_candy = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 90)
        text = font_candy.render(f"{candy_collected}", True, (255,165,0))
        self.screen.blit(text, (140, 0))

        if (remaining_time >=0):
            bar_width = ((remaining_time/countdown_time) * box_width) -4
            pygame.draw.rect(self.screen, (0,0,0), (*box_position, box_width, box_height), 2)
            pygame.draw.rect(self.screen, (139,0,139), (box_position[0] + 2, box_position[1] + 2, bar_width, box_height-4))
            pygame.draw.rect(self.screen, (128,128,128), (box_position[0] + 2 + bar_width, box_position[1] + 2, ((bar_width-4) - bar_width), box_height-4))
            remaining_time = int(remaining_time)
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            font_countdown = pygame.font.Font(None, 40)
            text = font_countdown.render(f"{minutes:02}:{seconds:02}", True, (255,255,255))
            self.screen.blit(text, ((config.SCREEN_WIDTH/2)-30, 50))

        powerup_ui = pygame.image.load("assets/ui/powerup.png")
        scaled_powerup_ui = pygame.transform.scale(powerup_ui, (powerup_ui.get_width() * 12, powerup_ui.get_height() * 12))
        self.screen.blit(scaled_powerup_ui, (config.SCREEN_WIDTH-(32 * 12), 0))

        #powerUps_image = pygame.image.load(powerUps_file_location[powerUp_index])
        #scaled_power_image = pygame.transform.scale(powerUps_image, (powerUps_image.get_width() * 4, powerUps_image.get_height() * 4))
        #self.screen.blit(scaled_power_image, (config.SCREEN_WIDTH-20,20))

    def moveAgents(self):
        self.offsetx = self.player.rect.x - config.SCREEN_WIDTH // 2 + config.TILE_SIZE // 2
        self.offsety = self.player.rect.y - config.SCREEN_HEIGHT // 2 + config.TILE_SIZE // 2

        for agent in self.agent_group:
            prevx = agent.rect.x
            prevy = agent.rect.y
            agent.update()

            agent.tilex = (agent.rect.x + config.TILE_SIZE // 4) // config.TILE_SIZE
            agent.tiley = (agent.rect.y + config.TILE_SIZE // 2) // config.TILE_SIZE

            if tile_map.tile_map[agent.tiley][agent.tilex] == '.':
                agent.speedx = 0
                agent.speedy = 0
                agent.rect.x = prevx
                agent.rect.y = prevy
            
            if agent.tilex == self.player.tilex and agent.tiley == self.player.tiley and random.randint(1, 10) == 1:
                candy_stolen = self.player.candy // 5
                self.player.candy -= candy_stolen
                agent.candy += candy_stolen
            
            self.screen.blit(agent.image, (agent.rect.x - self.offsetx, agent.rect.y - self.offsety))

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.drawTileMap()
            self.move()
            self.player.updateAnimation()
            self.moveAgents()
            self.handleEvent()
            self.createVignetteEffect()
            self.valuables_UI()
            pygame.display.flip()

    def drawTileMap(self):
        offset_x = self.player.rect.x - config.SCREEN_WIDTH // 2 + config.TILE_SIZE // 2
        offset_y = self.player.rect.y - config.SCREEN_HEIGHT // 2 + config.TILE_SIZE // 2
        
        self.screen.fill((100, 100, 100))
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                tile_image = tile_map.tiles[tile_type]
                x = col_index * config.TILE_SIZE - self.offsetx
                y = row_index * config.TILE_SIZE - self.offsety
                self.screen.blit(tile_image, (x, y))

        # regenerate candies
        currentTime = pygame.time.get_ticks()
        if (self.lastCandyGenerationTime == 0 or
            (currentTime - self.lastCandyGenerationTime >= config.CANDY_GENERATION_RATE)
        ):
            self.candies.clear()
            self.generateCandies()
            self.lastCandyGenerationTime = currentTime

        # render candies
        if currentTime - self.lastCandyGenerationTime <= config.CANDY_DISPLAY_INTERVAL:
            candy_image = tile_map.candy  
            for pos in self.candies:
                candy_x = pos[1] * config.TILE_SIZE - offset_x
                candy_y = pos[0] * config.TILE_SIZE - offset_y
                self.screen.blit(candy_image, (candy_x, candy_y))

    def generateCandies(self):
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                if tile_type not in ['.', 't'] and random.random() < 0.01:
                    self.candies.append((row_index, col_index))


#def draw_bar(screen, coins_collected, max_coins):
#    pygame.draw.rect(screen, BLACK, (*BAR_POS, BAR_WIDTH, BAR_HEIGHT), 2)  # Border
#    fill_width = (coins_collected / max_coins) * (BAR_WIDTH - 4)  # -4 for padding
#    pygame.draw.rect(screen, GREEN, (BAR_POS[0] + 2, BAR_POS[1] + 2, fill_width, BAR_HEIGHT - 4))  # Filled portion
#    text = font.render(f"Coins: {coins_collected}/{max_coins}", True, BLACK)
#    screen.blit(text, (BAR_POS[0] + 5, BAR_POS[1] - 25))  # Above the bar


if __name__ == "__main__":
    game = Game()
    game.run()