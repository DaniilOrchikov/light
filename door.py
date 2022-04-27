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
        self.player_stop = True
        self.line_collider = None
        self.player = player
        self.light_rect = None
        self.x, self.y = x, y
        self.ANGLE = math.pi / 2
        self.angle = self.ANGLE
        self.length = 18 * 4
        self.m = True
        self.is_open = False
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y

        self.OPEN_COUNT = 60
        self.open_count = 0

        self.generate()

    def generate(self):
        self.light_rect = []
        for j in range(0, 2):
            self.light_rect.extend(
                [(int(i[0] // 8) + j, int(i[1] // 8) + j) for i in
                 line(self.x, self.y, int(self.x1), int(self.y1))])
            self.light_rect.extend(
                [(int(i[0] // 8), int(i[1] // 8) + j) for i in
                 line(self.x, self.y, int(self.x1), int(self.y1))])
            self.light_rect.extend(
                [(int(i[0] // 8) + j, int(i[1] // 8)) for i in
                 line(self.x, self.y, int(self.x1), int(self.y1))])
        self.light_rect = list(set(self.light_rect))

        if not self.is_open or self.player_stop:
            if not self.is_open:
                self.rect = pygame.Rect(self.x - 4, self.y, 8, self.length)
            else:
                if self.x1 < self.x:
                    self.rect = pygame.Rect(self.x1, self.y1 - 4, self.length, 8)
                else:
                    self.rect = pygame.Rect(self.x, self.y - 4, self.length, 8)
        else:
            self.rect = None

        self.line_collider = [(self.x - 5, self.y - 5, self.x1 - 5, self.y1 - 5),
                              (self.x + 5, self.y + 5, self.x1 + 5, self.y1 + 5)]

    def get(self, arr):
        for i in self.light_rect:
            arr[i] = 1
        return arr

    def paint(self, sc, scroll):
        # for i in self.light_rect:
        #     pygame.draw.rect(sc, 'red', (i[0] * 8 - scroll[0], i[1] * 8 - scroll[1], 8, 8))
        # pygame.draw.line(sc, 'red', (self.line_collider[0] - scroll[0], self.line_collider[1] - scroll[1]),
        #                  (self.line_collider[2] - scroll[0], self.line_collider[3] - scroll[1]), 20)
        for i in self.line_collider:
            pygame.draw.line(sc, 'red', (i[0] - scroll[0], i[1] - scroll[1]), (i[2] - scroll[0], i[3] - scroll[1]))
        if self.rect:
            pygame.draw.rect(sc, 'blue', (self.rect[0] - scroll[0], self.rect[1] - scroll[1],
                                          self.rect[2], self.rect[3]))

    def open(self):
        self.is_open = True
        self.open_count = self.OPEN_COUNT
        self.push()

    def close(self):
        self.is_open = False
        self.angle = self.ANGLE
        self.push()

    def push(self, right='None', top='None'):
        speed = 0.1
        while self.angle < 0:
            self.angle += math.pi * 2
        while self.angle > math.pi * 2:
            self.angle -= math.pi * 2
        if right != 'None' or top != 'None':
            self.open_count = 0
        if self.is_open:
            angle = 0
            if 0 <= self.angle < math.pi / 2 and (top == 'False' or right == 'False'):
                angle += speed
            elif 0 < self.angle <= math.pi / 2 and (top == 'True' or right == 'True'):
                angle -= speed
            elif math.pi / 2 <= self.angle < math.pi and (right == 'False' or top == 'True'):
                angle += speed
            elif math.pi / 2 < self.angle <= math.pi and (right == 'True' or top == 'False'):
                angle -= speed
            elif math.pi <= self.angle < math.pi / 2 * 3 and (top == 'True' or right == 'True'):
                angle += speed
            elif math.pi < self.angle <= math.pi / 2 * 3 and (top == 'False' or right == 'False'):
                angle -= speed
            elif math.pi / 2 * 3 <= self.angle < math.pi * 2 and (right == 'True' or top == 'False'):
                angle += speed
            elif math.pi / 2 * 3 < self.angle <= math.pi * 2 and (right == 'False' or top == 'True'):
                angle -= speed
            if self.ANGLE + math.pi / 2 < self.angle < math.pi * 2 - 0.1 and angle > 0 or \
                    math.pi * 2 > self.angle > math.pi + 0.1 and angle < 0:
                self.player_stop = True
                angle = 0
            else:
                self.player_stop = False
            self.angle += angle
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y

    def move(self):
        if self.open_count:
            self.open_count -= 1
            self.angle += math.pi / 2 / self.OPEN_COUNT
            self.push()
        self.generate()
