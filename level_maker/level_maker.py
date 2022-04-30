import sys

import numpy as np
import pygame
from settings import *


class LevelMaker:
    def __init__(self, width, height, cell_size, map=None):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.tile_size = 18
        self.left = self.cell_size * 15
        self.top = self.cell_size * 2
        self.indent = self.cell_size // 3
        self.brush = 'w'
        if map is None:
            self.board = [['.' for _ in range(self.width)] for _ in range(self.height)]
        else:
            self.board = map
        self.im_board = {'.': pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA),
                         'w': pygame.image.load('../data/tiles/wall.png').convert_alpha(),
                         'l': pygame.image.load('../data/tiles/lamp.png').convert_alpha(),
                         'o': pygame.image.load('../data/tiles/window.png').convert_alpha()}
        self.im_board1 = [[pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA),
                           pygame.image.load('../data/tiles/wall.png').convert_alpha(),
                           pygame.image.load('../data/tiles/lamp.png').convert_alpha(),
                           pygame.image.load('../data/tiles/window.png').convert_alpha()]]
        self.tile_board = [['.', 'w', 'l', 'o', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]

    def paint(self, screen):
        pygame.draw.rect(screen, '#523a65', (0, 0, self.left - self.cell_size, HEIGHT))
        pygame.draw.rect(screen, '#6d6473', (self.left - self.cell_size, 0, WIDTH, HEIGHT))
        for y in range(self.width):
            for x in range(self.height):
                pygame.draw.rect(screen, 'red',
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
                if self.board[x][y] != '.':
                    screen.blit(
                        pygame.transform.scale(self.im_board[self.board[x][y]], (self.cell_size, self.cell_size)),
                        (x * self.cell_size + self.left, y * self.cell_size + self.top))

        for y in range(len(self.tile_board)):
            for x in range(len(self.tile_board[y])):
                if self.tile_board[y][x]:
                    screen.blit(self.im_board1[y][x],
                                (x * self.tile_size + self.indent * x + (
                                        self.left - self.cell_size - self.tile_size * 5 - self.indent * 4) // 2,
                                 y * self.tile_size + self.indent * y + self.cell_size * 2))
                if self.tile_board[y][x] == self.brush:
                    pygame.draw.rect(screen, 'white',
                                     (x * self.tile_size + self.indent * x + (
                                             self.left - self.cell_size - self.tile_size * 5 - self.indent * 4) // 2 - 2,
                                      y * self.tile_size + self.indent * y + self.cell_size * 2 - 2,
                                      self.tile_size + 4, self.tile_size + 4), 2)

    def mouse_event(self, pos):
        x, y = pos
        x = x // self.cell_size - self.left // self.cell_size
        y = y // self.cell_size - self.top // self.cell_size
        try:
            if x < 0 or y < 0:
                raise IndexError
            self.board[x][y] = self.brush
        except IndexError:
            x, y = pos
            x = x // (self.tile_size + self.indent) - 1
            y = y // (self.tile_size + self.indent) - 1
            print(x, y)
            try:
                if x < 0 or y < 0:
                    raise IndexError
                if self.tile_board[y][x]:
                    self.brush = self.tile_board[y][x]
            except IndexError:
                pass

    def save(self):
        with open('map1.txt', 'w') as map:
            board = np.fliplr(np.rot90(self.board, 3))
            board = '\n'.join([''.join(board[i]) for i in range(self.width)])
            print(board, file=map)

    def rect(self, pos1, pos2):
        max_pos, min_pos = max(pos1[0], pos2[0]), min(pos1[0], pos2[0])
        for j in range(min_pos // self.cell_size * self.cell_size, max_pos, self.cell_size):
            self.mouse_event((j, pos1[1]))
            self.mouse_event((j, pos2[1]))
        max_pos, min_pos = max(pos1[1], pos2[1]), min(pos1[1], pos2[1])
        for j in range(min_pos // self.cell_size * self.cell_size, max_pos, self.cell_size):
            self.mouse_event((pos1[0], j))
            self.mouse_event((pos2[0], j))

    def clear(self):
        self.board = [['.' for _ in range(self.width)] for _ in range(self.height)]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
width, height = 70, 100
cell_size = 9
if True:
    with open('../map.txt', 'r') as txt_map:
        txt_map = [list(i) for i in txt_map.read().split('\n')]
        width, height = len(txt_map[0]), len(txt_map)
maker = LevelMaker(width, height, cell_size, txt_map)

clock = pygame.time.Clock()

mouse_down = False
rect_pos = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN or mouse_down:
            mouse_down = True
            rect_pos = []
            maker.mouse_event(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                maker.save()
                print(1)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:
                if rect_pos:
                    rect_pos.append(pygame.mouse.get_pos())
                    maker.rect(*rect_pos)
                    rect_pos = []
                else:
                    rect_pos.append(pygame.mouse.get_pos())
            elif event.key == pygame.K_c:
                maker.clear()
    screen.fill((0, 0, 0))
    maker.paint(screen)

    pygame.display.flip()
    clock.tick()
