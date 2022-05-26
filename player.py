import pygame.draw
from numba import njit
from pygame import gfxdraw

from map import player_pos
from ray_casting import calculating_lightning
from settings import *


@njit(fastmath=True, cache=True)
def get_angle(mouse_pos):
    return math.atan2(mouse_pos[1] - HALF_HEIGHT - 8, mouse_pos[0] - HALF_WIDTH - 8)


class Player:
    def __init__(self, physics):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.scroll = [0.0, 0.0]
        self.size = TILE * 1.5
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.im = pygame.Surface((self.size, self.size))
        self.im.fill((255, 0, 0))
        self.physics = physics
        self.light_im = pygame.image.load('data/light/light.png').convert_alpha()
        self.is_move = False
        self.right, self.top = 'None', 'None'

    @property
    def pos(self):
        return self.rect.x + self.size // 2, self.rect.y + self.size // 2

    def movement(self, doors):
        doors = list(filter(
            lambda door: self.rect.x - RENDERING_RANGE[0] < door.x < self.rect.x + RENDERING_RANGE[0] and self.rect.y -
                         RENDERING_RANGE[1] < door.y < self.rect.y + RENDERING_RANGE[1], doors))
        self.right, self.top = 'None', 'None'
        self.is_move = False
        move = [0, 0]
        keys = pygame.key.get_pressed()
        speed = player_speed if not keys[pygame.K_LSHIFT] else player_shift_speed
        if keys[pygame.K_w]:
            move[1] += -speed
            self.top = 'True'
        if keys[pygame.K_s]:
            move[1] += speed
            self.top = 'False'
        if keys[pygame.K_a]:
            move[0] += -speed
            self.right = 'False'
        if keys[pygame.K_d]:
            move[0] += speed
            self.right = 'True'
        self.is_move = move != [0, 0]
        if move[0] and move[1] and keys[pygame.K_LSHIFT]:
            move[0] = move[0] + (1 if move[0] < 0 else -1)
            move[1] = move[1] + (1 if move[1] < 0 else -1)
        self.collisions = self.physics.movement(self.rect, move, doors)
        if self.collisions['door']:
            if self.is_move:
                self.collisions['door'].push(self.right, self.top)
            elif self.collisions['door'].open_count:
                self.collisions['door'].push('X', "x")
        mouse_pos = pygame.mouse.get_pos()
        self.angle = get_angle(mouse_pos)

        self.scroll[0] += round((self.pos[0] - self.scroll[0] - HALF_WIDTH) / 10)
        self.scroll[1] += round((self.pos[1] - self.scroll[1] - HALF_HEIGHT) / 10)

    def paint_light(self, sc_light, world_map, door_map):
        rays = calculating_lightning(self.pos, self.angle, FOV, False, world_map, door_map, self.rect.y)
        rays = [(i[0] - self.scroll[0], i[1] - self.scroll[1]) for i in rays]
        if len(rays) > 2:
            # pygame.draw.polygon(sc_light, (0, 0, 0), rays)
            gfxdraw.filled_polygon(sc_light, rays, (0, 0, 0))
        sc_light.blit(self.light_im, (self.rect.x - self.scroll[0] - self.light_im.get_width() // 2 + self.size // 2,
                                      self.rect.y - self.scroll[1] - self.light_im.get_height() // 2 + self.size // 2))

    def paint(self, sc):
        sc.blit(self.im, (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1]))
