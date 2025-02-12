
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class LevelConstants:
	LEVEL_UP_GAP = 2
	LEVEL_DELAY_TIME = 5

class ZombieConstants:
	ZOM_WIDTH = 106
	ZOM_HEIGHT = 130
	MAX_ZOMBIES = 3

	HIDDING_SPEED = 90
	SHOWING_SPEED = 90
	ANIMATION_SPEED = 10
	IS_HIT_SPEED = 10

	ZOM_SPRITE_1 = [179, 0, 117, 81]
	ZOM_SPRITE_2 = [313, 0, 117, 81]
	ZOM_SPRITE_3 = [449, 0, 117, 81]
	ZOM_SPRITE_4 = [585, 0, 117, 81]
	ZOM_SPRITE_5 = [717, 0, 117, 81]
	ZOM_SPRITE_6 = [864, 0, 117, 81]

class GraveConstants:
	GRAVE_NUM_MAX = 8
	GRAVE_POS = [(101, 230 ),
			  (345, 230 ),
			  (580, 230 ),
			  (230, 380 ),
			  (475, 380 ),
			  (101, 530 ),
			  (365, 530 ) , 
			  (590, 530 )]
class TextConstants:
	GAME_TITLE = "Whack A Zombie - Assignment 1"
	HIT_TEXT = "HITS - "
	MISS_TEXT = "MISSES - "
	LEVEL_TEXT = "LEVEL - "
	HIGH_SCORE_TEXT = "HIGH SCORE -"
	LIVES_TEXT = "LIVES -"

	HIT_POS = SCREEN_WIDTH / 4 * 0.4
	MISS_POS = SCREEN_WIDTH / 4 * 1.3
	LEVEL_POS = SCREEN_WIDTH / 4 * 2.2
	HIGH_SCORE_POS = SCREEN_WIDTH / 4 * 3.3

	LIVES_POS = SCREEN_HEIGHT/-1 * 1

	TEXT_COLOR = [255, 255, 255] # White
	
class ImageConstants:
	IMAGE = "./Resources/images/"
	IMAGE_BG = IMAGE + "background.png"
	IMAGE_HAMMER = IMAGE + "hammer.png"
	IMAGE_ZOMBIE = [IMAGE + "zombie_head_0.png",IMAGE + "zombie_head_1.png",IMAGE + "zombie_head_2.png",IMAGE + "zombie_head_3.png"]
	IMAGE_ZOMBIE_HIT = [IMAGE + "zombie_hit_0.png",IMAGE + "zombie_hit_1.png",IMAGE + "zombie_hit_2.png",IMAGE + "zombie_hit_3.png"]
	
class SoundConstants:
	SOUND = "./Resources/sounds/"
	SOUND_BG = SOUND + "music_bg.mp3"
	SOUND_HIT = SOUND + "hit.wav"
	SOUND_MISS = SOUND + "miss.wav"
	SOUND_LEVEL_UP = SOUND + "level_up.wav"

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

	HIT_POS = SCREEN_WIDTH / 4 * 0.4
	MISS_POS = SCREEN_WIDTH / 4 * 1.3
	LEVEL_POS = SCREEN_WIDTH / 4 * 2.2
	HIGH_SCORE_POS = SCREEN_WIDTH / 4 * 3.3

	LIVES_POS = SCREEN_HEIGHT/-1 * 1

	TEXT_COLOR = [255, 255, 255] # White