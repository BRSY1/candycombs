import pygame
import tile_map
import constants
import config
import player
import random
import time
import agent
import torch

end_time = time.time() + 200


class Game:
    MESSAGE_POP = pygame.USEREVENT + 1

    def __init__(self, isTraining=False):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("")
        pygame.mixer.music.play(-1)
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.player = player.Player([["assets/mainCharacterFrames/mainCharacterStanding1.png", "assets/mainCharacterFrames/mainCharacterWalking.png"],
                                     ["assets/mainCharacterFrames/mainCharacterKnifeStanding.png", "assets/mainCharacterFrames/mainCharacterKnifeWalking.png", "assets/mainCharacterFrames/mainCharacterKnifeStabbing.png"],
                                     ["assets/mainCharacterFrames/mainCharacterStarlightStanding.png", "assets/mainCharacterFrames/mainCharacterStartlightWalking.png"],
                                     ["assets/mainCharacterFrames/mainCharcterInvisbleStanding.png","assets/mainCharacterFrames/mainCharacterInvisibleWalking.png"]])
        self.agent1 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]])
        self.agent2 = agent.Agent([["assets/grubby10YrOld/grubby10YrOldStanding.png", "assets/grubby10YrOld/grubby10YrOldWalking.png"]])
        self.agent3 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]])

        self.agent_group = []
        self.agent_group.append(self.agent1) # can make this a for loop
        self.agent_group.append(self.agent2)
        self.agent_group.append(self.agent3)
        
        self.offsetx = 0
        self.offsety = 0
        self.candyGenerationCounter = 0
        self.lastCandyGenerationTime = 0
        self.candies = []
        self.player.powerUpIndex = -1
        self.powerUpLast = 0
        self.powerUpCooldown = 15000
        self.time_of_moves = []
        self.vignetteColourR = 0
        self.vignetteColourG = 0
        self.vignetteColourB = 0
        self.message = []

        self.isTraining = isTraining

        self.time_of_moves = 0
        self.easyTile_activ = 0
        self.mediumTileTil_activ = 0
        self.hardTile_activ = 0
        self.casinoTile_activ = 0
        self.lavaTile = [[0, 0] for _ in range(88)]

        self.casino_opt1 = 0
        self.casino_reward = 0
        self.bet_amount = 0
        self.exit = 0

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.isTraining:
                    torch.save(self.agent1.model.state_dict(), "trained_models/agent_model.pt")
                self.is_running = False

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.player.stop()

                playerXPos, playerYPos = self.player.tilex, self.player.tiley
                if event.key == pygame.K_o and tile_map.tile_map[playerYPos][playerXPos] == 't':
                    self.openChest(playerYPos, playerXPos)
                if event.key == pygame.K_o and tile_map.tile_map[playerYPos][playerXPos] == 'e':
                    self.easyTile_activ = 1
                if event.key == pygame.K_o and tile_map.tile_map[playerYPos][playerXPos] == 'm':
                    self.mediumTileTil_activ = 1
                if event.key == pygame.K_o and tile_map.tile_map[playerYPos][playerXPos] == 'h':
                    self.hardTile_activ = 1
                if event.key == pygame.K_o and (tile_map.tile_map[playerYPos][playerXPos] == '1' or tile_map.tile_map[playerYPos][playerXPos] == '2' or tile_map.tile_map[playerYPos][playerXPos] == '3' or tile_map.tile_map[playerYPos][playerXPos] == '4'):
                    self.casinoTile_activ = 1
                if self.casinoTile_activ == 1:
                    if event.key == pygame.K_1:
                        self.casino_opt1 = 1
                    if event.key == pygame.K_2:
                        self.casino_opt1 = 2
                    if event.key == pygame.K_3:
                        self.casino_opt1 = 3
                    if event.key == pygame.K_4:
                        self.casino_opt1 = 4
                    if event.key == pygame.K_x:
                        self.exit = 1
                    
            elif event.type == game.MESSAGE_POP:
                if self.message:
                    self.message.pop(0)
            


    def is_walkable(self, tilex, tiley):
        # Check bounds
        if tiley < 0 or tiley >= len(tile_map.tile_map) or tilex < 0 or tilex >= len(tile_map.tile_map[0]):
            return False  # Out of bounds (collision)

        return (tile_map.tile_map[tiley][tilex] != '.')  # Check if the tile is walkable

    def powerUp(self):
        playerXPos, playerYPos = self.player.tilex, self.player.tiley
        if  (tile_map.tile_map[playerYPos][playerXPos] == 'k' or 
            tile_map.tile_map[playerYPos][playerXPos] == 's' or 
            tile_map.tile_map[playerYPos][playerXPos] == 'i' or 
            tile_map.tile_map[playerYPos][playerXPos] == 'n'):
            self.pickUpPowerUp(playerYPos, playerXPos)

    def lavaBlock(self):
        value = 0
        lavaTile = [[0, 0] for _ in range(88)]
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                if tile_type == 'l':
                    lavaTile[value] = [row_index,col_index]
                    value+=1
       
        for i in range(0,len(lavaTile)):
            if (self.player.tiley == lavaTile[i][0]) and (self.player.tilex == lavaTile[i][1]):
                self.player.candy -= 5

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
            if self.player.powerUpIndex == constants.KNIFE:
                self.player.is_attacking = True
                self.player.lastAttackTime = pygame.time.get_ticks()

                for agent in self.agent_group:
                    if self.player.tilex == agent.tilex and self.player.tiley == agent.tiley:
                        candy_stolen = agent.candy // 5
                        agent.reward -= candy_stolen
                        agent.candy -= candy_stolen
                        self.message.append(f"You just stole {candy_stolen} candy")
                        self.player.candy += candy_stolen
                        self.player.powerUpIndex = -1
                        self.player.is_attacking = False

            if self.player.powerUpIndex == constants.SPEED:
                self.powerUpLast = pygame.time.get_ticks()
                self.player.powerUpIndex = -1
                config.SPEED *= 3
            
            if self.player.powerUpIndex == constants.NIGHT_VISION:
                self.powerUpLast = pygame.time.get_ticks()
                self.player.powerUpIndex = -1
                self.player.night_vis = True
            
            if self.player.powerUpIndex == constants.INVISIBILITY:
                self.powerUpLast = pygame.time.get_ticks()
                self.player.powerUpIndex = -1
                self.player.is_invisible = True
            
            
            
                
        
                    

        value = 0
        lavaTile = [[0, 0] for _ in range(88)]
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                if tile_type == 'l':
                    lavaTile[value] = [row_index,col_index]
                    value+=1

                value = 0
        lavaTile = [[0, 0] for _ in range(88)]
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                if tile_type == 'l':
                    lavaTile[value] = [row_index,col_index]
                    value+=1

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

        # remove candies
        currPos = (self.player.tiley, self.player.tilex)
        if currPos in self.candies:
            self.player.candy += 1
            self.candies.remove(currPos)

        # Draw the player centered on the screen
        player_draw_x = config.SCREEN_WIDTH // 2 - self.player.rect.width // 2
        player_draw_y = config.SCREEN_HEIGHT // 2 - self.player.rect.height // 2
        self.screen.blit(self.player.image, (player_draw_x, player_draw_y))


    def tileFinding(self):
        valueLava = 0
        valueEasy = 0
        valueMedium = 0
        valueHard =0 
        for row_index, row in enumerate(tile_map.tile_map):
            for col_index, tile_type in enumerate(row):
                #print(tile_type)
                if tile_type == 'l':
                    self.lavaTile[valueLava] = [row_index,col_index]
                    valueLava+=1


    def lavaTileActivation(self):
        current_time_2 = time.time()
        for i in range(0,len(self.lavaTile)):
            if (self.player.tiley == self.lavaTile[i][0]) and (self.player.tilex == self.lavaTile[i][1]):
                if self.time_of_moves == 0:
                    self.player.candy -= 5 if self.player.candy > 5 else self.player.candy
                    self.vignetteColourR = 200
                    self.createVignetteEffect()
                    self.time_of_moves = current_time_2
                else:
                    if ((self.time_of_moves - current_time_2) < -1):
                        self.player.candy -= 5 if self.player.candy > 5 else self.player.candy
                        self.vignetteColourR = 200
                        self.createVignetteEffect()
                        self.time_of_moves = current_time_2
            else:
                self.vignetteColourR = 0
                # UNCOMMENT IF YOU WANT FULL RED & FLASH RATHER THAN JUST FLASH ON DMG TICK
                # self.vignetteColorR = 255
                # self.createVignetteEffect()

    def quizTiles(self):
        easy = constants.easy_questions
        medium = constants.medium_questions
        hard = constants.hard_questions


        if (self.easyTile_activ == 1) or (self.mediumTileTil_activ == 1) or (self.hardTile_activ == 1):
            trivia_ui = pygame.image.load("assets/ui/trivia.png")
            scaled_trivia_ui = pygame.transform.scale(trivia_ui, (trivia_ui.get_width() * 22, trivia_ui.get_height()*20))
            self.screen.blit(scaled_trivia_ui, (450, 180))
            trivia_text = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 70)
            text = trivia_text.render(f"Terrifying Trivia", True, (255,255,255))
            self.screen.blit(text, (500+32, 180+16))

            one = pygame.image.load("assets/ui/1.png")
            one = pygame.transform.scale(one, (one.get_width() * 8, one.get_height()*8))
            self.screen.blit(one, (480, 500))

            two = pygame.image.load("assets/ui/2.png")
            two = pygame.transform.scale(two, (two.get_width() * 8, two.get_height()*8))
            self.screen.blit(two, (860, 500))

            three = pygame.image.load("assets/ui/3.png")
            three = pygame.transform.scale(three, (three.get_width() * 8, three.get_height()*8))
            self.screen.blit(three, (480, 600))

            four = pygame.image.load("assets/ui/4.png")
            four = pygame.transform.scale(four, (four.get_width() * 8, four.get_height()*8))
            self.screen.blit(four, (860, 600))

            keys = pygame.key.get_pressed()

            



    def casinoTiles(self):
        left = 180
        top = 300
        if self.casinoTile_activ == 1:
            temp = 0
            trivia_ui = pygame.image.load("assets/ui/trivia.png")
            scaled_trivia_ui = pygame.transform.scale(trivia_ui, (trivia_ui.get_width() * 22, trivia_ui.get_height()*20))
            self.screen.blit(scaled_trivia_ui, (450, 180))
            title_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 70)
            text_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 40)
            title = title_font.render(f"Casino", True, (255,255,255))
            self.screen.blit(title, (700, 190))
            sub_script = text_font.render(f"Bet amount", True, (255,255,255))
            self.screen.blit(sub_script, (left+310,top))
            option1 = text_font.render(f"Option 1: {self.player.candy//8}", True, (255,255,255))
            self.screen.blit(option1, (left+310,top+70))
            option2 = text_font.render(f"Option 2: {self.player.candy//4}", True, (255,255,255))
            self.screen.blit(option2, (left+310,top+140))
            option3 = text_font.render(f"Option 3: {self.player.candy//2}", True, (255,255,255))
            self.screen.blit(option3, (left+310,top+210))
            option4 = text_font.render(f"Option 4: {self.player.candy}", True, (255,255,255))
            self.screen.blit(option4, (left+310,top+280))
            reward = title_font.render(f"Exit: x", True, (0,255,0))
            self.screen.blit(reward, (left+700,top+280))
            if (self.casino_opt1 == 1):
                temp = (self.player.candy) // 8
                self.bet_amount = temp
                self.player.candy = (self.player.candy) - temp
            if (self.casino_opt1 == 2):
                temp = (self.player.candy) // 4
                self.bet_amount = self.player.candy
                self.player.candy = (self.player.candy) - temp
            if (self.casino_opt1 == 3):
                temp = (self.player.candy) // 2
                self.bet_amount = self.player.candy
                self.player.candy = (self.player.candy) - temp
            if (self.casino_opt1 == 4):
                self.bet_amount = self.player.candy
                self.player.candy = 0
            if (self.casino_opt1 == 1) or (self.casino_opt1 == 2) or (self.casino_opt1 == 3) or (self.casino_opt1 == 4):
                random_number = random.randint(0,3)
                temp2 = 0
                if (random_number == 1) or (random_number == 0) or (random_number == 2):
                    self.casino_reward = temp * random_number
                if (random_number == 3):
                    self.casino_reward = temp // 2
                self.player.candy += temp2
            reward = title_font.render(f"Reward: {self.casino_reward}", True, (255,0,0))
            self.screen.blit(reward, (left+310,top+350))
            if self.exit == 1:
                self.casinoTile_activ = 0
                self.exit = 0
            self.casino_opt1 = 0



    def resetPowerUps(self):
        now = pygame.time.get_ticks()
        if now - self.powerUpLast > self.powerUpCooldown:
            config.SPEED = config.BASESPEED
            self.player.night_vis = False
            self.player.is_invisible = False
            
            

    def createVignetteEffect(self):
        visionSurface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        visionSurface.fill((self.vignetteColourR, self.vignetteColourG, self.vignetteColourB,240))
        center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2) 
        for radius in range(config.VISION_RADIUS, 0, -30):
            alpha = int(240 * (radius / config.VISION_RADIUS)) 
            pygame.draw.circle(visionSurface, (self.vignetteColourR, self.vignetteColourG, self.vignetteColourB,0 + alpha), center, radius)
        self.screen.blit(visionSurface, (0, 0))

    def valuables_UI(self):
        box_position = ((config.SCREEN_WIDTH/2)-300, 25)
        box_width = (config.SCREEN_WIDTH/2) - 200 
        box_height = 50
        #powerUps_file_location = ("","","","","")
        countdown_time = 200
        current_time = time.time()
        remaining_time = end_time - current_time

        time_amount = 3
        candy_collected = self.player.candy
        

        candy_ui = pygame.image.load("assets/ui/candy.png")
        scaled_candy_ui = pygame.transform.scale(candy_ui, (candy_ui.get_width() * 12, candy_ui.get_height() * 12)) 
        self.screen.blit(scaled_candy_ui, (0,0))

        candy_image = pygame.image.load("assets/tiles/candy_orange.png")
        scaled_candy_image = pygame.transform.scale(candy_image, (candy_image.get_width() * 4, candy_image.get_height() * 4))
        self.screen.blit(scaled_candy_image, (2,2))
        
        font_candy = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 90)
        text = font_candy.render(f"{candy_collected}", True, (255,165,0))
        self.screen.blit(text, (140, 0))

        time_ui = pygame.image.load("assets/ui/timebar.png")
        scaled_time_ui = pygame.transform.scale(time_ui, (time_ui.get_width() * 20, time_ui.get_height() * 25))
        self.screen.blit(scaled_time_ui, (config.SCREEN_WIDTH // 3 - 52,0))

        if (remaining_time >=0):
            bar_width = ((remaining_time/countdown_time) * box_width) -4
            pygame.draw.rect(self.screen, (0,0,0), (*box_position, box_width, box_height), 2)
            pygame.draw.rect(self.screen, (139,0,139), (box_position[0] + 2, box_position[1] + 2, bar_width, box_height-4))
            pygame.draw.rect(self.screen, (128,128,128), (box_position[0] + 2 + bar_width, box_position[1] + 2, ((bar_width-4) - bar_width), box_height-4))
            remaining_time = int(remaining_time)
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            
            font_countdown = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 40)
            text = font_countdown.render(f"{minutes:02}:{seconds:02}", True, (139,0,139))
            self.screen.blit(text, ((config.SCREEN_WIDTH/2)-46, 75))

        powerup_ui = pygame.image.load("assets/ui/powerup.png")
        scaled_powerup_ui = pygame.transform.scale(powerup_ui, (powerup_ui.get_width() * 12, powerup_ui.get_height() * 12))
        self.screen.blit(scaled_powerup_ui, (config.SCREEN_WIDTH-(32 * 12), 0))

        # render current powerup
        if self.player.powerUpIndex != -1:
            powerUpImage = tile_map.powerUps[self.player.powerUpIndex]
            scaledPowerupImage = pygame.transform.scale(powerUpImage, (powerup_ui.get_width() * 6, powerup_ui.get_height() * 6))
            self.screen.blit(scaledPowerupImage, (config.SCREEN_WIDTH-(19 * 12), 45))


        #powerUps_image = pygame.image.load(powerUps_file_location[powerUp_index])
        #scaled_power_image = pygame.transform.scale(powerUps_image, (powerUps_image.get_width() * 4, powerUps_image.get_height() * 4))
        #self.screen.blit(scaled_power_image, (config.SCREEN_WIDTH-20,20))

    def getOffset(self):
        offsetx = self.player.rect.x - config.SCREEN_WIDTH // 2 + config.TILE_SIZE // 2
        offsety = self.player.rect.y - config.SCREEN_HEIGHT // 2 + config.TILE_SIZE // 2
        return offsetx, offsety

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
            
            if agent.tilex == self.player.tilex and agent.tiley == self.player.tiley and random.randint(1, 10) == 1 and not self.player.is_invisible:
                candy_stolen = self.player.candy // 5
                self.player.candy -= candy_stolen
                agent.candy += candy_stolen
                agent.reward += candy_stolen
            
            self.screen.blit(agent.image, (agent.rect.x - self.offsetx, agent.rect.y - self.offsety))

    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.drawTileMap()
            self.move()
            self.tileFinding()
            self.lavaTileActivation()
            self.player.updateAnimation()
            self.moveAgents()
            self.handleEvent()
            if not self.player.night_vis:
                self.createVignetteEffect()
            self.quizTiles()
            self.casinoTiles()
            self.valuables_UI()
            self.powerUp()
            self.resetPowerUps()
            self.messageMaintainer()
            self.messageBox()
            pygame.display.flip()

    def drawTileMap(self):
        offset_x, offset_y = self.getOffset()
        
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
                if tile_type not in ['.', 't', 'l', 'e', 'm', 'h'] and random.random() < 0.01:
                    self.candies.append((row_index, col_index))

    def openChest(self, r, c):
        if self.player.powerUpIndex == -1:
            tile_map.tile_map[r][c] = random.choice(['i','n','k','s']) 
        
    def pickUpPowerUp(self, r, c):
        if tile_map.tile_map[r][c] == 'k':
            self.player.powerUpIndex = constants.KNIFE
            self.message.append("You just got a candy knife!") 
        elif tile_map.tile_map[r][c] == 's':
            self.player.powerUpIndex = constants.SPEED
            self.message.append("You just got a speed potion!") 
        elif tile_map.tile_map[r][c] == 'i':
            self.player.powerUpIndex = constants.INVISIBILITY
            self.message.append("You just got an invisibility potion!") 
        elif tile_map.tile_map[r][c] == 'n':
            self.player.powerUpIndex = constants.NIGHT_VISION
            self.message.append("You just got a night vision potion!")
        tile_map.tile_map[r][c] = 'a'

    def messageMaintainer(self):
        if len(self.message) == 4:
            self.message.pop(0)

    def messageBox(self):
        i = config.SCREEN_HEIGHT
        alpha = 180
        for message in self.message:
            font_msg = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 50)
            text = font_msg.render(message, True, (255,255,255))
            text.set_alpha(255-alpha)
            self.screen.blit(text, (50, i-100))
            i -= 50
            alpha -= 30
        

#def draw_bar(screen, coins_collected, max_coins):
#    pygame.draw.rect(screen, BLACK, (*BAR_POS, BAR_WIDTH, BAR_HEIGHT), 2)  # Border
#    fill_width = (coins_collected / max_coins) * (BAR_WIDTH - 4)  # -4 for padding
#    pygame.draw.rect(screen, GREEN, (BAR_POS[0] + 2, BAR_POS[1] + 2, fill_width, BAR_HEIGHT - 4))  # Filled portion
#    text = font.render(f"Coins: {coins_collected}/{max_coins}", True, BLACK)
#    screen.blit(text, (BAR_POS[0] + 5, BAR_POS[1] - 25))  # Above the bar


if __name__ == "__main__":
    game = Game()
    game.run()