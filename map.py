from numba.core import types
from numba.typed import Dict
from numba import int64

from light_emitter import LightEmitter
from settings import *
from tile import Tile, Wall, Window, Tree

with open('map.txt', 'r') as txt_map:
    txt_map = txt_map.read().split('\n')

physics_world_map = []
world_map = set()
map_for_lighting = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
door_map = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
light_emitter_map = set()
foreground_world_map = set()
for j, row in enumerate(txt_map):
    physics_world_map.append([])
    for i, char in enumerate(row):
        if char == 'w':
            physics_world_map[-1].append(Wall(i * TILE, j * TILE))
            world_map.add(Wall(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
        elif char == 'o':
            world_map.add(Window(i * TILE, j * TILE))
            physics_world_map[-1].append(Window(i * TILE, j * TILE))
        elif char == 'l':
            light_emitter_map.add(LightEmitter(i * TILE, j * TILE))
            physics_world_map[-1].append(None)
        elif char == 't':
            foreground_world_map.add(Tree(i * TILE, j * TILE))
            map_for_lighting[(i * TILE, j * TILE)] = 1
            physics_world_map[-1].append(Tile(i * TILE, j * TILE))
            world_map.add(Tile(i * TILE, j * TILE))
        else:
            physics_world_map[-1].append(None)
