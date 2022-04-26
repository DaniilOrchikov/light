import pygame

from ray_casting import ray_casting
from settings import *


class LightEmitter:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.image.load('data/lamp.png').convert_alpha()
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))

    def paint_light(self, sc, map_for_lighting, intensity):
        rays = ray_casting((self.x + TILE // 2, self.y + TILE // 2),
                           0, map_for_lighting, [0.0, 0.0], math.pi * 2, True)[1:]
        try:
            pygame.draw.polygon(sc, intensity, rays)
        except ValueError:
            pass

    def paint(self, screen):

        screen.blit(self.im, (self.x, self.y))
