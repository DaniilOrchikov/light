from os import listdir
from random import randrange, randint

from settings import *


class Tile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.Surface((TILE, TILE))
        self.rect = pygame.Rect(self.x, self.y, TILE, TILE)

    def paint(self, sc):
        sc.blit(self.im, (self.x, self.y))


class Wall(Tile):
    def __init__(self, x, y):
        super(Wall, self).__init__(x, y)
        self.im = pygame.image.load('data/tiles/wall.png').convert_alpha()


class Window(Tile):
    def __init__(self, x, y):
        super(Window, self).__init__(x, y)
        self.im = pygame.image.load('data/tiles/window.png').convert_alpha()


class Tree(Tile):
    im = [pygame.image.load('data/tree/' + i) for i in listdir('data/tree')]

    def __init__(self, x, y):
        super(Tree, self).__init__(x, y)
        self.im = Tree.im[randrange(len(Tree.im))].convert_alpha()
        self.im = pygame.transform.flip(pygame.transform.rotate(self.im, randrange(0, 360, 10)), bool(randint(0, 1)), bool(randint(0, 1)))
        self.margins = [self.im.get_width() // 2 - TILE // 2, self.im.get_height() // 2 - TILE // 2]

    def paint(self, sc):
        sc.blit(self.im, (self.x - self.margins[0], self.y - self.margins[1]))
