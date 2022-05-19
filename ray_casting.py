from numba import njit

from settings import *


@njit(fastmath=True, cache=True)
def mapping(a, b, average):
    return int(a // average) * average, int(b // average) * average


@njit(fastmath=True, cache=True)
def calculating_lightning(pos, angle, fov, its_lamp, world_map, door_map, player_pos_y):
    rays = []
    arr = ray_casting(pos, angle, fov, its_lamp, world_map, door_map)
    rays.append(arr[0])
    shift = 35
    for i in range(1, len(arr) - 1):
        if not (arr[i - 1][0] == arr[i + 1][0] == arr[i][0] or arr[i - 1][1] == arr[i + 1][1] == arr[i][1]) and \
                player_pos_y + HALF_HEIGHT + shift > arr[i][1] > player_pos_y - HALF_HEIGHT - shift:
            rays.append(arr[i])
        elif not (arr[i - 1][1] >= player_pos_y + HALF_HEIGHT + shift and arr[i][1] >= player_pos_y + HALF_HEIGHT + shift and
                  arr[i + 1][1] >= player_pos_y + HALF_HEIGHT + shift) and not (
                arr[i - 1][1] <= player_pos_y - HALF_HEIGHT - shift and arr[i][1] <= player_pos_y - HALF_HEIGHT - shift and
                arr[i + 1][1] <= player_pos_y - HALF_HEIGHT - shift):
            rays.append(arr[i])
    rays.append(arr[-1])
    return rays


@njit(fastmath=True, cache=True)
def ray_casting(pos, angle, fov, its_lamp, world_map, door_map):
    rays = [(0.0, 0.0)]
    m_d = MAX_DEPTH
    if not its_lamp:
        m_d = MAX_DEPTH * 1.7
        rays = [(float(pos[0]), float(pos[1]))]
    ox, oy = pos
    xm, ym = mapping(ox, oy, TILE)
    cur_angle = angle - fov / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001
        X, Y = -10, -10

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH * 2, AVERAGE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y, TILE) in world_map or mapping(x + dx, y, AVERAGE) in door_map or \
                    math.sqrt((pos[0] - x - dx) ** 2 + (pos[1] - y) ** 2) > m_d:
                X, Y = x + dx, y
                break
            x += dx * AVERAGE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT * 2, AVERAGE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy, TILE) in world_map or mapping(x, y + dy, AVERAGE) in door_map or \
                    math.sqrt((pos[0] - x) ** 2 + (pos[1] - y - dy) ** 2) > m_d:
                if math.sqrt((pos[0] - X) ** 2 + (pos[1] - Y) ** 2) >= math.sqrt(
                        (pos[0] - x) ** 2 + (pos[1] - y - dy) ** 2):
                    X, Y = x, y + dy
                break
            y += dy * AVERAGE

        if X >= 0 and Y >= 0:
            if math.sqrt((pos[0] - X) ** 2 + (pos[1] - Y) ** 2) > m_d:
                X, Y = cos_a * m_d + pos[0], sin_a * m_d + pos[1]
            rays.append((X, Y))

        cur_angle += fov / NUM_RAYS
    return rays
