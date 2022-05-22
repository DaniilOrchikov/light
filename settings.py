import math
import pygame
from random import randint

# game settings
WIDTH = 990 * 1200 // 1200
HEIGHT = 558 * 1200 // 1200
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 18
FPS_POS = (WIDTH - 65, 5)

# ray casting settings
FOV = math.pi / 2
HALF_FOV = FOV / 2
NUM_RAYS = 130
MAX_DEPTH = 300
RENDERING_RANGE = [MAX_DEPTH * 3, MAX_DEPTH * 2.1]

# player settings
player_angle = 0
player_speed = 2
player_shift_speed = 4

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)

# door
AVERAGE = TILE // 2
DOOR_PUSHING_ANGLE = 0.1
DOOR_PUSHING_ANGLE_SHIFT = 0.2
