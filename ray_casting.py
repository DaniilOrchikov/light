from numba import njit

from settings import *


@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int(a // TILE) * TILE, int(b // TILE) * TILE


@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, world_map, scroll, fov, leave_the_initial_pos):
    rays = [(0.0, 0.0)]
    if leave_the_initial_pos:
        rays = [(player_pos[0] - scroll[0], player_pos[1] - scroll[1])]
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - fov / 2
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
            if mapping(x + dx, y) in world_map:
                X = x + dx
                Y = y
                break
            x += dx * TILE
        # if X < 0:
        #     X = x + dx
        #     Y = y

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT * 2, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a

            if mapping(x, y + dy) in world_map:
                if abs(Y - player_pos[1]) > abs(y + dy - player_pos[1]):
                    Y = y + dy
                    X = x
                break
            y += dy * TILE

        # if Y < 0:
        #     X = x
        #     Y = y + dy

        if X >= 0 and Y >= 0:
            rays.append((X - scroll[0], Y - scroll[1]))

        cur_angle += fov / NUM_RAYS
    return rays
