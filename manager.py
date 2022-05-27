import pygame.gfxdraw
from numba import njit

from connecting_squares import connecting_squares, paint_connecting_squares
from level import create_level
from map import *


def cut_sc(sc):
    sc_list = []
    columns = sc.get_width() // WIDTH
    rows = sc.get_height() // HEIGHT
    rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    for j in range(rows):
        sc_list.append([])
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            sc_list[-1].append(sc.subsurface(pygame.Rect(frame_location, rect.size)))
    return sc_list


@njit(fastmath=True, cache=True)
def combining_rects(arr):
    new_arr = set()
    for y0 in range(len(arr)):
        min_y = 9999
        x0 = 0
        for x in range(len(arr[0])):
            if not arr[y0][x]:
                if x - x0 > 1 or min_y != 9999:
                    new_arr.add((x0 * TILE, y0 * TILE, x * TILE - x0 * TILE, (min_y + 1) * TILE - y0 * TILE))
                    for i in range(y0, min(len(arr), min_y + 1)):
                        for j in range(x0, min(x, len(arr[0]))):
                            arr[i][j] = 0
                x0 = x + 1
                min_y = 9999
                continue
            for y in range(y0, min(min_y, len(arr))):
                if not arr[y][x]:
                    min_y = min(min_y, y - 1)
                    break
    return new_arr


