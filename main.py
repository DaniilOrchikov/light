import sys
import pygame

from cursor import Cursor
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF)

from physics import Physics
from player import Player
from map import physics_world_map
from manager import Manager

clock = pygame.time.Clock()
physics = Physics(physics_world_map)
player = Player(physics)
drawing = Manager(screen, player)
pygame.mouse.set_visible(False)
cursor = Cursor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.movement(screen)
    screen.fill((80, 80, 255))

    drawing.paint()
    drawing.fps(clock)

    cursor.paint(*pygame.mouse.get_pos(), screen)

    pygame.display.flip()
    clock.tick()
