import sys

from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF)

font = pygame.font.SysFont('Arial', 36, bold=True)
text = font.render('Загружаем ресурсы', True, 'white')
screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()

from cursor import Cursor
from physics import Physics
from player import Player
from manager import Manager

clock = pygame.time.Clock()
physics = Physics()
player = Player(physics)
manager = Manager(screen, player)
pygame.mouse.set_visible(False)
cursor = Cursor(player)
sunlight_intensity = SUNLIGHT_INTENSITY

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

    if pygame.key.get_pressed()[pygame.K_PAGEUP]:
        if sunlight_intensity < SUNLIGHT_INTENSITY:
            sunlight_intensity += 1
    elif pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
        if sunlight_intensity > 0:
            sunlight_intensity -= 1

    player.movement(manager.doors)
    manager.paint(sunlight_intensity)
    manager.fps(clock)

    cursor.event_controller(events, manager.doors, player.scroll)
    cursor.paint(*pygame.mouse.get_pos(), screen)

    pygame.display.flip()
    clock.tick(FPS)
