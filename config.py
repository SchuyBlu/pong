import pygame
import os

# Initialize pygame fonts.
pygame.font.init()

# Initialze sound.
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
PLAYER_W = 5
PLAYER_H = 80
FPS = 60
UPPER_LIMIT = 75
BALL_VEL_DEFAULT = 4
BALL_VEL_X = 4
BALL_VEL_Y = 4
MOVEMENT = 5

# Create fonts.
NAME_FONT = pygame.font.Font(os.path.join("fonts", "PressStart2P.ttf"), 50)
SCORE_FONT = pygame.font.Font(os.path.join("fonts", "PressStart2P.ttf"), 30)
WINNER_FONT = pygame.font.Font(os.path.join("fonts", "PressStart2P.ttf"), 40)

# Create user events.
P1_POINT = pygame.USEREVENT + 1
P2_POINT = pygame.USEREVENT + 2

# Finally, create the sound effect constants.
PLAY_LEFT_BLIP = True
PLAY_RIGHT_BLIP = True
PLAY_SCORED = True
BLIP1 = pygame.mixer.Sound(os.path.join("sound_effects", "blip1.mp3"))
BLIP2 = pygame.mixer.Sound(os.path.join("sound_effects", "blip2.mp3"))
BLIP3 = pygame.mixer.Sound(os.path.join("sound_effects", "blip3.mp3"))
BLIP4 = pygame.mixer.Sound(os.path.join("sound_effects", "blip4.mp3"))
SCORED = pygame.mixer.Sound(os.path.join("sound_effects", "scored.mp3"))
WINNER = pygame.mixer.Sound(os.path.join("sound_effects", "winner.mp3"))