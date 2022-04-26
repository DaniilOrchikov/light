import pygame

from settings import *
from map import world_map, map_for_lighting, light_emitter_map, foreground_world_map


class Manager:
    def __init__(self, screen, player):
        self.screen = screen
        self.sc = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.bounding_box = [*[(i * TILE, -2 * TILE) for i in range(-2, WIDTH // TILE + 2)],
                             *[(i * TILE, HEIGHT + 2 * TILE) for i in range(-2, WIDTH // TILE + 2)],
                             *[(-2 * TILE, i * TILE) for i in range(-2, HEIGHT // TILE + 2)],
                             *[(WIDTH + 2 * TILE, i * TILE) for i in range(-2, HEIGHT // TILE + 2)]]
        self.bounding_box = set(self.bounding_box)
        self.sc_middle_plan = pygame.Surface((WIDTH * 3, HEIGHT * 3), pygame.SRCALPHA)
        self.sc_middle_plan.fill((0, 0, 0, 0))
        self.sc_foreground = pygame.Surface((WIDTH * 3, HEIGHT * 3), pygame.SRCALPHA)
        self.sc_foreground.fill((0, 0, 0, 0))
        for tile in world_map:
            tile.paint(self.sc_middle_plan)
        for tile in foreground_world_map:
            tile.paint(self.sc_foreground)
        for i in light_emitter_map:
            i.paint(self.sc_middle_plan)
        self.sc_light_emitter = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light_emitter1 = pygame.Surface((WIDTH, HEIGHT))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, RED)
        self.screen.blit(render, FPS_POS)

    def paint(self, player):
        self.sc.fill((120, 120, 120))
        self.sc_light.fill((50, 50, 50, 0))

        bounding_box = set(((i[0] + player.scroll[0]) // TILE * TILE, (i[1] + player.scroll[1]) // TILE * TILE) for i in
                           self.bounding_box)
        # map_for_lighting_copy = map_for_lighting.union(bounding_box)
        self.sc_light_emitter1.fill((40, 40, 40))
        self.sc_light_emitter.fill((50, 50, 50))
        for i in light_emitter_map:
            intensity = 0
            i.paint_light(self.sc_light_emitter, self.sc_light_emitter1,
                          (intensity, intensity, intensity), player.scroll, map_for_lighting)
        self.sc.blit(self.sc_light_emitter1, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.sc.blit(self.sc_middle_plan, (-player.scroll[0], -player.scroll[1]))
        self.sc.blit(self.sc_light_emitter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        player.paint_light(self.sc_light, map_for_lighting)
        self.sc.blit(self.sc_light, (0, 0))
        player.paint(self.sc)
        self.sc.blit(self.sc_foreground, (-player.scroll[0], -player.scroll[1]))
        self.screen.blit(self.sc, (0, 0))
