import pygame as pg
import random
from GameDefine import *
import logging as log
import math

log.basicConfig(level=log.DEBUG, format="%(levelname)s: %(message)s")

# Constants

#Initilize screen for game
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    system_events = None
    game_events = {pg.QUIT: None, pg.MOUSEBUTTONDOWN: None, pg.MOUSEBUTTONUP: None, pg.KEYDOWN: None, pg.KEYUP: None, "resume": None, 'restart': None}

    def __init__(self):
        self.entity_manager = EntityManager()

        # Static entity
        self.init()
    def init(self):
        self.entity_manager = EntityManager()

        # Static entity
        self.static_entity = Entity("Static")
        self.static_entity.add_component(StaticComponent())
        self.static_entity.add_component(RestartButtonComponent())
        self.entity_manager.add_entity(self.static_entity)

        self.zombie_entity = Entity("Zombie")
        self.zombie_entity.add_component(ZombieComponent())
        self.zombie_entity.add_component(TransformComponent())
        self.entity_manager.add_entity(self.zombie_entity)

        self.hammer_entity = Entity("Hammer")
        self.hammer_entity.add_component(HammerComponent())
        self.hammer_entity.add_component(TransformComponent())
        self.entity_manager.add_entity(self.hammer_entity)

        self.score_enity = Entity("Score")
        self.score_enity.add_component(ScoreComponent())
        self.entity_manager.add_entity(self.score_enity)

        self.entity_manager.add_system(CollisionSystem())
        self.entity_manager.add_system(UpdatePlayerScoreSystem()) 

        self.entity_manager.init()
    def update(self):

        # Update events
        for event in Game.system_events:
            if event.type == pg.QUIT:
                return pg.QUIT
            Game.game_events[event.type] = event

        self.entity_manager.update()

        if Game.game_events[pg.QUIT]: return pg.QUIT
    def render(self):
        self.entity_manager.draw()

    def clean(self):
        # Reset game events
        events = Game.game_events

        resume = Game.game_events['resume']

        for key in events:
            if key == 'restart':
                if Game.game_events[key]:
                    print("RESTART")
                    self.init()
                    Game.game_events['restart'] = None
                    Game.game_events['resume'] = None
            elif key != 'resume': 
                Game.game_events[key] = None


    
# ECS for game "Whacking zombies"
# Entities: player, zombie, score
# Components: position, sprite, health, score
# Systems: movement, collision, rendering, scoring

class EntityManager:
    def __init__(self):
        self.entities = {}
        self.systems = []
    def add_entity(self, entity):
        self.entities[entity.name] = entity
    def get_entity(self, name):
        return self.entities[name]
    def add_system(self, system):
        self.systems.append(system)
        system.entity_manager = self
    def draw(self):
        for entity in self.entities.values():
            entity.draw()
    def update(self):
        for system in self.systems:
            system.process()
        for entity in self.entities.values():
            entity.update()
    def init(self):
        for entity in self.entities.values():
            entity.init()
# Entities
class Entity:
    def __init__(self, name):
        self.components = {}  
        self.name = name
    #component is name of class
    def get_component(self, component):
        return self.components[component.__name__]
    
    def add_component(self, component):
        self.components[component.__class__.__name__] = component
        component.entity = self

    def draw(self):
        for component in self.components.values():
            component.draw()

    def update(self):
        for component in self.components.values():
            component.update()

    def init(self):
        for component in self.components.values():
            component.init()

# Components
class Component:
    def __init__(self):
        pass
    def draw(self):
        if Game.game_events['resume']: 
            return False
        return True
    def update(self):
        pass
    def init(self):
        pass

class StaticComponent(Component):
    def __init__(self):
        self.bgMusic = pg.mixer.music.load(SoundConstants.SOUND_BG)
        pg.mixer.music.play(-1)
        self.background = pg.image.load(ImageConstants.IMAGE_BG)
    def draw(self):
        if not(super().draw()): return
        screen.blit(self.background, (0, 0))
    def update(self):
        pass
    def handle_event(self, event):
        pass
    def init(self):
        pass

