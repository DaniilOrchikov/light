from PIL import Image
from numba.core import types
from numba.typed import Dict
from numba import int64

from door import Door
from light_emitter import LightEmitter
from settings import *
from tile import Tile, Wall, Window, Tree

# with open('map.txt', 'r') as txt_map:
#     txt_map = txt_map.read().split('\n')
physics_world_map = []
world_map = set()
map_for_lighting = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
door_map = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
light_emitter_map = set()
foreground_world_map = set()
doors = []

im_map = Image.open('im_map.png')
width, height = im_map.size
pixels = im_map.load()
for j in range(height):
    physics_world_map.append([])
    for i in range(width):
        r, g, b, h = pixels[i, j]
        if (r, g, b) == (0, 0, 0):  # стена
            physics_world_map[-1].append(Wall(i * TILE, j * TILE))
            world_map.add(Wall(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
        elif (r, g, b) == (0, 255, 0):  # дерево
            foreground_world_map.add(Tree(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
            physics_world_map[-1].append(Tile(i * TILE, j * TILE))
            world_map.add(Tile(i * TILE, j * TILE))
        elif (r, g, b) == (220, 220, 0):  # лампа
            light_emitter_map.add(LightEmitter(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
        elif (r, g, b) == (212, 131, 212):  # окно
            world_map.add(Window(i * TILE, j * TILE))
            physics_world_map[-1].append(Window(i * TILE, j * TILE))
        elif (r, g, b) == (255, 0, 0):  # ^
            if pixels[i - 1, j + 1] == (0, 0, 0, 255):
                doors.append(Door(i * TILE - 1, (j + 1) * TILE, math.pi / 2 * 3))
            else:
                doors.append(Door(i * TILE + TILE // 2 - 1, (j + 1) * TILE, math.pi / 2 * 3))
            physics_world_map[-1].append(None)
        elif (r, g, b) == (255, 129, 129):  # >
            if pixels[i - 1, j - 1] == (0, 0, 0, 255):
                doors.append(Door(i * TILE, j * TILE, 0))
            else:
                doors.append(Door(i * TILE, j * TILE + TILE // 2, 0))
            physics_world_map[-1].append(None)
        elif (r, g, b) == (178, 0, 0):  # V
            if pixels[i - 1, j - 1] == (0, 0, 0, 255):
                doors.append(Door(i * TILE - 1, j * TILE, math.pi / 2))
            else:
                doors.append(Door(i * TILE + TILE // 2 - 1, j * TILE, math.pi / 2))
            physics_world_map[-1].append(None)
        elif (r, g, b) == (182, 97, 97):  # <
            if pixels[i + 1, j - 1] == (0, 0, 0, 255):
                doors.append(Door((i + 1) * TILE, j * TILE, math.pi))
            else:
                doors.append(Door((i + 1) * TILE, j * TILE + TILE // 2 + 1, math.pi))
            physics_world_map[-1].append(None)
        else:
            physics_world_map[-1].append(None)
im_map.close()

# for i, row in enumerate(txt_map):
#     physics_world_map.append([])
#     for j, char in enumerate(row):
#         if char == 'w':
#             physics_world_map[-1].append(Wall(i * TILE, j * TILE))
#             world_map.add(Wall(i * TILE, j * TILE))
#             map_for_lighting[(i * TILE, j * TILE)] = 1
#         elif char == 'o':
#             world_map.add(Window(i * TILE, j * TILE))
#             physics_world_map[-1].append(Window(i * TILE, j * TILE))
#         elif char == 'l':
#             light_emitter_map.add(LightEmitter(i * TILE, j * TILE))
#             physics_world_map[-1].append(None)
#         elif char == 't':
#             foreground_world_map.add(Tree(i * TILE, j * TILE))
#             map_for_lighting[(i * TILE, j * TILE)] = 1
#             physics_world_map[-1].append(Tile(i * TILE, j * TILE))
#             world_map.add(Tile(i * TILE, j * TILE))
#         else:
#             physics_world_map[-1].append(None)
