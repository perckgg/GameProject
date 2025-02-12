import pygame
import random
from pygame import *
from Classes.GameDefine import Constants, Zombie
from Classes.SoundEffect import SoundEffect

class Game:
    def __init__(self):
        # Initialize screen and title
        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        pygame.display.set_caption(Constants.GAME_TITLE)
        self.background = pygame.image.load(Constants.IMAGE_BG)

        # Font for displaying text
        self.font_obj = pygame.font.Font(Constants.FONT_NAME, Constants.FONT_SIZE)

        # Initialize 3 label: level - hits - misses
        self.hits = 0
        self.misses = 0
        self.level = 1
        self.lives = 3
        self.high_score = self.load_high_score() #preload high score from previous play

        self.zombies = []

        # Position of the graves in background
        self.grave_positions = []
        self.grave_positions.append(Constants.GRAVE_POS_1)
        self.grave_positions.append(Constants.GRAVE_POS_2)
        self.grave_positions.append(Constants.GRAVE_POS_3)
        self.grave_positions.append(Constants.GRAVE_POS_4)
        self.grave_positions.append(Constants.GRAVE_POS_5)
        self.grave_positions.append(Constants.GRAVE_POS_6)
        self.grave_positions.append(Constants.GRAVE_POS_7)
        self.grave_positions.append(Constants.GRAVE_POS_8)

        # Initialize zombie's sprite sheet - 6 states    
        zombie_sprite_sheet = pygame.image.load(Constants.IMAGE_ZOMBIE)
        self.zombie = []
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_1))
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_2))
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_3))
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_4))
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_5))
        self.zombie.append(zombie_sprite_sheet.subsurface(Constants.ZOM_SPRITE_6))

        # Initialize hammer image
        self.hammer_image = pygame.image.load(Constants.IMAGE_HAMMER).convert_alpha()
        self.hammer_image_rotate = transform.rotate(self.hammer_image.copy(), Constants.HAMMER_ANGLE)

        # Initialize sound effects
        self.soundEffect = SoundEffect()
        

    # Calculate the level up based on current hit & LEVEL_HIT_GAP
    def getPlayerLevel(self):
        nextLevel = int(self.hits / Constants.LEVEL_UP_GAP) + 1
        if nextLevel != self.level:         
            self.soundEffect.playLevelUpSound() # Play sound level up
        return nextLevel

    # Calculate the time respawning new zombie
    def getStayTime(self, timeToRespawn):
        timeToRespawn = Constants.RESPAWN_TIME - self.level * Constants.RESPAWN_DELTA_TIME
        if timeToRespawn <= Constants.RESPAWN_DELTA_TIME:
            timeToRespawn = Constants.RESPAWN_DELTA_TIME
        return timeToRespawn

    # Check if the mouse hits zombie or not
    def isZombieHit(self, mouse_position, current_grave_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_grave_position[0]
        current_hole_y = current_grave_position[1]
        distanceX = mouse_x - current_hole_x
        distanceY = mouse_y - current_hole_y
        if (0 < distanceX < Constants.ZOM_WIDTH) and (0 < distanceY < Constants.ZOM_HEIGHT):
            return True
        else:
            return False
    def generateZombies(self, num_zombies):
        if len(self.zombies) + num_zombies > Constants.MAX_ZOMBIES:  # Check if maximum zombies reached
            return 0
        spawnIndices = random.choices(range(Constants.GRAVE_NUM_MAX), num_zombies)  # Generate multiple spawn indices
        for spawnIndex in spawnIndices:
            newZombie = Zombie(spawnIndex, self.zombie[0])  # Create a new zombie
            self.zombies.append(newZombie)
        return 1

    # Update, rotate the hammer
    def update_hammer(self, mouse_position, image, image_rotate, isHit):
        mouse_x = mouse_position[0] - Constants.HAMMER_DISTANCE_X   
        mouse_y = mouse_position[1] - Constants.HAMMER_DISTANCE_Y
        if isHit:
            self.screen.blit(image_rotate, [mouse_x, mouse_y])
        else:
            self.screen.blit(image, [mouse_x, mouse_y])

    # Update the zombie animation, re-calculate the player's hits, misses, level
    def update_sprite(self, image, graveStoneIndex, isHit):
        # Update the zombie animation
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(image, (self.grave_positions[graveStoneIndex]))
        self.update_hammer(mouse.get_pos(), self.hammer_image, self.hammer_image_rotate, isHit)

        # Update the player's hits
        current_hit_string = Constants.HIT_TEXT + str(self.hits)
        hit_text = self.font_obj.render(current_hit_string, True, Constants.TEXT_COLOR)
        hit_text_pos = hit_text.get_rect()
        hit_text_pos.centerx = Constants.HIT_POS
        hit_text_pos.centery = Constants.FONT_SIZE
        self.screen.blit(hit_text, hit_text_pos)

        # Update the player's misses
        current_misses_string = Constants.MISS_TEXT + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, Constants.TEXT_COLOR)
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = Constants.MISS_POS
        misses_text_pos.centery = Constants.FONT_SIZE
        self.screen.blit(misses_text, misses_text_pos)

        # Update the player's level
        current_level_string = Constants.LEVEL_TEXT + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, Constants.TEXT_COLOR)
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = Constants.LEVEL_POS
        level_text_pos.centery = Constants.FONT_SIZE
        self.screen.blit(level_text, level_text_pos)

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def render_high_score(self):
        current_high_score_text = Constants.HIGH_SCORE_TEXT + str(self.high_score)
        high_score_text = self.font_obj.render(current_high_score_text, True, Constants.TEXT_COLOR)
        high_score_text_pos = high_score_text.get_rect()
        high_score_text_pos.centerx = Constants.HIGH_SCORE_POS
        high_score_text_pos.centery = Constants.FONT_SIZE
        self.screen.blit(high_score_text, high_score_text_pos)
    
    def render_lives(self):
        current_lives_text = Constants.LIVES_TEXT + str(self.lives)
        lives_text = self.font_obj.render(current_lives_text, True, Constants.TEXT_COLOR)
        lives_text_pos = lives_text.get_rect()
        lives_text_pos.centerx = Constants.SCREEN_WIDTH // 2
        lives_text_pos.centery = Constants.SCREEN_HEIGHT - Constants.FONT_SIZE
        self.screen.blit(lives_text, lives_text_pos)

    def show_end_screen(self):
        self.font_obj_end = pygame.font.Font(Constants.FONT_NAME, Constants.FONT_SIZE_OVER)
        game_over_text = self.font_obj_end.render('Game Over', True, Constants.TEXT_COLOR)
        game_over_text_pos = game_over_text.get_rect()
        game_over_text_pos.centerx = Constants.SCREEN_WIDTH // 2
        game_over_text_pos.centery = Constants.SCREEN_HEIGHT // 2
        self.screen.blit(game_over_text, game_over_text_pos)
        
        pygame.display.flip()
    def game_over(self):
        if self.lives == 0:
            self.show_end_screen()
            pygame.time.wait(3000)  # Wait for 2 seconds
            pygame.quit()
    # Start the game's main loop
    def start(self):
        isHit = False # Check if zombie is hit or not
        cycle_time = 0  # Count clock's time
        hammer_time = 0
        animationIndex = -1
        loop = True
        is_down = False
        graveStoneIndex = 0
        zombieStatus = 1
        spawnAnimationIndex = 0
        deadAnimationIndex = 3
        stayTime = 0
        timeToRespawn = 1.5
        gameTime = 0
        lastSpawnTime = 0
        respawnTime = 0.3
        pic = self.zombie[0]
        mouse.set_visible(False)
        clock = pygame.time.Clock()  # Time variables

        for i in range(len(self.zombie)):
            self.zombie[i].set_colorkey((0, 0, 0))
            self.zombie[i] = self.zombie[i].convert_alpha()     

        while loop:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == MOUSEBUTTONDOWN and event.button == Constants.LEFT_MOUSE_BUTTON:
                    if self.isZombieHit(mouse.get_pos(), self.grave_positions[graveStoneIndex]):
                        zombieStatus = 3
                        is_down = False
                        self.hits += 1
                        self.level = self.getPlayerLevel()
                        timeToRespawn = self.getStayTime(timeToRespawn)
                        self.soundEffect.playHitSound() # Play hit sound effect
                        isHit = True
                    else:
                        self.misses += 1
                        self.soundEffect.playMissSound() # Play miss sound effect
                        isHit = False 
                    if self.hits > self.high_score:
                        self.high_score = self.hits
                        self.save_high_score()                 

            mil = clock.tick(Constants.FPS)
            sec = mil / 1000.0
            cycle_time += sec
            if (zombieStatus == 1): # Zombie status: Go up
                if cycle_time > Constants.SPAWN_ANI_TIME:
                    if spawnAnimationIndex > Constants.SPAWN_ANI_INDEX_MAX:
                        stayTime += sec
                        #self.update_sprite(pic, graveStoneIndex, isHit)
                        if(stayTime > timeToRespawn):
                            spawnAnimationIndex = Constants.SPAWN_ANI_INDEX_MAX
                            zombieStatus = 2
                            stayTime = 0
                            continue
                    else:
                        pic = self.zombie[spawnAnimationIndex]
                        spawnAnimationIndex += 1
                        #self.update_sprite(pic, graveStoneIndex, isHit)
                        cycle_time = 0

            if (zombieStatus == 2): # Zombie status: Go down
                if cycle_time > Constants.SPAWN_ANI_TIME:
                    pic = self.zombie[spawnAnimationIndex]
                    spawnAnimationIndex -= 1
                    #self.update_sprite(pic, graveStoneIndex, isHit)
                    cycle_time = 0
                    if spawnAnimationIndex < 0:
                        spawnAnimationIndex = 0
                        zombieStatus = 1
                        self.lives -= 1
                        graveStoneIndex = random.randint(0, Constants.GRAVE_NUM_MAX - 1)
                        # self.generateZombie()

            if (zombieStatus == 3): #Zombie status: Dead
                if cycle_time > Constants.DEAD_ANI_TIME:
                    pic = self.zombie[deadAnimationIndex]
                    deadAnimationIndex += 1
                    #self.update_sprite(pic, graveStoneIndex, isHit)
                    cycle_time = 0
                    if deadAnimationIndex > Constants.DEAD_ANI_INDEX_MAX:
                        spawnAnimationIndex = 0
                        pic = self.zombie[spawnAnimationIndex]
                        deadAnimationIndex = 3
                        zombieStatus = 1
                        graveStoneIndex = random.randint(0, Constants.GRAVE_NUM_MAX - 1)
                        # self.generateZombie()

            self.update_sprite(pic, graveStoneIndex, isHit)
            self.render_high_score()
            if gameTime - lastSpawnTime > respawnTime:
                if self.generateZombies(min(math.floor(math.log(self.level, 2)), Constants.MAX_ZOMBIES)):
                    lastSpawnTime = gameTime

            self.render_lives()
            self.game_over()

            #Check hammer animation
            hammer_time += sec
            if (hammer_time > Constants.HAMMER_ANI_TIME) & (isHit):
                hammer_time = 0
                isHit = False

            # Update the display     
            pygame.display.flip()

###########################################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Start game - Run main loop
myGame = Game()
myGame.start()

# Exit game if the main loop ends
pygame.quit()
