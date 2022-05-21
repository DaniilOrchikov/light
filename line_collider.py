import pygame.draw

from settings import *


class LineCollider:
    def __init__(self, x, y, angle, length, width):
        self.line_collider = None
        self.x2_1 = None
        self.y2_1 = None
        self.y1_1 = None
        self.x1_1 = None
        self.y2 = None
        self.x2 = None
        self.y1 = None
        self.x1 = None
        self.y = x
        self.x = y
        self.regenerate(x, y, angle, length, width)

    def regenerate(self, x, y, angle, length, width):
        self.x, self.y = x, y
        self.x1, self.y1 = x, y
        self.x2, self.y2 = math.cos(angle) * width + x, math.sin(angle) * width + y
        self.x1_1, self.y1_1 = math.cos(angle + math.pi / 2) * length + self.x1, \
                               math.sin(angle + math.pi / 2) * length + self.y1
        self.x2_1, self.y2_1 = math.cos(angle + math.pi / 2) * length + self.x2, \
                               math.sin(angle + math.pi / 2) * length + self.y2
        self.line_collider = [[self.x1, self.y1, self.x1_1, self.y1_1], [self.x2, self.y2, self.x2_1, self.y2_1],
                              [self.x1, self.y1, self.x2, self.y2], [self.x1_1, self.y1_1, self.x2_1, self.y2_1]]

    def paint(self, sc, scroll):
        for i in self.line_collider:
            pygame.draw.line(sc, 'red', (i[0] - scroll[0], i[1] - scroll[1]), (i[2] - scroll[0], i[3] - scroll[1]))
        pygame.draw.circle(sc, 'blue', (self.x1 - scroll[0], self.y1 - scroll[1]), 5)
        pygame.draw.circle(sc, 'green', (self.x2 - scroll[0], self.y2 - scroll[1]), 5)
