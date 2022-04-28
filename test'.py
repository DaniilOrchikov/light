def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

import sys

from settings import *

from numba import njit


# @njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, world_map):
    ox, oy = player_pos
    rays = [(ox, oy)]
    cur_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001
        X, Y = -10, -10

        x, y = cos_a * MAX_DEPTH, sin_a * MAX_DEPTH
        for i in world_map:
            pos = line_intersection(((ox, oy), (x, y)), i)
            if pos:
                X, Y = min((X, Y), pos, key=lambda a: math.sqrt((ox - a[0]) ** 2 + (oy - a[1]) ** 2))
        if X < 0:
            X = x + ox
            Y = y + oy

        if X >= 0 and Y >= 0:
            rays.append((X, Y))

        cur_angle += FOV / NUM_RAYS
    return rays


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF)

clock = pygame.time.Clock()
angle = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((80, 80, 255))
    line = ((300, 500), (200, 200))
    line1 = ((300, 100), (200, 200))
    lines = [line, line1]
    rays = ray_casting((100, 300), angle, lines)
    pygame.draw.polygon(screen, (234, 224, 191, 100), rays)
    pygame.draw.rect(screen, 'red', (95, 295, 10, 10))
    for line in lines:
        pygame.draw.line(screen, 'red', line[0], line[1])

    pygame.display.flip()
    clock.tick()
