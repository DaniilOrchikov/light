from numba import njit

from ray_casting import ray_casting
from settings import *
import pygame


@njit(fastmath=True, cache=True)
def get_angle(mouse_pos):
    return math.atan2(mouse_pos[1] - HALF_HEIGHT, mouse_pos[0] - HALF_WIDTH)


class Player:
    def __init__(self, physics):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.scroll = [0.0, 0.0]
        self.size = TILE // 2
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.im = pygame.Surface((self.size, self.size))
        self.im.fill((255, 0, 0))
        self.physics = physics
        self.light_im = pygame.image.load('data/light/light.png').convert_alpha()

    @property
    def pos(self):
        return self.rect.x + self.size // 2, self.rect.y + self.size // 2

    def movement(self, sc):
        move = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move[1] += -player_speed
        if keys[pygame.K_s]:
            move[1] += player_speed
        if keys[pygame.K_a]:
            move[0] += -player_speed
        if keys[pygame.K_d]:
            move[0] += player_speed
        collisions = self.physics.movement(self.rect, move)
        mouse_pos = pygame.mouse.get_pos()
        self.angle = get_angle(mouse_pos)

        self.scroll[0] += round((self.rect.x - self.scroll[0] - HALF_WIDTH) / 10, 2)
        self.scroll[1] += round((self.rect.y - self.scroll[1] - HALF_HEIGHT) / 10, 2)

    def paint_light(self, sc_light, world_map):
        rays = ray_casting(self.pos, self.angle, FOV, False, world_map)
        rays = [(i[0] - self.scroll[0], i[1] - self.scroll[1]) for i in rays]
        try:
            pygame.draw.polygon(sc_light, (234, 224, 191, 100), rays)
        except ValueError:
            pass
        sc_light.blit(self.light_im, (self.rect.x - self.scroll[0] - self.light_im.get_width() // 2 + self.size // 2,
                                      self.rect.y - self.scroll[1] - self.light_im.get_height() // 2 + self.size // 2))

    def paint(self, sc):
        sc.blit(self.im, (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1]))
