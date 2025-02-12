class GameConstants:
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	FPS = 60

class LevelConstants:
	LEVEL_UP_GAP = 5
	LEVEL_DELAY_TIME = 5

class ZombieConstants:
	ZOM_WIDTH = 98
	ZOM_HEIGHT = 81
	MAX_ZOMBIES = 3

	ZOM_SPRITE_1 = [179, 0, 117, 81]
	ZOM_SPRITE_2 = [313, 0, 117, 81]
	ZOM_SPRITE_3 = [449, 0, 117, 81]
	ZOM_SPRITE_4 = [585, 0, 117, 81]
	ZOM_SPRITE_5 = [717, 0, 117, 81]
	ZOM_SPRITE_6 = [864, 0, 117, 81]

class GraveConstants:
	GRAVE_NUM_MAX = 8
	GRAVE_POS_1 = [101, 230 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_2 = [345, 230 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_3 = [580, 230 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_4 = [230, 380 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_5 = [475, 380 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_6 = [101, 530 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_7 = [365, 530 - ZombieConstants.ZOM_HEIGHT]
	GRAVE_POS_8 = [590, 530 - ZombieConstants.ZOM_HEIGHT]

class HammerConstants:
	HAMMER_ANGLE = 45
	HAMMER_DISTANCE_X = 16
	HAMMER_DISTANCE_Y = 25

class TimeConstants:
	SPAWN_ANI_TIME = 0.1
	DEAD_ANI_TIME = 0.1

	RESPAWN_TIME = 1.5
	RESPAWN_DELTA_TIME = 0.15

	HAMMER_ANI_TIME = 0.8

class AnimationConstants:	
	SPAWN_ANI_INDEX_MAX = 2
	DEAD_ANI_INDEX_MAX = 4

class FontConstants:
	FONT_NAME = "./Resources/fonts/ZOMBIE.ttf"
	FONT_SIZE = 36
	FONT_SIZE_OVER = 108

class TextConstants:
	GAME_TITLE = "Whack A Zombie - Assignment 1"
	HIT_TEXT = "HITS - "
	MISS_TEXT = "MISSES - "
	LEVEL_TEXT = "LEVEL - "
	HIGH_SCORE_TEXT = "HIGH SCORE -"
	LIVES_TEXT = "LIVES -"

	HIT_POS = GameConstants.SCREEN_WIDTH / 4 * 0.4
	MISS_POS = GameConstants.SCREEN_WIDTH / 4 * 1.3
	LEVEL_POS = GameConstants.SCREEN_WIDTH / 4 * 2.2
	HIGH_SCORE_POS = GameConstants.SCREEN_WIDTH / 4 * 3.3

	LIVES_POS = GameConstants.SCREEN_HEIGHT/-1 * 1

	TEXT_COLOR = [255, 255, 255] # White

class ImageConstants:
	IMAGE = "./Resources/images/"
	IMAGE_BG = IMAGE + "background.png"
	IMAGE_HAMMER = IMAGE + "hammer.png"
	IMAGE_ZOMBIE = IMAGE + "zombie.png"

class SoundConstants:
	SOUND = "./Resources/sounds/"
	SOUND_BG = SOUND + "music_bg.mp3"
	SOUND_HIT = SOUND + "hit.wav"
	SOUND_MISS = SOUND + "miss.wav"
	SOUND_LEVEL_UP = SOUND + "level_up.wav"

class Constants(GameConstants, LevelConstants, ZombieConstants, GraveConstants, HammerConstants, 
	TimeConstants, AnimationConstants, FontConstants, TextConstants, ImageConstants, SoundConstants):
	LEFT_MOUSE_BUTTON = 1

class Zombie:
	def __init__(self):
		self.index = -1
		self.zombieStatus = -1
		self.animationIndex = 0
		self.stayTime = 0
		self.pic = None
	def __init__(self, index, pic):
		self.index = index					# Equal to position of its grave
		self.zombieStatus = 0
		self.animationIndex = 0
		self.stayTime = 0					# Existing time of its frame
		self.pic = pic