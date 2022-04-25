import pygame
from pygame import gfxdraw

from ray_casting import ray_casting
from settings import *


class LightEmitter:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.Surface((TILE, TILE))
        self.im.fill((100, 50, 200))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))

    def paint(self, sc, scroll, map_for_lighting):
        rays = ray_casting((self.x + TILE // 2, self.y + TILE // 2),
                           0, map_for_lighting, scroll, math.pi * 2, False)[1:]
        try:
            pygame.draw.polygon(sc, (0, 0, 0), rays)
            # gfxdraw.aapolygon(sc, rays, (0, 0, 0))
        except ValueError:
            pass
        # sc.blit(self.im, (self.x - scroll[0], self.y - scroll[1]))
        # sc.blit(self.sc_light, (0, 0))
