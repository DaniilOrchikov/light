import pygame.draw

from ray_casting import calculating_lightning
from settings import *


class LightEmitter:
    light_im = pygame.image.load('data/light/lamp_light.png').convert_alpha()

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.image.load('data/tiles/lamp.png').convert_alpha()
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))
        self.light_im = LightEmitter.light_im.convert_alpha()
        self.rect = pygame.Rect(self.x - TILE // 4, self.y - TILE // 4, TILE + TILE // 2, TILE + TILE // 2)
        self.on = True
        self.TURN_ON_TIME = 15
        self.turn_on_time = 0

    def on_off(self):
        self.on = not self.on
        self.turn_on_time = self.TURN_ON_TIME

    def paint_light(self, sc, sc1, intensity, scroll, world_map, door_map, player_pos_y):
        if self.turn_on_time:
            self.turn_on_time -= 1
        if self.on and self.turn_on_time % randint(2, 7) == 0:
            rays = calculating_lightning((self.x + TILE // 2, self.y + TILE // 2), 0, math.pi * 2, True, world_map,
                                         door_map, player_pos_y)[1:]
            rays = [(i[0] - scroll[0], i[1] - scroll[1]) for i in rays]
            try:
                pygame.draw.polygon(sc, intensity, rays)
            except ValueError:
                pass
            sc1.blit(self.light_im, (self.x - scroll[0] - self.light_im.get_width() // 2 + TILE // 2,
                                     self.y - scroll[1] - self.light_im.get_height() // 2 + TILE // 2))

    def paint(self, screen):
        screen.blit(self.im, (self.x, self.y))
