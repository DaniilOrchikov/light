import pygame.draw
from pygame import gfxdraw

from ray_casting import calculating_lightning
from settings import *


class LightEmitter:
    light_im = pygame.image.load('data/light/lamp_light.png').convert_alpha()

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.on_im = pygame.image.load('data/lamp/on.png').convert_alpha()
        self.off_im = pygame.image.load('data/lamp/off.png').convert_alpha()
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))
        self.light_im = LightEmitter.light_im.convert_alpha()
        self.rect = pygame.Rect(self.x - TILE // 4, self.y - TILE // 4, TILE + TILE // 2, TILE + TILE // 2)
        self.on = True
        self.TURN_ON_TIME = 15
        self.turn_on_time = 0

    def on_off(self):
        self.on = not self.on
        self.turn_on_time = self.TURN_ON_TIME

    def paint(self, sc, sc1, intensity, scroll, world_map, door_map, player_pos_y, screen, player):
        # освещение
        if self.turn_on_time:
            self.turn_on_time -= 1
        if self.on and self.turn_on_time % randint(2, 7) == 0:
            rays = calculating_lightning((self.x + TILE // 2, self.y + TILE // 2), 0, math.pi * 2, True, world_map,
                                         door_map, player_pos_y)[1:]
            rays = [(i[0] - scroll[0], i[1] - scroll[1]) for i in rays]
            if len(rays) > 2:
                # pygame.draw.polygon(sc, intensity, rays)
                gfxdraw.filled_polygon(sc, rays, intensity)
            sc1.blit(self.light_im, (self.x - scroll[0] - self.light_im.get_width() // 2 + self.on_im.get_width() // 2,
                                     self.y - scroll[
                                         1] - self.light_im.get_height() // 2 + self.on_im.get_height() // 2))
        # спрайт лампы
            screen.blit(self.on_im, (self.x - player.scroll[0], self.y - player.scroll[1]))
        else:
            screen.blit(self.off_im, (self.x - player.scroll[0], self.y - player.scroll[1]))
