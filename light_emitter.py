from ray_casting import ray_casting
from settings import *


class LightEmitter:
    light_im = pygame.image.load('data/light/lamp_light.png').convert_alpha()

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.im = pygame.image.load('data/tiles/lamp.png').convert_alpha()
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))
        self.light_im = LightEmitter.light_im.convert_alpha()

    def paint_light(self, sc, sc1, intensity, scroll, world_map, door_map):
        rays = ray_casting((self.x + TILE // 2, self.y + TILE // 2), 0, math.pi * 2, True, world_map, door_map)[1:]
        rays = [(i[0] - scroll[0], i[1] - scroll[1]) for i in rays]
        try:
            pygame.draw.polygon(sc, intensity, rays)
        except ValueError:
            pass
        sc1.blit(self.light_im, (self.x - scroll[0] - self.light_im.get_width() // 2 + TILE // 2,
                                 self.y - scroll[1] - self.light_im.get_height() // 2 + TILE // 2))

    def paint(self, screen):

        screen.blit(self.im, (self.x, self.y))
