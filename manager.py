import pygame.draw

from level import create_level
from settings import *
from map import *


class Manager:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.doors = doors
        for i in self.doors:
            i.add_player(self.player)
        self.sc = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.sc_background = pygame.Surface((WIDTH * 6, HEIGHT * 6), pygame.SRCALPHA)
        self.sc_background.fill((0, 0, 0, 0))
        self.sc_middle_plan = pygame.Surface((WIDTH * 6, HEIGHT * 6), pygame.SRCALPHA)
        self.sc_middle_plan.fill((0, 0, 0, 0))
        self.sc_lamp = pygame.Surface((WIDTH * 6, HEIGHT * 6), pygame.SRCALPHA)
        self.sc_lamp.fill((0, 0, 0, 0))
        self.sc_bounding_trees = pygame.Surface((WIDTH * 6, HEIGHT * 6), pygame.SRCALPHA)
        self.sc_bounding_trees.fill((0, 0, 0, 0))
        self.sc_foreground = pygame.Surface((WIDTH * 6, HEIGHT * 6), pygame.SRCALPHA)
        self.sc_foreground.fill((0, 0, 0, 0))

        self.sc_foreground_del = pygame.Surface((WIDTH, HEIGHT),
                                                pygame.SRCALPHA)  # для удаления деревьев на месте курсора
        self.sc_foreground_del.fill((255, 255, 255))
        self.sc_foreground_copy = pygame.Surface((WIDTH, HEIGHT),
                                                 pygame.SRCALPHA)  # копия слоя с деревьями для корректной работы их удаления

        self.sky_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.sky_screen.fill((0, 0, 0, 0))
        for tile in background_map_l1:
            tile.paint(self.sc_background)
        for tile in background_map_l2:
            tile.paint(self.sc_background)
        for tile in background_map_l3:
            tile.paint(self.sc_background)
        create_level(self.sc_middle_plan)
        for tile in foreground_world_map:
            if tile.type == 'tree':
                tile.paint(self.sc_foreground)
            else:
                tile.paint(self.sc_bounding_trees)
        self.sc_light_emitter = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light_emitter1 = pygame.Surface((WIDTH, HEIGHT))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, RED)
        self.screen.blit(render, FPS_POS)

    def paint(self, sunlight_intensity):
        self.sc.fill((105, 105, 105))
        self.sc_light.fill((50, 50, 50, 0))
        self.sc_lamp.fill((0, 0, 0, 0))
        self.sky_screen.fill((0, 0, 0, 0))
        self.sc_foreground_copy.fill((0, 0, 0, 0))
        self.sc_foreground_del.fill((255, 255, 255))
        for i in range(12):
            pygame.draw.circle(self.sc_foreground_del, (0, 0, 0, 180 - i * 15), pygame.mouse.get_pos(), 100 - i * 3)
            pygame.draw.circle(self.sc_foreground_del, (0, 0, 0, 180 - i * 15),
                               (self.player.pos[0] - self.player.scroll[0], self.player.pos[1] - self.player.scroll[1]),
                               90 - i * 3)

        door_map_copy = door_map.copy()
        for door in self.doors:
            if self.player.rect.x - RENDERING_RANGE[0] < door.x < self.player.rect.x + RENDERING_RANGE[0] and \
                    self.player.rect.y - RENDERING_RANGE[1] < door.y < self.player.rect.y + RENDERING_RANGE[1]:
                door.move()
                door_map_copy = door.get(door_map_copy)
        self.sc_light_emitter1.fill((40, 40, 40))
        self.sc_light_emitter.fill((50, 50, 50))
        for i in light_emitter_map:
            if self.player.rect.x - RENDERING_RANGE[0] < i.x < self.player.rect.x + RENDERING_RANGE[0] and \
                    self.player.rect.y - RENDERING_RANGE[1] < i.y < self.player.rect.y + RENDERING_RANGE[1]:
                i.paint(self.sc_light_emitter, self.sc_light_emitter1, (10, 10, 10),
                        self.player.scroll, map_for_lighting, door_map_copy, self.player.rect.y, self.sc_lamp)
        self.sc.blit(self.sc_background, (-self.player.scroll[0], -self.player.scroll[1]))

        self.sky_screen.fill((0, 0, 0, 90 - sunlight_intensity))
        self.sc.blit(self.sky_screen, (0, 0))

        self.player.paint_light(self.sc_light_emitter, map_for_lighting, door_map_copy)
        self.sc.blit(self.sc_light_emitter1, (0, 0),
                     special_flags=pygame.BLEND_RGBA_SUB)  # это отрисовывается ореол света рядом с лампой
        self.sc.blit(self.sc_lamp, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc.blit(self.sc_middle_plan, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc.blit(self.sc_light_emitter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.sc.blit(self.sc_light, (0, 0))
        self.player.paint(self.sc)
        for door in self.doors:
            door.paint(self.sc, self.player.scroll)
        self.sc_foreground_copy.blit(self.sc_foreground, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc_foreground_copy.blit(self.sc_foreground_del, (0, 0),
                                     special_flags=pygame.BLEND_RGBA_MIN)
        self.sc.blit(self.sc_foreground_copy, (0, 0))
        self.sc.blit(self.sc_bounding_trees, (-self.player.scroll[0], -self.player.scroll[1]))
        self.screen.blit(self.sc, (0, 0))