class HammerComponent(Component):
    def __init__(self):
        self.hit = 0
        self.hammer_image = pg.image.load(ImageConstants.IMAGE_HAMMER)
        self.hammer_rotated_image = pg.transform.rotate(self.hammer_image, 45)

        self.hammer = self.hammer_image
        self.image_size = self.hammer.get_size()

        self.animation_speed = 3

    def draw(self):
        if not(super().draw()): return
        #Make mouse position as center of hammer
        screen.blit(self.hammer, (pg.mouse.get_pos()[0] - self.image_size[0] / 2, pg.mouse.get_pos()[1] - self.image_size[1] / 2))

    def update(self):
        if self.hit:
            if self.animation_speed > 0:
                self.animation_speed -= 1
            else:
                self.animation_speed = 3
                self.hit = 0
                self.hammer = self.hammer_image
        self.handle_event()

    #Animation when user use left mouse button
    def handle_event(self):
        event = Game.game_events[pg.MOUSEBUTTONDOWN]
        if event and event.button == 1:
            self.hammer = self.hammer_rotated_image
            self.hit = 1

    def init(self):
        pass

class ZombieComponent(Component):

    def __init__(self):
        self.is_hidden = True
        self.is_hit = False
        self.grave_index = 0
        self.escape_count = 0

        self.zombie_img = [pg.transform.scale(pg.image.load(i), (int(pg.image.load(i).get_width() * 2 / 3), int(pg.image.load(i).get_height() * 2 / 3))) for i in ImageConstants.IMAGE_ZOMBIE]
        self.zombie_hit_img = [pg.transform.scale(pg.image.load(i), (int(pg.image.load(i).get_width() * 2 / 3), int(pg.image.load(i).get_height() * 2 / 3))) for i in ImageConstants.IMAGE_ZOMBIE_HIT]

        # Field for handling animation
        self.hidding_index = self.hidding_speed = ZombieConstants.HIDDING_SPEED # Caculate by frame
        self.showing_index = self.showing_speed = ZombieConstants.SHOWING_SPEED # Caculate by frame 
        self.is_hit_index =  self.is_hit_speed = ZombieConstants.IS_HIT_SPEED

        self.animation_index = 0
        self.animation_state = 1

        self.sprite = self.zombie_img[0]
        
    def init(self):
        pass
    def draw(self):
        if not(super().draw()): return
        dest = self.entity.get_component(TransformComponent).dest
        if not(self.is_hidden):
            screen.blit(self.sprite, dest)
            # screen.blit(self.sprite, GraveConstants.GRAVE_POS[self.grave_index])
    def update(self):
        self.update_animation()
        self.update_transform()
        
    def handle_event(self, event):
        pass
    def update_animation(self):
        if self.is_hidden:
            if self.hidding_index > 0:
                self.hidding_index -= 1
                return
            else:
                self.hidding_index = ZombieConstants.HIDDING_SPEED
                self.is_hidden = False
                self.is_hit = False
                self.grave_index = random.randint(0, GraveConstants.GRAVE_NUM_MAX - 1)

        if self.is_hit:
            if self.animation_state != 4: self.is_hit_animation()
            else: self.up_to_down()
        else:
            if self.animation_state == 1: self.down_to_up()
            elif self.animation_state == 2: self.stay_unchanged_and_disappear()
            elif  self.animation_state == 3: self.up_to_down()            

    def down_to_up(self):
        self.sprite = self.zombie_img[math.floor((self.animation_index / ZombieConstants.ANIMATION_SPEED) * self.zombie_img.__len__())]
        self.animation_index += 1
        if self.animation_index >= ZombieConstants.ANIMATION_SPEED: 
            self.animation_index = ZombieConstants.ANIMATION_SPEED - 1
            self.animation_state = 2 # Stay unchanged and disappear

    def stay_unchanged_and_disappear(self):
        if self.showing_index > 0:
            self.showing_index -= 1
            self.sprite = self.zombie_img[self.zombie_img.__len__() - 1]
        else:
            self.showing_index = ZombieConstants.SHOWING_SPEED
            self.animation_state = 3 # Up to down

    def is_hit_animation(self):
        self.sprite = self.zombie_hit_img[math.floor((self.animation_index / ZombieConstants.ANIMATION_SPEED) * self.zombie_img.__len__())]
        if self.is_hit_index > 0:
            self.is_hit_index -= 1
        else:
            self.is_hit_index = ZombieConstants.IS_HIT_SPEED
            self.animation_state = 4 # Up to down

    def up_to_down(self):
        if self.is_hit:
            self.sprite = self.zombie_hit_img[math.floor((self.animation_index / ZombieConstants.ANIMATION_SPEED) * self.zombie_img.__len__())]
        else: self.sprite = self.zombie_img[math.floor((self.animation_index / ZombieConstants.ANIMATION_SPEED) * self.zombie_img.__len__())]
        self.animation_index -= 1
        
        if self.animation_index < 0: 
            self.animation_state = 1
            self.animation_index = 0
            self.is_hidden = True
            if not(self.is_hit): self.escape_count += 1
            else: self.is_hit = False

    def update_transform(self):
        transform = self.entity.get_component(TransformComponent)
        transform.dest = pg.Rect(GraveConstants.GRAVE_POS[self.grave_index][0],
                    GraveConstants.GRAVE_POS[self.grave_index][1] - self.sprite.get_height(),
                    self.sprite.get_width(), self.sprite.get_height())
        
