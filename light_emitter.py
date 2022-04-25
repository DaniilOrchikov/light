import pygame

from ray_casting import ray_casting
from settings import *


class LightEmitter:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.image.load('data/lamp.png').convert_alpha()
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))

    def paint(self, sc, screen, scroll, map_for_lighting):
        rays = ray_casting((self.x + TILE // 2, self.y + TILE // 2),
                           0, map_for_lighting, scroll, math.pi * 2, False)[1:]
        try:
            pygame.draw.polygon(sc, (0, 0, 0), rays)
        except ValueError:
            pass

        screen.blit(self.im, (self.x - scroll[0], self.y - scroll[1]))
