import pygame.image


class Cursor:
    def __init__(self):
        self.im = pygame.image.load('data/icons/cursor.png').convert_alpha()

    def paint(self, x, y, sc):
        sc.blit(self.im, (x - self.im.get_width() // 2, y - self.im.get_height() // 2))
