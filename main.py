import sys

import pygame
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)

from physics import Physics
from player import Player
from map import world_map
from manager import Manager

clock = pygame.time.Clock()
physics = Physics(world_map)
player = Player(physics)
drawing = Manager(screen, player)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.movement()
    screen.fill((80, 80, 255))

    drawing.paint()
    drawing.fps(clock)

    pygame.display.flip()
    clock.tick()