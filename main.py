import sys

from cursor import Cursor
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF)

from physics import Physics
from player import Player
from map import physics_world_map
from manager import Manager

clock = pygame.time.Clock()
physics = Physics(physics_world_map)
player = Player(physics)
manager = Manager(screen, player)
pygame.mouse.set_visible(False)
cursor = Cursor()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if manager.door.is_open:
                    manager.door.close()
                else:
                    manager.door.open()
    player.movement(manager.door)
    screen.fill((80, 80, 255))

    manager.paint()
    manager.fps(clock)

    cursor.paint(*pygame.mouse.get_pos(), screen)

    pygame.display.flip()
    clock.tick()
