import sys
import time

from PIL import Image
from numba.core import types
from numba.typed import Dict
from numba import int64

from door import Door
from light_emitter import LightEmitter
from settings import *
from tile import *

physics_world_map = []
world_map = []
map_for_lighting = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
door_map = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
light_emitter_map = set()
foreground_world_map = set()
background_map_l1 = []
background_map_l2 = []
background_map_l3 = []
doors = []

im_map = Image.open('im_map.png')
width, height = im_map.size
pixels = im_map.load()
for j in range(height):
    physics_world_map.append([])
    world_map.append([])
    for i in range(width):
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        r, g, b, h = pixels[i, j]
        if (r, g, b) == (0, 0, 0):  # стена
            physics_world_map[-1].append(Wall(i * TILE, j * TILE))
            world_map[-1].append(Wall(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
        elif (r, g, b) == (0, 255, 0):  # дерево
            foreground_world_map.add(Tree(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
            physics_world_map[-1].append(Tile(i * TILE, j * TILE))
            world_map[-1].append(Stump(i * TILE, j * TILE))
        elif (r, g, b) == (0, 129, 0):  # ограничивающее дерево
            foreground_world_map.add(BoundingTree(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
            physics_world_map[-1].append(Tile(i * TILE, j * TILE))
            world_map[-1].append(Tile(i * TILE, j * TILE))
        elif (r, g, b) == (220, 220, 0):  # лампа
            light_emitter_map.add(LightEmitter(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
            background_map_l1.append(Floor(i * TILE, j * TILE))
        elif (r, g, b) == (212, 131, 212):  # окно
            world_map[-1].append(Window(i * TILE, j * TILE))
            physics_world_map[-1].append(Window(i * TILE, j * TILE))
        elif (r, g, b) == (255, 168, 255):  # имитация окна:
            physics_world_map[-1].append(Tile(i * TILE, j * TILE))
            world_map[-1].append(None)
        elif (r, g, b) == (193, 193, 193):  # пол
            background_map_l1.append(Floor(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(Floor(i * TILE, j * TILE))
        # двери
        elif (r, g, b) == (255, 0, 0):  # ^
            doors.append(Door(i * TILE + AVERAGE, (j + 1) * TILE, math.pi / 2 * 3))
            background_map_l1.append(Floor(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
        elif (r, g, b) == (255, 129, 129):  # >
            doors.append(Door(i * TILE, j * TILE + TILE // 2, 0))
            background_map_l1.append(Floor(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
        elif (r, g, b) == (178, 0, 0):  # V
            doors.append(Door(i * TILE + TILE // 2, j * TILE, math.pi / 2))
            background_map_l1.append(Floor(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
        elif (r, g, b) == (182, 97, 97):  # <
            doors.append(Door((i + 1) * TILE, j * TILE + TILE // 2 + 1, math.pi))
            background_map_l1.append(Floor(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
        else:
            background_map_l1.append(Dirt(i * TILE, j * TILE))
            if not randint(0, 10):
                background_map_l2.append(Mud(i * TILE, j * TILE))
            if not randint(0, 10):
                background_map_l3.append(Grass(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
            world_map[-1].append(None)
        if (r, g, b) == (28, 0, 255):
            player_pos = (i * TILE, j * TILE)
im_map.close()
