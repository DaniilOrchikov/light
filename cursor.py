import pygame.image

from map import light_emitter_map
from physics import door_collision


class Cursor:
    def __init__(self):
        self.im = pygame.image.load('data/icons/cursor.png').convert_alpha()
        self.rect = pygame.Rect(*[i - 8 for i in pygame.mouse.get_pos()], 16, 16)

    def event_controller(self, event, doors, scroll):
        self.rect = pygame.Rect(*[i - 8 for i in pygame.mouse.get_pos()], 16, 16)
        self.rect[0] += scroll[0]
        self.rect[1] += scroll[1]
        collide_door = None
        for door in doors:
            if door_collision((self.rect[0], self.rect[1], self.rect[2], self.rect[3]), door.line_collider):
                collide_door = door
                break
        if collide_door is not None and pygame.mouse.get_pressed(3)[0]:
            if collide_door.is_open:
                collide_door.close()
            else:
                collide_door.open()
        collide_lamp = None
        for lamp in light_emitter_map:
            if self.rect.colliderect(lamp.rect):
                collide_lamp = lamp
                break
        if collide_lamp is not None and pygame.mouse.get_pressed(3)[0]:
            if not collide_lamp.turn_on_time:
                collide_lamp.on_off()

    def paint(self, x, y, sc):
        sc.blit(self.im, (x - self.im.get_width() // 2, y - self.im.get_height() // 2))
