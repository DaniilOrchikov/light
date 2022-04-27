from numba import njit

from settings import *


@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int(a // TILE) * TILE, int(b // TILE) * TILE


@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, fov, its_lamp, world_map, door_map):
    rays = [(0.0, 0.0)]
    m_d = MAX_DEPTH
    if not its_lamp:
        m_d *= 2.4
        rays = [(float(player_pos[0]), float(player_pos[1]))]
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
        for i in range(0, WIDTH * 2, 8):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map or (int((x + dx) // 8), int(y) // 8) in door_map or \
                    math.sqrt((player_pos[0] - x - dx) ** 2 + (player_pos[1] - y) ** 2) > m_d:
                X, Y = x + dx, y
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT * 2, 8):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map or (int(x) // 8, int((y + dy) // 8)) in door_map or \
                    math.sqrt((player_pos[0] - x) ** 2 + (player_pos[1] - y - dy) ** 2) > m_d:
                if abs(Y - player_pos[1]) > abs(y + dy - player_pos[1]):
                    X, Y = x, y + dy
                break
            y += dy * TILE

        if X >= 0 and Y >= 0:
            if math.sqrt((player_pos[0] - X) ** 2 + (player_pos[1] - Y) ** 2) > m_d:
                X, Y = cos_a * m_d + player_pos[0], sin_a * m_d + player_pos[1]
            rays.append((X, Y))

        cur_angle += fov / NUM_RAYS
    return rays
