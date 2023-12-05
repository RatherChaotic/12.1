# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

# Constants
MOVEMENT_SPEED = 5
GRAVITY = 1  

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]
        self.speed = MOVEMENT_SPEED
        self.velocity_y = 0  # vert velocity

    def handle_movement(self):
        keys = pg.key.get_pressed()
        direction = pg.Vector2(0, 0)

        if keys[pg.K_a]:
            direction.x = -1
        elif keys[pg.K_d]:
            direction.x = 1
        if keys[pg.K_w]:
            direction.y = -1
        elif keys[pg.K_s]:
            direction.y = 1

        direction.normalize_ip()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        self.apply_gravity()