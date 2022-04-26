import numpy as np
import pygame.draw

from settings import *


def roll(a, b, dx=1, dy=1):
    shape = a.shape[:-2] + ((a.shape[-2] - b.shape[-2]) // dy + 1,) + ((a.shape[-1] - b.shape[-1]) // dx + 1,) + b.shape
    strides = a.strides[:-2] + (a.strides[-2] * dy,) + (a.strides[-1] * dx,) + a.strides[-2:]
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


class Physics:
    def __init__(self, map):
        map = np.array([np.array(i, dtype=object) for i in map])
        self.map = roll(np.array(map, dtype=object), np.array([[0 for _ in range(4)] for _ in range(4)]))

    def collision_test(self, rect):
        for i in self.map[rect.y // TILE - 1, rect.x // TILE - 1]:
            for tile in i:
                if tile is not None:
                    if tile.rect.colliderect(rect):
                        return tile
        return None

    def movement(self, rect, move):
        collisions = {'right': False, 'left': False, 'top': False, 'bottom': False}
        if move[0] != 0:
            rect.x += move[0]
            collision_tile = self.collision_test(rect)
            if collision_tile:
                if move[0] > 0:
                    collisions['right'] = True
                    rect.right = collision_tile.rect.left
                else:
                    collisions['left'] = True
                    rect.left = collision_tile.rect.right
        if move[1] != 0:
            rect.y += move[1]
            collision_tile = self.collision_test(rect)
            if collision_tile:
                if move[1] > 0:
                    collisions['bottom'] = True
                    rect.bottom = collision_tile.rect.top
                else:
                    collisions['top'] = True
                    rect.top = collision_tile.rect.bottom
        return collisions
