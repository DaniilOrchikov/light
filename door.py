from numba import njit

from line_collider import LineCollider
from settings import *


@njit(fastmath=True, cache=True)
def generate_light_rect(x, y, x1, y1):
    light_rect = []
    light_rect.extend(
        [((int(i[0] // AVERAGE)) * AVERAGE, (int(i[1] // AVERAGE)) * AVERAGE) for i in line(x, y, int(x1), int(y1))])
    return list(set(light_rect))


@njit(fastmath=True, cache=True)
def line(x1, y1, x2, y2):
    arr = []
    dx, dy = x2 - x1, y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y, error, t = x1, y1, el / 2, 0
    arr.append((x, y))
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        arr.append((x, y))
    return arr


@njit(fastmath=True, cache=True)
def normal_angle(angle):
    while angle > math.pi * 2:
        angle -= math.pi * 2
    while angle < 0:
        angle += math.pi * 2
    angle = round(angle, 3)
    return angle


class Door:
    def __init__(self, x, y, direction):
        x = x // AVERAGE * AVERAGE
        y = y // AVERAGE * AVERAGE
        self.direction = {math.pi: '<', 0: '>', math.pi / 2: 'V', math.pi / 2 * 3: '^'}[direction]
        self.rect = None
        self.player_stop = False
        self.player = None
        self.light_rect = None
        self.x, self.y = x, y
        self.ANGLE = normal_angle(direction)
        self.angle = self.ANGLE
        self.length = 18 * 4 + 16
        self.m = True
        self.is_open = False
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y
        self.im = pygame.image.load('data/door.png').convert_alpha()
        self.width = 5
        self.line_collider = LineCollider(-math.cos(self.angle - math.pi / 2) * self.width + self.x,
                                          -math.sin(self.angle - math.pi / 2) * self.width + self.y,
                                          self.angle - math.pi / 2, self.length, self.width * 2)

        self.OPEN_COUNT = 50
        self.open_count = 0

        self.generate()

    def add_player(self, player):
        self.player = player

    def generate(self):
        self.light_rect = generate_light_rect(self.x, self.y, self.x1, self.y1)

        if not self.is_open or self.player_stop:
            self.get_rect()
        else:
            self.rect = None
        self.line_collider.regenerate(-math.cos(self.angle - math.pi / 2) * self.width + self.x,
                                      -math.sin(self.angle - math.pi / 2) * self.width + self.y,
                                      self.angle - math.pi / 2, self.length, self.width * 2)

    def get(self, arr):
        for i in self.light_rect:
            arr[i] = 1
        return arr

    def paint(self, sc, scroll):
        im = pygame.transform.rotate(self.im, math.degrees(self.angle) * -1)
        sc.blit(im, (self.x - scroll[0] - im.get_width() // 2, self.y - scroll[1] - im.get_height() // 2))
        # self.line_collider.paint(sc, scroll)

    def open(self):
        self.is_open = True
        self.open_count = self.OPEN_COUNT
        self.push()

    def close(self):
        if self.open_count < self.OPEN_COUNT / 4:
            self.open_count = 0
            self.is_open = False
            self.angle = self.ANGLE
            self.push()

    def push(self, right='None', top='None'):
        keys = pygame.key.get_pressed()
        speed = DOOR_PUSHING_ANGLE if not keys[pygame.K_LSHIFT] else DOOR_PUSHING_ANGLE_SHIFT
        self.angle = normal_angle(self.angle)
        if right != 'None' or top != 'None':
            self.open_count = 0
        if self.is_open:
            angle = 0
            if 0 <= self.angle < math.pi / 2 and (top == 'False' or right == 'False'):
                angle += speed
            elif 0 <= self.angle <= math.pi / 2 and (top == 'True' or right == 'True'):
                angle -= speed
            elif math.pi / 2 <= self.angle < math.pi and (right == 'False' or top == 'True'):
                angle += speed
            elif math.pi / 2 < self.angle <= math.pi and (right == 'True' or top == 'False'):
                angle -= speed
            elif math.pi <= self.angle < math.pi / 2 * 3 and (top == 'True' or right == 'True'):
                angle += speed
            elif math.pi < self.angle <= math.pi / 2 * 3 and (top == 'False' or right == 'False'):
                angle -= speed
            elif math.pi / 2 * 3 <= self.angle < math.pi * 2 and (right == 'True' or top == 'False'):
                angle += speed
            elif math.pi / 2 * 3 < self.angle <= math.pi * 2 and (right == 'False' or top == 'True'):
                angle -= speed
            if self.p_stop(angle):
                self.player_stop = True
                angle = 0
            else:
                self.player_stop = False
            self.angle += angle
        self.x1 = self.length * math.cos(self.angle) + self.x
        self.y1 = self.length * math.sin(self.angle) + self.y

    def get_rect(self):
        if not self.is_open:
            if self.direction == 'V':
                self.rect = pygame.Rect(self.x - 4, self.y, 8, self.length)
            elif self.direction == '^':
                self.rect = pygame.Rect(self.x1 - 4, self.y1, 8, self.length)
            elif self.direction == '>':
                self.rect = pygame.Rect(self.x, self.y - 4, self.length, 8)
            else:
                self.rect = pygame.Rect(self.x1, self.y1 - 4, self.length, 8)
        else:
            if self.direction in 'V^':
                if self.x > self.x1:
                    self.rect = pygame.Rect(self.x1, self.y1 - 4, self.length, 8)
                else:
                    self.rect = pygame.Rect(self.x, self.y - 4, self.length, 8)
            else:
                if self.y > self.y1:
                    self.rect = pygame.Rect(self.x1 - 4, self.y1, 8, self.length)
                else:
                    self.rect = pygame.Rect(self.x - 4, self.y, 8, self.length)

    def p_stop(self, angle):
        self.angle = normal_angle(self.angle)
        if self.direction == 'V':
            if angle > 0:
                return math.pi < self.angle < math.pi / 2 * 3
            return math.pi * 2 > self.angle > math.pi / 2 * 3
        if self.direction == '^':
            if angle > 0:
                return 0 < self.angle < math.pi / 2
            return math.pi + 0.1 > self.angle > math.pi / 2
        if self.direction == '>':
            if angle > 0:
                return math.pi / 2 < self.angle < math.pi
            return math.pi / 2 * 3 > self.angle > math.pi
        if angle > 0:
            return math.pi / 2 * 3 < self.angle < math.pi * 2
        return math.pi / 2 > self.angle > 0

    def move(self):
        self.angle = normal_angle(self.angle)
        if self.open_count:
            self.open_count -= 1
            if self.direction == '>':
                if self.y1 <= self.player.rect.y:
                    self.angle -= math.pi / 4 / self.OPEN_COUNT
                else:
                    self.angle += math.pi / 4 / self.OPEN_COUNT
            elif self.direction == '<':
                if self.y1 <= self.player.rect.y:
                    self.angle += math.pi / 4 / self.OPEN_COUNT
                else:
                    self.angle -= math.pi / 4 / self.OPEN_COUNT
            elif self.direction == 'V':
                if self.x1 < self.player.rect.x:
                    self.angle += math.pi / 4 / self.OPEN_COUNT
                else:
                    self.angle -= math.pi / 4 / self.OPEN_COUNT
            else:
                if self.x1 < self.player.rect.x:
                    self.angle -= math.pi / 4 / self.OPEN_COUNT
                else:
                    self.angle += math.pi / 4 / self.OPEN_COUNT
            self.push()
        self.generate()
