from settings import *
import pygame
import math


class Player:
    def __init__(self, physics):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.scroll = [0, 0]
        self.rect = pygame.Rect(self.x, self.y, TILE // 2, TILE // 2)
        self.im = pygame.Surface((TILE // 2, TILE // 2))
        self.im.fill((255, 0, 0))
        self.physics = physics

    @property
    def pos(self):
        return self.rect.x + TILE // 4, self.rect.y + TILE // 4

    def movement(self):
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
        if keys[pygame.K_LEFT]:
            self.angle -= 0.04
        if keys[pygame.K_RIGHT]:
            self.angle += 0.04

        self.scroll[0] += round((self.rect.x - self.scroll[0] - HALF_WIDTH) / 10, 2)
        self.scroll[1] += round((self.rect.y - self.scroll[1] - HALF_HEIGHT) / 10, 2)

    def paint(self, sc):
        sc.blit(self.im, (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1]))
