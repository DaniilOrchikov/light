import time
from random import randint

from numba import njit

from settings import *


@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int(a // TILE) * TILE, int(b // TILE) * TILE


@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, world_map, scroll, fov, its_lamp, time):
    rays = [(0.0, 0.0)]
    if not its_lamp:
        rays = [(player_pos[0] - scroll[0], player_pos[1] - scroll[1])]
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - fov / 2
    m_d = MAX_DEPTH + math.sin(time)
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001
        X, Y = -10, -10

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH * 2, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map or (
                    math.sqrt((player_pos[0] - x - dx) ** 2 + (player_pos[1] - y) ** 2) > m_d and its_lamp):
                X = x + dx
                Y = y
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT * 2, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a

            if mapping(x, y + dy) in world_map or (
                    math.sqrt((player_pos[0] - x) ** 2 + (player_pos[1] - y - dy) ** 2) > m_d and its_lamp):
                if abs(Y - player_pos[1]) > abs(y + dy - player_pos[1]):
                    Y = y + dy
                    X = x
                break
            y += dy * TILE

        if X >= 0 and Y >= 0:
            if its_lamp:
                if math.sqrt((player_pos[0] - X) ** 2 + (player_pos[1] - Y) ** 2) > m_d:
                    X, Y = cos_a * m_d + player_pos[0], sin_a * m_d + player_pos[1]
            rays.append((X - scroll[0], Y - scroll[1]))

        cur_angle += fov / NUM_RAYS
    return rays
