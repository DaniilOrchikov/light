from light_emitter import LightEmitter
from settings import *
from tile import Tile, Wall, Window, Tree

with open('map.txt', 'r') as txt_map:
    txt_map = txt_map.read().split('\n')

world_map = set()
map_for_lighting = set()
light_emitter_map = set()
foreground_world_map = set()
for j, row in enumerate(txt_map):
    for i, char in enumerate(row):
        if char == 'w':
            world_map.add(Wall(i * TILE, j * TILE))
            map_for_lighting.add((i * TILE, j * TILE))
        elif char == 'o':
            world_map.add(Window(i * TILE, j * TILE))
        elif char == 'l':
            light_emitter_map.add(LightEmitter(i * TILE, j * TILE))
        elif char == 't':
            foreground_world_map.add(Tree(i * TILE, j * TILE))
            map_for_lighting.add((i * TILE, j * TILE))
            world_map.add(Tile(i * TILE, j * TILE))