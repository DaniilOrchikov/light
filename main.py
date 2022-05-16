import sys

from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF)

from cursor import Cursor
from physics import Physics
from player import Player
from manager import Manager

clock = pygame.time.Clock()
physics = Physics()
player = Player(physics)
manager = Manager(screen, player)
pygame.mouse.set_visible(False)
cursor = Cursor()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    player.movement(manager.doors)
    screen.fill((80, 80, 255))

    manager.paint()
    manager.fps(clock)

    cursor.event_controller(events, manager.doors, player.scroll)
    cursor.paint(*pygame.mouse.get_pos(), screen)

    pygame.display.flip()
    clock.tick(FPS)