class Manager:
    def __init__(self, screen, player):
        scale_w, scale_h = math.ceil(len(world_map[0]) * TILE / WIDTH), math.ceil(len(world_map) * TILE / HEIGHT)
        self.scale = (scale_w, scale_h)
        self.screen = screen
        self.player = player
        self.doors = doors
        for i in self.doors:
            i.add_player(self.player)
        self.sc = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.sc_background = pygame.Surface((WIDTH * scale_w, HEIGHT * scale_h), pygame.SRCALPHA)
        self.sc_background.fill((0, 0, 0, 0))
        self.sc_middle_plan = pygame.Surface((WIDTH * scale_w, HEIGHT * scale_h), pygame.SRCALPHA)
        self.sc_middle_plan.fill((0, 0, 0, 0))
        self.sc_bounding_trees = pygame.Surface((WIDTH * scale_w, HEIGHT * scale_h), pygame.SRCALPHA)
        self.sc_bounding_trees.fill((0, 0, 0, 0))
        self.sc_foreground = pygame.Surface((WIDTH * scale_w, HEIGHT * scale_h), pygame.SRCALPHA)
        self.sc_foreground.fill((0, 0, 0, 0))

        self.sc_foreground_del = pygame.Surface((WIDTH, HEIGHT),
                                                pygame.SRCALPHA)  # для удаления листвы на месте курсора
        self.sc_foreground_del.fill((255, 255, 255))
        self.sc_foreground_del_1 = pygame.Surface((WIDTH, HEIGHT),
                                                  pygame.SRCALPHA)  # для удаления листвы на месте курсора
        self.sc_foreground_del_1.fill((255, 255, 255))
        self.sc_foreground_copy = pygame.Surface((WIDTH, HEIGHT),
                                                 pygame.SRCALPHA)  # копия слоя с деревьями для корректной работы удаления листвы

        self.sc_foreground_del_2 = pygame.Surface((WIDTH * scale_w, HEIGHT * scale_h),
                                                  pygame.SRCALPHA)  # для удаления листвы на месте пола
        paint_connecting_squares(connecting_squares(foreground_del), self.sc_foreground_del_2,
                                 (WIDTH * scale_w, HEIGHT * scale_h))
        self.cut_sc_foreground_del_2 = cut_sc(self.sc_foreground_del_2)

        self.sky_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.sky_screen.fill((0, 0, 0, 0))
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Arial', 36, bold=True)
        text = font.render('Рендерим локацию', True, 'white')
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        for tile in background_map_l1:
            tile.paint(self.sc_background)
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        for tile in background_map_l2:
            tile.paint(self.sc_background)
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        for tile in background_map_l3:
            tile.paint(self.sc_background)
        self.cut_sc_background = cut_sc(self.sc_background)
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        create_level(self.sc_middle_plan)
        self.cut_sc_middle_plan = cut_sc(self.sc_middle_plan)
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        for tile in foreground_world_map:
            if tile.type == 'tree':
                # чтобы окно не зависало при загрузке уровня
                pygame.event.get()
                # -------------------------------------------
                tile.paint(self.sc_foreground)
            else:
                tile.paint(self.sc_bounding_trees)
        # чтобы окно не зависало при загрузке уровня
        pygame.event.get()
        # -------------------------------------------
        self.cut_sc_foreground = cut_sc(self.sc_foreground)
        self.cut_sc_bounding_trees = cut_sc(self.sc_bounding_trees)
        self.sc_light_emitter = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light_emitter1 = pygame.Surface((WIDTH, HEIGHT))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, RED)
        self.screen.blit(render, FPS_POS)

    def paint(self, sunlight_intensity):
        self.sc.fill((105, 105, 105))
        self.sc_light.fill((50, 50, 50, 0))
        self.sky_screen.fill((0, 0, 0, 0))
        self.sc_foreground_copy.fill((0, 0, 0, 0))
        self.sc_light_emitter1.fill((40, 40, 40))
        self.sc_light_emitter.fill((50, 50, 50))
        self.sc_foreground_del.fill((255, 255, 255))
        self.sc_foreground_del_1.fill((255, 255, 255))
        # for polygon in self.foreground_del:
        #     pygame.gfxdraw.filled_polygon(self.sc_foreground_del,
        #                            [self.offset_of_the_painting_position(*i) for i in polygon],
        #                            (15, 16, 15, 150))
        # for i in range(6):
        #     for tile in self.foreground_del:
        #         pygame.draw.rect(self.sc_foreground_del, (15, 15, 15, 240 - i * 40),
        #                          (*self.offset_of_the_painting_position(tile[0] + i * 2, tile[1] + i * 2),
        #                           tile[2] - i * 4, tile[3] - i * 4))
        for i in range(12):
            pygame.draw.circle(self.sc_foreground_del_1, (0, 0, 0, 240 - i * 20), pygame.mouse.get_pos(),
                               100 - i * 3)
            pygame.draw.circle(self.sc_foreground_del_1, (0, 0, 0, 240 - i * 20),
                               self.offset_of_the_painting_position(self.player.pos[0], self.player.pos[1]),
                               120 - i * 3)
        self.sc_foreground_del.blit(self.sc_foreground_del_1, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.paint_map_pieces(self.sc_foreground_del, self.cut_sc_foreground_del_2, pygame.BLEND_RGBA_MIN)
        # self.sc_foreground_del.blit(self.sc_foreground_del_2, self.offset_of_the_painting_position(0, 0),
        #                             special_flags=pygame.BLEND_RGBA_MIN)

        door_map_copy = door_map.copy()
        for door in self.doors:
            if self.player.rect.x - RENDERING_RANGE[0] < door.x < self.player.rect.x + RENDERING_RANGE[0] and \
                    self.player.rect.y - RENDERING_RANGE[1] < door.y < self.player.rect.y + RENDERING_RANGE[1]:
                door.move()
                door_map_copy = door.get(door_map_copy)
        self.paint_map_pieces(self.sc, self.cut_sc_background)
        # self.sc.blit(self.sc_background, (-self.player.scroll[0], -self.player.scroll[1]))

        self.sky_screen.fill((0, 0, 0, SUNLIGHT_INTENSITY - sunlight_intensity))

        for i in light_emitter_map:
            if self.player.rect.x - RENDERING_RANGE[0] < i.x < self.player.rect.x + RENDERING_RANGE[0] and \
                    self.player.rect.y - RENDERING_RANGE[1] < i.y < self.player.rect.y + RENDERING_RANGE[1]:
                i.paint(self.sc_light_emitter, self.sc_light_emitter1, (10, 10, 10),
                        self.player.scroll, map_for_lighting, door_map_copy, self.player.rect.y, self.sc, self.player)
        self.player.paint_light(self.sc_light_emitter, map_for_lighting, door_map_copy)
        self.sc.blit(self.sc_light_emitter1, (0, 0),
                     special_flags=pygame.BLEND_RGBA_SUB)  # это отрисовывается ореол света рядом с лампой
        self.paint_map_pieces(self.sc, self.cut_sc_middle_plan)
        # self.sc.blit(self.sc_middle_plan, (-self.player.scroll[0], -self.player.scroll[1]))
        self.player.paint(self.sc)
        for door in self.doors:
            if self.player.rect.x - RENDERING_RANGE[0] < door.x < self.player.rect.x + RENDERING_RANGE[0] and \
                    self.player.rect.y - RENDERING_RANGE[1] < door.y < self.player.rect.y + RENDERING_RANGE[1]:
                door.paint(self.sc, self.player.scroll)
        self.paint_map_pieces(self.sc_foreground_copy, self.cut_sc_foreground)
        # self.sc_foreground_copy.blit(self.sc_foreground, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc_foreground_copy.blit(self.sc_foreground_del, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.sc.blit(self.sc_foreground_copy, (0, 0))
        self.paint_map_pieces(self.sc, self.cut_sc_bounding_trees)
        # self.sc.blit(self.sc_bounding_trees, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc.blit(self.sky_screen, (0, 0))
        self.sc.blit(self.sc_light_emitter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.sc.blit(self.sc_light, (0, 0))
        self.screen.blit(self.sc, (0, 0))

    def paint_map_pieces(self, sc, sc_list, flag=None):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if flag is not None:
                    sc.blit(sc_list[self.player.rect.y // HEIGHT + j][self.player.rect.x // WIDTH + i], (
                        self.offset_of_the_painting_position((self.player.rect.x // WIDTH + i) * WIDTH,
                                                             (self.player.rect.y // HEIGHT + j) * HEIGHT)),
                            special_flags=flag)
                else:
                    sc.blit(sc_list[self.player.rect.y // HEIGHT + j][self.player.rect.x // WIDTH + i], (
                        self.offset_of_the_painting_position((self.player.rect.x // WIDTH + i) * WIDTH,
                                                             (self.player.rect.y // HEIGHT + j) * HEIGHT)))

    def offset_of_the_painting_position(self, x, y):
        return round(x - self.player.scroll[0]), round(y - self.player.scroll[1])
