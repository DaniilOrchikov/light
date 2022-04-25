import pygame
from pygame import gfxdraw

from settings import *
from ray_casting import ray_casting
from map import world_map, map_for_lighting, light_emitter_map


class Manager:
    def __init__(self, screen):
        self.screen = screen
        self.l = pygame.Surface((WIDTH, HEIGHT))
        self.sc = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.bounding_box = [*[(i * TILE, -2 * TILE) for i in range(-2, WIDTH // TILE + 2)],
                             *[(i * TILE, HEIGHT + 2 * TILE) for i in range(-2, WIDTH // TILE + 2)],
                             *[(-2 * TILE, i * TILE) for i in range(-2, HEIGHT // TILE + 2)],
                             *[(WIDTH + 2 * TILE, i * TILE) for i in range(-2, HEIGHT // TILE + 2)]]
        self.bounding_box = set(self.bounding_box)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, RED)
        self.screen.blit(render, FPS_POS)

    def paint(self, player):
        self.sc.fill((80, 80, 80))
        self.l.fill((30, 30, 30))
        self.sc_light.fill((30, 30, 30))
        for tile in world_map:
            tile.paint(self.sc, player.scroll)

        bounding_box = set(((i[0] + player.scroll[0]) // TILE * TILE, (i[1] + player.scroll[1]) // TILE * TILE) for i in
                           self.bounding_box)
        map_for_lighting_copy = map_for_lighting.union(bounding_box)
        rays = ray_casting(player.pos, player.angle, map_for_lighting_copy, player.scroll, FOV, True)
        try:
            pygame.draw.polygon(self.sc_light, (0, 0, 0), rays)
            # gfxdraw.aapolygon(self.l, rays, (0, 0, 0))
        except ValueError:
            pass
        for i in light_emitter_map:
            i.paint(self.l, player.scroll, map_for_lighting.copy())
        self.sc.blit(self.sc_light, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.sc.blit(self.l, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        player.paint(self.sc)
        self.screen.blit(self.sc, (0, 0))
