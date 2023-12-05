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
        self.old_pos = (0, 0)
        self.speed = MOVEMENT_SPEED
        self.velocity_y = 0  # vert velocity

    def handle_movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.centerx -= self.speed
        elif keys[pg.K_d]:
            self.rect.centerx += self.speed
        if keys[pg.K_w]:
            self.rect.centery -= self.speed
        elif keys[pg.K_s]:
            self.rect.centery += self.speed

    def apply_gravity(self):
        # increase vertical velocity
        self.velocity_y += GRAVITY

        # update players position based on the vert velocity
        self.rect.y += self.velocity_y

    def update(self, game_map):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        self.apply_gravity()
        game_map.collide(self)

    def move_back(self):
        self.rect.x, self.rect.y = self.old_pos
        # reset vertical velocity when moving back
        self.velocity_y = 0