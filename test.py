import pygame
import tile_map
import constants
import config
import player
import random
import time
import agent
import torch
import textwrap

end_time = time.time() + 300


def getLocation():
    locationx, locationy = None, None
    for i in range(100):
        for j in range(100):
            if tile_map.tile_map[j][i] == 't':
                if random.randint(0, 3)  == 1:
                    locationy = j
                    locationx = i
                
    return locationx, locationy

class Game:
    MESSAGE_POP = pygame.USEREVENT + 1
    


    def __init__(self, isTraining=False):
        pygame.init()
        pygame.mixer.init()

        # Load and play background music
        pygame.mixer.music.load("assets/bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.is_running = True
        pygame.display.set_caption("CandyCombs")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        player_locationx = None
        player_locationy = None
        self.player = player.Player([["assets/mainCharacterFrames/mainCharacterStanding1.png", "assets/mainCharacterFrames/mainCharacterWalking.png"],
                                     ["assets/mainCharacterFrames/mainCharacterKnifeStanding.png", "assets/mainCharacterFrames/mainCharacterKnifeWalking.png", "assets/mainCharacterFrames/mainCharacterKnifeStabbing.png"],
                                     ["assets/mainCharacterFrames/mainCharacterStarlightStanding.png", "assets/mainCharacterFrames/mainCharacterStartlightWalking.png"],
                                     ["assets/mainCharacterFrames/mainCharcterInvisbleStanding.png","assets/mainCharacterFrames/mainCharacterInvisibleWalking.png"]],
                                     player_locationx, player_locationy)
        locationx, locationy = getLocation()
        self.agent1 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent2 = agent.Agent([["assets/grubby10YrOld/grubby10YrOldStanding.png", "assets/grubby10YrOld/grubby10YrOldWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent3 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent4 = agent.Agent([["assets/skeleton/skeletonStanding.png", "assets/skeleton/skeletonWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent5 = agent.Agent([["assets/skeleton/skeletonStanding.png", "assets/skeleton/skeletonWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent6 = agent.Agent([["assets/skeleton/skeletonStanding.png", "assets/skeleton/skeletonWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent7 = agent.Agent([["assets/skeleton/skeletonStanding.png", "assets/skeleton/skeletonWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent8 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent9 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent10 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent11 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent12 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent13 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]], locationx, locationy)
        locationx, locationy = getLocation()
        self.agent14 = agent.Agent([["assets/minotaur/minotaurStanding.png", "assets/minotaur/minotaurWalking.png"]], None, None)
        locationx, locationy = getLocation()
        self.agent15 = agent.Agent([["assets/grubby10YrOld/grubby10YrOldStanding.png", "assets/grubby10YrOld/grubby10YrOldWalking.png"]], None, None)
        locationx, locationy = getLocation()
        self.agent16 = agent.Agent([["assets/marvoloWizardFrames/marvoloStanding.png", "assets/marvoloWizardFrames/marvoloFloating.png"]], None, None)


        self.agent_group = [self.agent1, self.agent2, self.agent3, self.agent4, self.agent5, self.agent6, self.agent7, self.agent8, self.agent9, self.agent10, self.agent11, self.agent12, self.agent13, self.agent14, self.agent15]
        
        self.random = 0
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
        self.exit = 0
        self.randomQuestion = random.randint(0,4)

        self.isTraining = isTraining

        self.time_of_moves = 0
        self.easyTile_activ = 0
        self.mediumTileTil_activ = 0
        self.hardTile_activ = 0
        self.casinoTile_activ = 0
        self.casino_op1 = 0
        self.casino_reward = 0

        self.easyTile = [[0, 0],[0,0]]
        self.mediumTile = [[0, 0],[0,0]]
        self.hardTile = [[0, 0],[0,0]]
        self.lavaTile = [[0, 0] for _ in range(88)]

        self.animation_time = 0
        self.animation_type = 0
        self.animation = 0
        self.is_load_screen = True
        self.font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 74)
        self.title_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 100)

    def displayLoadScreen(self):

        self.screen.fill((0,0,0))

        # title_text = self.title_font.render("CandyCombs", True, (0, 0, 0))
        # how_to_play_text = self.font.render("How to Play", True, (50, 50, 50))
        # movement_text = self.font.render("Movement : Arrows", True, (50, 50, 50))
        # open_chest_text = self.font.render("Open Chest : O", True, (50, 50, 50))
        # use_power_up_text = self.font.render("Use Power Up : Space ", True, (50, 50, 50))

        # self.screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        # self.screen.blit(how_to_play_text, (config.SCREEN_WIDTH // 2 - how_to_play_text.get_width() // 2, 200))
        
        # instruction_y_offset = 300
        # self.screen.blit(movement_text, (config.SCREEN_WIDTH // 2 - movement_text.get_width() // 2, instruction_y_offset))
        # self.screen.blit(open_chest_text, (config.SCREEN_WIDTH // 2 - open_chest_text.get_width() // 2, instruction_y_offset + 75))
        # self.screen.blit(use_power_up_text, (config.SCREEN_WIDTH // 2 - use_power_up_text.get_width() // 2, instruction_y_offset + 150))
        instructions_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 40)
        title_text = self.title_font.render("CandyCombs", True, (255, 255, 255))  # Black
        #how_to_play_text = self.font.render("How to Play", True, (169, 169, 169))  # Dark Grey
        movement_text = instructions_font.render("Movement : Arrows", True, (255, 165, 0))  # Orange
        open_chest_text = instructions_font.render("Open Chest : O", True, (255, 165, 0))  # Orange
        use_power_up_text = instructions_font.render("Use Power Up : Space", True, (255, 165, 0))  # Orange

        # Game objectives in grey
        game_objective_text = self.font.render("Steal as much candy as you can", True, (0, 0, 0))  # Dark Grey
        enter_text = self.font.render("Click Enter to Start", True, (255, 255, 255))  # Dark Grey

        # Blit texts onto the screen with adjusted spacing
        self.screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        # self.screen.blit(how_to_play_text, (config.SCREEN_WIDTH // 2 - how_to_play_text.get_width() // 2, 350))
        
        # Add spacing by adjusting y-coordinates for each instruction
        self.screen.blit(movement_text, (config.SCREEN_WIDTH // 2 - movement_text.get_width() // 2, 400))
        self.screen.blit(open_chest_text, (config.SCREEN_WIDTH // 2 - open_chest_text.get_width() // 2, 475))  # 50 pixels below
        self.screen.blit(use_power_up_text, (config.SCREEN_WIDTH // 2 - use_power_up_text.get_width() // 2, 550))  # 100 pixels below

        # Add game objective and start instruction at the bottom
        self.screen.blit(game_objective_text, (config.SCREEN_WIDTH // 2 - game_objective_text.get_width() // 2, 600))
        self.screen.blit(enter_text, (config.SCREEN_WIDTH // 2 - enter_text.get_width() // 2, 675))


        pygame.display.flip()

#Movement - arrows
#Open Chest = O
#Use power up = Space (_)

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.isTraining:
                    torch.save(self.agent1.model.state_dict(), "trained_models/agent_model.pt")
                self.is_running = False

            if self.is_load_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.is_load_screen = False
                        global end_time
                        end_time = time.time() + 90
            
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
                        self.casino_op1 = 1
                    if event.key == pygame.K_2:
                        self.casino_op1 = 2
                    if event.key == pygame.K_3:
                        self.casino_op1 = 3
                    if event.key == pygame.K_4:
                        self.casino_op1 = 4
                    if event.key == pygame.K_x:
                        self.exit = 1
                    
            elif event.type == game.MESSAGE_POP:
                    if self.message:
                        self.messagePop()


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
                if tile_type == 'e':
                    self.easyTile[valueEasy] = [row_index,col_index]
                if tile_type == 'm':
                    self.easyTile[valueMedium] = [row_index,col_index]
                if tile_type == 'h':
                    self.easyTile[valueHard] = [row_index,col_index]


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

        keys = pygame.key.get_pressed()

        if(self.easyTile_activ == 1):
                if self.player.candy < 2:
                    self.message.append("You cannot afford this")
                    self.exit = 1
                else:
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
                    i = self.randomQuestion
                    offset = 0
                    question = easy[i][0]
                    sub_array = question.split("$")
                    for line in sub_array:
                        trivia_question = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 30)
                        question_text = trivia_question.render(f"{line}", True, (255,255,255))
                        self.screen.blit(question_text, (500,400+offset))
                        offset += 50
                    answer = easy[i][5]
                    chosen = -1
                    

                    #answer text
                    oneAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    oneAnswerText = oneAnswer.render(f"{easy[i][1]}", True, (255,255,255))
                    self.screen.blit(oneAnswerText, (550,600))

                    twoAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    twoAnswerText = twoAnswer.render(f"{easy[i][2]}", True, (255,255,255))
                    self.screen.blit(twoAnswerText, (930,600))

                    threeAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    threeAnswerText = threeAnswer.render(f"{easy[i][3]}", True, (255,255,255))
                    self.screen.blit(threeAnswerText, (550,700))

                    fourAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    fourAnswerText = fourAnswer.render(f"{easy[i][4]}", True, (255,255,255))
                    self.screen.blit(fourAnswerText, (930,700))
                    
                    if keys[pygame.K_1]:
                        chosen = 0
                    elif keys[pygame.K_2]:
                        chosen = 1
                    elif keys[pygame.K_3]:
                        chosen = 2
                    elif keys[pygame.K_4]:
                        chosen = 3
                    if chosen == answer:
                        self.player.candy += 2
                        self.message.append("You got it right and gained 2 candy")
                        tile_map.tile_map[self.player.tilex][self.player.tiley] = 'a'
                        self.exit = 1
                    elif chosen != answer and chosen != -1:
                        self.player.candy -= 2
                        self.message.append("You got it wrong and lost 2 candy")
                        tile_map.tile_map[self.player.tilex][self.player.tiley] = 'a'   
                        self.exit = 1
            
        if(self.mediumTileTil_activ == 1):
                if self.player.candy < 4:
                    self.message.append("You cannot afford this")
                    self.exit = 1
                else:
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
                    i = self.randomQuestion
                    question = medium[i][0]
                    answer = medium[i][5]
                    chosen = -1
                    offset = 0
                    sub_array = question.split("$")
                    for line in sub_array:
                        trivia_question = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 30)
                        question_text = trivia_question.render(f"{line}", True, (255,255,255))
                        self.screen.blit(question_text, (500,400+offset))
                        offset += 50

                    #answer text
                    oneAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    oneAnswerText = oneAnswer.render(f"{medium[i][1]}", True, (255,255,255))
                    self.screen.blit(oneAnswerText, (550,600))

                    twoAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    twoAnswerText = twoAnswer.render(f"{medium[i][2]}", True, (255,255,255))
                    self.screen.blit(twoAnswerText, (930,600))

                    threeAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    threeAnswerText = threeAnswer.render(f"{medium[i][3]}", True, (255,255,255))
                    self.screen.blit(threeAnswerText, (550,700))

                    fourAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    fourAnswerText = fourAnswer.render(f"{medium[i][4]}", True, (255,255,255))
                    self.screen.blit(fourAnswerText, (930,700))
                    
                    if keys[pygame.K_1]:
                        chosen = 0
                    elif keys[pygame.K_2]:
                        chosen = 1
                    elif keys[pygame.K_3]:
                        chosen = 2
                    elif keys[pygame.K_4]:
                        chosen = 3
                    if chosen == answer:
                        self.player.candy += 4
                        self.message.append("You got it right and gained 4 candy")
                        tile_map.tile_map[self.player.tilex][self.player.tiley] = 'a'
                        self.exit = 1
                    elif chosen != answer and chosen != -1:
                        self.player.candy -= 4
                        self.message.append("You got it wrong and lost 4 candy")
                        self.exit = 1

        if(self.hardTile_activ == 1):
                if self.player.candy < 8:
                    self.message.append("You cannot afford this")
                    self.exit = 1
                else:
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
                    i = self.randomQuestion
                    question = hard[i][0]
                    answer = hard[i][5]
                    chosen = -1
                    offset = 0
                    sub_array = question.split("$")
                    for line in sub_array:
                        trivia_question = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 30)
                        question_text = trivia_question.render(f"{line}", True, (255,255,255))
                        self.screen.blit(question_text, (500,400+offset))
                        offset += 50

                    #answer text
                    oneAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    oneAnswerText = oneAnswer.render(f"{hard[i][1]}", True, (255,255,255))
                    self.screen.blit(oneAnswerText, (550,600))

                    twoAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    twoAnswerText = twoAnswer.render(f"{hard[i][2]}", True, (255,255,255))
                    self.screen.blit(twoAnswerText, (930,600))

                    threeAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    threeAnswerText = threeAnswer.render(f"{hard[i][3]}", True, (255,255,255))
                    self.screen.blit(threeAnswerText, (550,700))

                    fourAnswer = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 25)
                    fourAnswerText = fourAnswer.render(f"{hard[i][4]}", True, (255,255,255))
                    self.screen.blit(fourAnswerText, (930,700))
                    
                    if keys[pygame.K_1]:
                        chosen = 0
                    elif keys[pygame.K_2]:
                        chosen = 1
                    elif keys[pygame.K_3]:
                        chosen = 2
                    elif keys[pygame.K_4]:
                        chosen = 3
                    if chosen == answer:
                        self.player.candy += 8
                        self.message.append("You got it right and gained 8 candy")
                        tile_map.tile_map[self.player.tilex][self.player.tiley] = 'a'
                        self.exit = 1
                    elif chosen != answer and chosen != -1:
                        self.player.candy -= 8
                        self.message.append("You got it wrong and lost 8 candy")
                        self.exit = 1
            
        if self.exit == 1:
            self.easyTile_activ = 0
            self.hardTile_activ = 0
            self.mediumTileTil_activ = 0
            self.casinoTile_activ = 0
            self.randomQuestion = random.randint(0,4)
            self.exit = 0


            


            



    def casinoTiles(self):
        top = 450
        left = 180
        wheel = ["assets/ui/wheel_green.png","assets/ui/wheel_orange.png","assets/ui/wheel_red.png","assets/ui/wheel_blue.png"]
        if self.casinoTile_activ == 1:
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
            self.screen.blit(reward, (left+700,top+360))
            wheel_ui = pygame.image.load(wheel[self.animation_type])
            scaled_wheel_ui = pygame.transform.scale(wheel_ui, (trivia_ui.get_width() * 10, trivia_ui.get_height()*10))
            self.screen.blit(scaled_wheel_ui, (800, top+50))
            if self.animation != 1:
                if (self.casino_op1 == 1):
                    temp = (self.player.candy) // 8
                    self.bet_amount = temp
                    self.player.candy = (self.player.candy) - temp
                    self.animation = 1
                    self.animation_type = 0
                if (self.casino_op1 == 2):
                    temp = (self.player.candy) // 4
                    self.bet_amount = temp
                    self.player.candy = (self.player.candy) - temp
                    self.animation = 1
                    self.animation_type = 1
                if (self.casino_op1 == 3):
                    temp = (self.player.candy) // 2
                    self.bet_amount = temp
                    self.player.candy = (self.player.candy) - temp
                    self.animation = 1
                    self.animation_type = 2
                if (self.casino_op1 == 4):
                    self.bet_amount = self.player.candy
                    self.player.candy = 0
                    self.animation = 1
                    self.animation_type = 3
                if (self.casino_op1 == 1) or (self.casino_op1 == 2) or (self.casino_op1 == 3) or (self.casino_op1 == 4):
                    self.random = random.randint(0,3)
                    if (self.random == 1) or (self.random == 0) or (self.random == 2):
                        self.casino_reward = self.bet_amount * self.random
                    elif (self.random == 3):
                        self.casino_reward = self.bet_amount // 2
                    self.player.candy += self.casino_reward
                    self.casino_op1 = 0
            if self.animation == 1 and self.animation_time < 7:
                if (pygame.time.get_ticks() % 15) == 0:
                    self.animation_time += 1
                    random_2 = random.randint(0,3)
                    self.animation_type = random_2
            if self.animation == 1 and self.animation_time == 7:
                self.animation_type = self.random
                self.animation = 0
                self.animation_time = 0
            reward = title_font.render(f"Reward: {self.casino_reward}", True, (255,0,0))
            self.screen.blit(reward, (left+310,top+360))
            if self.exit == 1:
                self.casinoTile_activ = 0
                self.exit = 0

    def resetPowerUps(self):
        now = pygame.time.get_ticks()
        if now - self.powerUpLast > self.powerUpCooldown:
            config.SPEED = config.BASESPEED
            self.night_vis = False
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
        countdown_time = 300
        current_time = time.time()
        if self.is_load_screen == False:
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
                agent.speedx = random.randint(-10, 10)
                agent.speedy = random.randint(-10, 10)
                agent.rect.x = prevx
                agent.rect.y = prevy
            
            if agent.tilex == self.player.tilex and agent.tiley == self.player.tiley and random.randint(1, 10) == 1:
                candy_stolen = self.player.candy // 5
                self.player.candy -= candy_stolen
                agent.candy += candy_stolen
            
            self.screen.blit(agent.image, (agent.rect.x - self.offsetx, agent.rect.y - self.offsety))

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
            tile_map.tile_map[r][c] = random.choice(['i','k','s','n']) 
        
    def pickUpPowerUp(self, r, c):
        if tile_map.tile_map[r][c] == 'k':
            self.player.powerUpIndex = constants.KNIFE
            self.message.append("You just got a candy knife") 
        elif tile_map.tile_map[r][c] == 's':
            self.player.powerUpIndex = constants.SPEED
            self.message.append("You just got a speed potion")
        elif tile_map.tile_map[r][c] == 'i':
            self.player.powerUpIndex = constants.INVISIBILITY
            self.message.append("You just got an invisibility potion") 
        elif tile_map.tile_map[r][c] == 'n':
            self.player.powerUpIndex = constants.NIGHT_VISION
            self.message.append("You just got a night vision potion")
        tile_map.tile_map[r][c] = 'a'

    def messageMaintainer(self):
        if len(self.message) == 4:
            self.messagePop()
    
    def messagePop(self):
        if len(self.message) == 4:
            temp3 = self.message[3]
            temp2 = self.message[2]
            temp1 = self.message[1]
            self.message.pop()
            self.message[0] = temp1
            self.message[1] = temp2
            self.message[2] = temp3
        elif len(self.message) == 3:
            temp2 = self.message[2]
            temp1 = self.message[1]
            self.message.pop()
            self.message[0] = temp1
            self.message[1] = temp2
        elif len(self.message) == 2:
            temp1 = self.message[1]
            self.message.pop()
            self.message[0] = temp1
        elif len(self.message) == 1:
            self.message = [""]


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
    

    def show_end_screen(self):
        # Fill the screen with a background color
        self.screen.fill((0, 0, 0))  # Black background

        # Load or set font for the end screen
        end_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 40)
        message_font = pygame.font.Font("assets/fonts/PixemonTrialRegular-p7nLK.ttf", 30)

        # Display the game over message
        end_text = end_font.render("Game Over", True, (255, 0, 0))  # Red color
        end_rect = end_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(end_text, end_rect)

        # Display the final score or candy collected
        final_score_text = message_font.render(f"Total Candy Collected: {self.player.candy}", True, (255, 255, 255))
        score_rect = final_score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, score_rect)

        # Display restart and quit instructions
        restart_text = message_font.render("Press Q to Quit", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()  # Update the screen

        # Wait for player input to restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_q:  # Quit the game
                        self.is_running = False
                        waiting = False

    
    def run(self):
        while self.is_running:
            self.clock.tick(config.FPS)
            self.handleEvent()
            if self.is_load_screen:
                self.displayLoadScreen()
            else:
                self.drawTileMap()
                self.move()
                self.tileFinding()
                self.lavaTileActivation()
                self.quizTiles()
                self.casinoTiles()
                self.player.updateAnimation()
                self.moveAgents()
                if not self.player.night_vis:
                    self.createVignetteEffect()
                if self.is_load_screen == False:
                    self.valuables_UI()
                self.powerUp()
                self.resetPowerUps()
                self.messageMaintainer()
                self.messageBox()
                if time.time() > end_time:
                    self.show_end_screen()  # Display end screen
                    break  # Exit the game loop
                pygame.display.flip()



#def draw_bar(screen, coins_collected, max_coins):
#    pygame.draw.rect(screen, BLACK, (*BAR_POS, BAR_WIDTH, BAR_HEIGHT), 2)  # Border
#    fill_width = (coins_collected / max_coins) * (BAR_WIDTH - 4)  # -4 for padding
#    pygame.draw.rect(screen, GREEN, (BAR_POS[0] + 2, BAR_POS[1] + 2, fill_width, BAR_HEIGHT - 4))  # Filled portion
#    text = font.render(f"Coins: {coins_collected}/{max_coins}", True, BLACK)
#    screen.blit(text, (BAR_POS[0] + 5, BAR_POS[1] - 25))  # Above the bar


if __name__ == "__main__":
    game = Game()
    game.run()