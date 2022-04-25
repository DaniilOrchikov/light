import pygame
from settings import *


class Tile:
    def __init__(self, x, y, color=(30, 70, 50)):
        self.x, self.y = x, y
        self.im = pygame.Surface((TILE, TILE))
        self.im.fill(color)
        self.rect = pygame.Rect(self.x, self.y, TILE, TILE)

    def paint(self, sc, scroll):
        sc.blit(self.im, (self.x - scroll[0], self.y - scroll[1]))
