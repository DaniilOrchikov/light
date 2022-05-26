import random
from os import listdir
from random import randrange

import pygame

from settings import *


class Tile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.Surface((TILE, TILE))
        self.rect = pygame.Rect(self.x, self.y, TILE, TILE)
        self.type = 'tile'

    def paint(self, sc):
        sc.blit(self.im, (self.x, self.y))


class Floor(Tile):
    frames = []
    sheet = pygame.image.load('data/floor/floor.png').convert()
    columns = sheet.get_width() // TILE
    rect = pygame.Rect(0, 0, TILE, TILE)
    for i in range(columns):
        frame_location = (TILE * i, 0)
        frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))

    def __init__(self, x, y):
        super(Floor, self).__init__(x, y)
        self.im = Floor.frames[randrange(len(Floor.frames))]
        self.type = 'floor'


class Grass(Tile):
    images = [pygame.image.load(f'data/grass/{i + 1}.png').convert_alpha() for i in range(len(listdir("data/grass")))]

    def __init__(self, x, y):
        super(Grass, self).__init__(x, y)
        self.im = Grass.images[randrange(len(Grass.images))]
        self.type = 'grass'


class Dirt(Tile):
    frames = []
    sheet = pygame.image.load('data/dirt/dirt.png').convert()
    columns = sheet.get_width() // TILE
    rect = pygame.Rect(0, 0, TILE, TILE)
    for i in range(columns):
        frame_location = (TILE * i, 0)
        frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))

    def __init__(self, x, y):
        super(Dirt, self).__init__(x, y)
        self.im = Dirt.frames[randrange(len(Dirt.frames))]
        self.type = 'dirt'


class Mud(Tile):
    images = [pygame.image.load(f'data/mud/{i + 1}.png').convert_alpha() for i in range(len(listdir("data/mud")))]

    def __init__(self, x, y):
        super(Mud, self).__init__(x, y)
        self.im = Mud.images[randrange(len(Mud.images))]
        self.type = 'mud'


class Wall(Tile):
    image = pygame.image.load('data/tiles/wall.png').convert_alpha()

    def __init__(self, x, y):
        super(Wall, self).__init__(x, y)
        self.im = Wall.image
        self.type = 'wall'


class Window(Tile):
    image = pygame.image.load('data/tiles/window.png').convert_alpha()

    def __init__(self, x, y):
        super(Window, self).__init__(x, y)
        self.im = Window.image
        self.type = 'window'


class Tree(Tile):
    im = [pygame.image.load('data/tree/' + i) for i in listdir('data/tree')]

    def __init__(self, x, y):
        super(Tree, self).__init__(x, y)
        self.im = Tree.im[randrange(len(Tree.im))].convert_alpha()
        self.im = pygame.transform.flip(pygame.transform.rotate(self.im, randrange(0, 360, 10)), bool(randint(0, 1)),
                                        bool(randint(0, 1)))
        self.margins = [self.im.get_width() // 2 - TILE // 2, self.im.get_height() // 2 - TILE // 2]
        self.type = 'tree'

    def paint(self, sc):
        sc.blit(self.im, (self.x - self.margins[0], self.y - self.margins[1]))


class Stump(Tile):
    images = [pygame.image.load('data/stump/' + i).convert_alpha() for i in listdir('data/stump')]

    def __init__(self, x, y):
        super(Stump, self).__init__(x, y)
        self.im = Stump.images[randrange(len(Stump.images))]
        self.im = pygame.transform.flip(pygame.transform.rotate(self.im, randrange(0, 360, 10)), bool(randint(0, 1)),
                                        bool(randint(0, 1)))
        self.type = 'stump'

    def paint(self, sc):
        sc.blit(self.im,
                (self.x - self.im.get_width() // 2 + TILE // 2, self.y - self.im.get_height() // 2 + TILE // 2))


class BoundingTree(Tree):
    def __init__(self, x, y):
        super(BoundingTree, self).__init__(x, y)
        self.type = 'bounding_tree'
