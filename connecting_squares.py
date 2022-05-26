import mahotas

from settings import *


def checking_neighbors(arr, y, x):
    v = 0
    for i in (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1):
        if not arr[y + i[0], x + i[1]]:
            v += 1
    return v


def connecting_squares(arr):
    points = []
    h, w = len(arr), len(arr[0])
    for y0 in range(h):
        for x0 in range(w):
            polygon = []
            if arr[y0, x0] == 1:
                polygon.append([x0, y0])
                arr[y0, x0] = -1
                x, y = x0 + 1, y0
                previous_direction = 'right'
                while x != x0 or y != y0 + 1:
                    arr[y, x] = -1
                    if arr[y, x - 1] == 1 and checking_neighbors(arr, y, x - 1) > 0:
                        direction = 'left'
                        if previous_direction != direction:
                            previous_direction = direction
                            polygon.append([x, y])
                        x -= 1
                        continue
                    elif arr[y - 1, x] == 1 and checking_neighbors(arr, y - 1, x) > 0:
                        direction = 'up'
                        if previous_direction != direction:
                            previous_direction = direction
                            polygon.append([x, y])
                        y -= 1
                        continue
                    elif arr[y, x + 1] == 1 and checking_neighbors(arr, y, x + 1) > 0:
                        direction = 'right'
                        if previous_direction != direction:
                            previous_direction = direction
                            polygon.append([x, y])
                        x += 1
                        continue
                    elif arr[y + 1, x] == 1 and checking_neighbors(arr, y + 1, x) > 0:
                        direction = 'down'
                        if previous_direction != direction:
                            previous_direction = direction
                            polygon.append([x, y])
                        y += 1
                        continue
                polygon.append([x0, y0 + 1])
                arr[y0 + 1, x0] = -1
                mahotas.polygon.fill_polygon([(i[1], i[0]) for i in polygon], arr, -1)
                polygon = [[i[0] * TILE, i[1] * TILE] for i in polygon]
                points.append(polygon)
    print(*points, sep='\n')
    return points
