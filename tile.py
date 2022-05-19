import random
from os import listdir
from random import randrange

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
    def __init__(self, x, y):
        super(Grass, self).__init__(x, y)
        self.im = pygame.image.load(f'data/grass/{random.randint(1, len(listdir("data/grass")))}.png').convert_alpha()
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


class Wall(Tile):
    def __init__(self, x, y):
        super(Wall, self).__init__(x, y)
        self.im = pygame.image.load('data/tiles/wall.png').convert_alpha()
        self.type = 'wall'


class Window(Tile):
    def __init__(self, x, y):
        super(Window, self).__init__(x, y)
        self.im = pygame.image.load('data/tiles/window.png').convert_alpha()
        self.type = 'window'


class Tree(Tile):
    im = [pygame.image.load('data/tree/' + i) for i in listdir('data/tree')]

    def __init__(self, x, y):
        super(Tree, self).__init__(x, y)
        self.im = Tree.im[randrange(len(Tree.im))].convert_alpha()
        self.im = pygame.transform.flip(pygame.transform.rotate(self.im, randrange(0, 360, 10)), bool(randint(0, 1)),
                                        bool(randint(0, 1)))
        self.margins = [self.im.get_width() // 2 - TILE // 2, self.im.get_height() // 2 - TILE // 2]

    def paint(self, sc):
        sc.blit(self.im, (self.x - self.margins[0], self.y - self.margins[1]))
