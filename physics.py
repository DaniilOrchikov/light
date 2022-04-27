import numpy as np

from settings import *


def door_collision(player_rect, door_rect):
    player_lines = [(player_rect[0], player_rect[1], player_rect[0] + player_rect[2], player_rect[1]),
                    (player_rect[0] + player_rect[2], player_rect[1], player_rect[0] + player_rect[2],
                     player_rect[1] + player_rect[3]),
                    (player_rect[0] + player_rect[2], player_rect[1] + player_rect[3], player_rect[0],
                     player_rect[1] + player_rect[3]),
                    (player_rect[0], player_rect[1] + player_rect[3], player_rect[0], player_rect[1])]
    door_lines = [door_rect]
    for i in player_lines:
        for j in door_lines:
            xmax1, xmin1, xmax2, xmin2, ymax1, ymin1, ymax2, ymin2 = \
                max(i[0], i[2]), min(i[0], i[2]), max(j[0], j[2]), min(j[0], j[2]), \
                max(i[1], i[3]), min(i[1], i[3]), max(j[1], j[3]), min(j[1], j[3])
            if xmax1 >= xmin2 and xmax2 >= xmin1 and ymax1 >= ymin2 and ymax2 >= ymin1:
                p1p3, p1p2, p1p4, p3p1, p3p4, p3p2 = (j[0] - i[0], j[1] - i[1]), (i[2] - i[0], i[3] - i[1]), \
                                                     (j[2] - i[0], j[3] - i[1]), (i[0] - j[0], i[1] - j[1]), \
                                                     (j[2] - j[0], j[3] - j[1]), (i[2] - j[0], i[3] - j[1])
                if (p1p3[0] * p1p2[1] - p1p2[0] * p1p3[1]) * (p1p4[0] * p1p2[1] - p1p4[1] * p1p2[0]) <= 0 and \
                        (p3p1[0] * p3p4[1] - p3p4[0] * p3p1[1]) * (p3p2[0] * p3p4[1] - p3p2[1] * p3p4[0]) <= 0:
                    return i
    return False


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

    def movement(self, rect, move, door_rect):
        collisions = {'right': False, 'left': False, 'top': False, 'bottom': False, 'door': False}
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

        door_col = door_collision((rect[0], rect[1], rect[2], rect[3]), door_rect)
        if door_col:
            if door_col[0] == rect[0] and door_col[1] == rect[1]:
                collisions['door'] = 'top'
            elif door_col[0] == rect[0] + rect[2] and door_col[1] == rect[1]:
                collisions['door'] = 'right'
            elif door_col[0] == rect[0] + rect[2] and door_rect[1] == rect[1] + rect[3]:
                collisions['door'] = 'bottom'
            else:
                collisions['door'] = 'left'
        return collisions
