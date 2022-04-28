from door import Door
from settings import *
from map import world_map, map_for_lighting, light_emitter_map, foreground_world_map, door_map


class Manager:
    def __init__(self, screen, player):
        self.screen = screen
        self.doors = [Door(18 * 14, 18 * 39, player, math.pi / 2 * 3),
                      Door(18 * 14, 18 * 39 + 8, player, math.pi / 2)]
        self.player = player
        self.sc = pygame.Surface((WIDTH, HEIGHT))
        self.sc_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
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

    def paint(self):
        self.sc.fill((120, 120, 120))
        self.sc_light.fill((50, 50, 50, 0))

        door_map_copy = door_map.copy()
        for door in self.doors:
            door.move()
            door_map_copy = door.get(door_map_copy)
        self.sc_light_emitter1.fill((40, 40, 40))
        self.sc_light_emitter.fill((50, 50, 50))
        for i in light_emitter_map:
            if self.player.line_collider.x - LIGHT_RENDERING_RANGE[0] < i.x < self.player.line_collider.x + \
                    LIGHT_RENDERING_RANGE[0] and \
                    self.player.line_collider.y - LIGHT_RENDERING_RANGE[1] < i.y < self.player.line_collider.y + \
                    LIGHT_RENDERING_RANGE[1]:
                intensity = 0
                i.paint_light(self.sc_light_emitter, self.sc_light_emitter1,
                              (intensity, intensity, intensity), self.player.scroll, map_for_lighting, door_map_copy)
        self.sc.blit(self.sc_light_emitter1, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.sc.blit(self.sc_middle_plan, (-self.player.scroll[0], -self.player.scroll[1]))
        self.sc.blit(self.sc_light_emitter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.player.paint_light(self.sc_light, map_for_lighting, door_map_copy)
        self.sc.blit(self.sc_light, (0, 0))
        self.player.paint(self.sc)
        self.sc.blit(self.sc_foreground, (-self.player.scroll[0], -self.player.scroll[1]))
        self.screen.blit(self.sc, (0, 0))
        for door in self.doors:
            door.paint(self.screen, self.player.scroll)
