import pygame.transform

from map import world_map


def create_level(screen):
    for y in range(len(world_map)):
        for x in range(len(world_map[0])):
            if world_map[y][x] is not None:
                tile = world_map[y][x]
                if tile.type == 'wall' or tile.type == 'stump':
                    tile.paint(screen)
                elif tile.type == 'window':
                    if world_map[y - 1][x] is not None and world_map[y - 1][x].type == 'wall':
                        tile.im = pygame.transform.rotate(tile.im, 180)
                        tile.paint(screen)
                    else:
                        if world_map[y - 1][x] is not None and world_map[y - 1][x].type == 'floor':
                            tile.im = pygame.transform.rotate(tile.im, -90)
                        else:
                            tile.im = pygame.transform.rotate(tile.im, 90)
                        tile.paint(screen)
