class Physics:
    def __init__(self, map):
        self.map = map

    def collision_test(self, rect):
        for i in self.map:
            if i.rect.colliderect(rect):
                return i
        return None

    def movement(self, rect, move):
        collisions = {'right': False, 'left': False, 'top': False, 'bottom': False}
        if move[0] != 0:
            rect.x += move[0]
            collision_tile = self.collision_test(rect)
            if collision_tile:
                if move[0] > 0:
                    collisions['right'] = True
                    rect.right = collision_tile.rect.left
                else:
                    collisions['left'] = True
                    rect.left = collision_tile.rect.right
        if move[1] != 0:
            rect.y += move[1]
            collision_tile = self.collision_test(rect)
            if collision_tile:
                if move[1] > 0:
                    collisions['bottom'] = True
                    rect.bottom = collision_tile.rect.top
                else:
                    collisions['top'] = True
                    rect.top = collision_tile.rect.bottom
        return collisions