class TransformComponent(Component):
    def __init__(self):
        self.src = pg.Rect(0, 0, 0, 0)
        self.dest = pg.Rect(0, 0, 0, 0)
    def draw(self):
        pass
    def update(self):
        pass
    def handle_event(self, event):
        pass

class ScoreComponent(Component):
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.level = 0
        self.lives = 3
        self.miss_sound = pg.mixer.Sound(SoundConstants.SOUND_MISS)
        self.levelUpSound = pg.mixer.Sound(SoundConstants.SOUND_LEVEL_UP)
        self.hit_sound = pg.mixer.Sound(SoundConstants.SOUND_HIT)
        self.font_obj = pg.font.Font(FontConstants.FONT_NAME,FontConstants.FONT_SIZE)
        try:
            with open('high_score.txt', 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            return 0
    def draw(self):
        if not(super().draw()): return
        hit_text = self.font_obj.render(TextConstants.HIT_TEXT + str(self.hits), True, TextConstants.TEXT_COLOR)
        hit_text_pos = hit_text.get_rect()
        hit_text_pos.centerx = TextConstants.HIT_POS
        hit_text_pos.centery = FontConstants.FONT_SIZE
        screen.blit(hit_text, hit_text_pos)

        # Render the player's misses
        miss_text = self.font_obj.render(TextConstants.MISS_TEXT + str(self.misses), True, TextConstants.TEXT_COLOR)
        miss_text_pos = miss_text.get_rect()
        miss_text_pos.centerx = TextConstants.MISS_POS
        miss_text_pos.centery = FontConstants.FONT_SIZE
        screen.blit(miss_text, miss_text_pos)

        # Render the player's level
        level_text = self.font_obj.render(TextConstants.LEVEL_TEXT + str(self.level), True, TextConstants.TEXT_COLOR)
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = TextConstants.LEVEL_POS
        level_text_pos.centery = FontConstants.FONT_SIZE
        screen.blit(level_text, level_text_pos)

        # Render high score
        current_high_score_text = TextConstants.HIGH_SCORE_TEXT + str(self.high_score)
        high_score_text = self.font_obj.render(current_high_score_text, True, TextConstants.TEXT_COLOR)
        high_score_text_pos = high_score_text.get_rect()
        high_score_text_pos.centerx = TextConstants.HIGH_SCORE_POS
        high_score_text_pos.centery = FontConstants.FONT_SIZE
        screen.blit(high_score_text, high_score_text_pos)
        
        # Render lives
        current_lives_text = TextConstants.LIVES_TEXT + str(self.lives)
        lives_text = self.font_obj.render(current_lives_text, True, TextConstants.TEXT_COLOR)
        lives_text_pos = lives_text.get_rect()
        lives_text_pos.centerx = SCREEN_WIDTH // 2
        lives_text_pos.centery = SCREEN_HEIGHT - FontConstants.FONT_SIZE
        screen.blit(lives_text, lives_text_pos)

    def update(self):
        # Update level
        nextLevel = math.floor(self.hits / LevelConstants.LEVEL_UP_GAP)
        if nextLevel != self.level:
            self.levelUpSound.play()
            self.level = nextLevel

    def handle_event(self, event):
        pass

class RestartButtonComponent(Component):
    def __init__(self):
        self.x, self.y = SCREEN_HEIGHT // 2 - 50, SCREEN_HEIGHT // 2 + 50
        self.font = pg.font.Font(FontConstants.FONT_NAME, FontConstants.FONT_SIZE)
        self.change_text("Restart", "black")
        self.feedback = ""
        self.restart = False
        self.enabled = False

        font = pg.font.Font(FontConstants.FONT_NAME, FontConstants.FONT_SIZE * 2)
        game_over_text = font.render("Game Over", True, TextConstants.TEXT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, True, pg.Color("White"))
        self.size = self.text.get_size()
        self.surface = pg.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        if self.enabled:
            screen.blit(self.surface, (self.x, self.y))
            font = pg.font.Font(FontConstants.FONT_NAME, FontConstants.FONT_SIZE * 2)
            game_over_text = font.render("Game Over", True, TextConstants.TEXT_COLOR)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(game_over_text, game_over_rect)
        if self.restart:
            print("Hello")
            Game.game_events['restart'] = True

    def update(self):
        event = Game.game_events[pg.MOUSEBUTTONDOWN]
        x, y = pg.mouse.get_pos()
        if event:
            if self.rect.collidepoint(x, y):
                self.restart = True
                return
        self.restart = False


#Systems
class System:
    def __init__(self):
        pass
    def process(self):
        pass
class CollisionSystem(System):
    def __init__(self):
        pass
    def process(self):
        event = Game.game_events[pg.MOUSEBUTTONDOWN]
        if event and event.button == 1:
            self.hammer_collide_zoombie()
    def hammer_collide_zoombie(self):
        score_component = self.entity_manager.get_entity('Score').get_component(ScoreComponent)
        hammer_component = self.entity_manager.get_entity('Hammer').get_component(HammerComponent)
        zombie_rect = self.entity_manager.get_entity('Zombie').get_component(TransformComponent).dest
        zombie_component = self.entity_manager.get_entity('Zombie').get_component(ZombieComponent)

        if not(zombie_component.is_hidden):
            hammer_pos = pg.mouse.get_pos()
            if zombie_rect.collidepoint(hammer_pos):
                score_component.hit_sound.play()
                zombie_component.is_hit = True
                score_component.hits += 1
            else:
                score_component.miss_sound.play()
        else:
            score_component.miss_sound.play()
            score_component.misses += 1
    
class UpdatePlayerScoreSystem(System):
    def __init__(self):
        pass

    def process(self):
        score_component = self.entity_manager.get_entity('Score').get_component(ScoreComponent)
        zombie_component = self.entity_manager.get_entity('Zombie').get_component(ZombieComponent)

        score_component.lives = 3 - zombie_component.escape_count

        if score_component.lives == 0:
            Game.game_events['resume'] = True
            self.show_game_over_screen()
        
        self.update_by_level(zombie_component, score_component)
    def show_game_over_screen(self):
        self.entity_manager.get_entity('Static').get_component(RestartButtonComponent).enabled = True
    
    def update_by_level(self,zombie_component, score_component):
        if score_component.level == 2: 
            Game.game_events[pg.QUIT] = True
            return
        zombie_component.showing_speed = ZombieConstants.HIDDING_SPEED * (1 - (score_component.level - 1) * 0.1)


# class RenderSystem:
#     def render_grave()

