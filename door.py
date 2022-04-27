import math

import pygame
from numba import njit


@njit(fastmath=True, cache=True)
def line(x1, y1, x2, y2):
    arr = []
    dx, dy = x2 - x1, y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y, error, t = x1, y1, el / 2, 0
    arr.append((x, y))
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        arr.append((x, y))
    return arr


class Door:
    def __init__(self, x, y, player):
        self.rect = None
        self.player = player
        self.light_rect = None
        self.x, self.y = x, y
        self.angle = -1.1
        self.c = 0
        self.length = 18 * 3
        self.m = True
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y
        self.generate()

    def generate(self):
        self.light_rect = []
        for j in range(-8, 8, 8):
            self.light_rect.extend(
                [(i[0] // 8 * 8 + j, i[1] // 8 * 8 + j) for i in line(self.x, self.y, int(self.x1), int(self.y1))])
        self.rect = [self.x, self.y, self.x1, self.y1]

    def get(self, arr):
        for i in self.light_rect:
            arr[i] = 1
        return arr

    def paint(self, sc, scroll):
        pygame.draw.line(sc, 'red', (self.rect[0] - scroll[0], self.rect[1] - scroll[1]),
                         (self.rect[2] - scroll[0], self.rect[3] - scroll[1]))

    def push(self, right, top):
        speed = 0.1
        while self.angle < 0:
            self.angle += math.pi * 2
        while self.angle > math.pi * 2:
            self.angle -= math.pi * 2
        print(self.angle, right, top)
        if 0 <= self.angle < math.pi / 2 and (top == 'False' or right == 'False'):
            self.angle += speed
        elif 0 < self.angle <= math.pi / 2 and (top == 'True' or right == 'True'):
            self.angle -= speed
        elif math.pi / 2 <= self.angle < math.pi and (right == 'False' or top == 'True'):
            self.angle += speed
        elif math.pi / 2 < self.angle <= math.pi and (right == 'True' or top == 'False'):
            self.angle -= speed
        elif math.pi <= self.angle < math.pi / 2 * 3 and (top == 'True' or right == 'True'):
            self.angle += speed
        elif math.pi < self.angle <= math.pi / 2 * 3 and (top == 'False' or right == 'False'):
            self.angle -= speed
        elif math.pi / 2 * 3 <= self.angle < math.pi * 2 and (right == 'True' or top == 'False'):
            self.angle += speed
        elif math.pi / 2 * 3 < self.angle <= math.pi * 2 and (right == 'False' or top == 'True'):
            self.angle -= speed
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y

    def move(self):
        self.generate()
