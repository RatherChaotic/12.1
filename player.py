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

    def handle_movement(self, map):
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
        keys = pg.get.key.pressed
        if keys[pg.K_a] and not map.collide(self):
            self.rect.centerx -= 5
        elif keys[pg.K_d] and not map.collide(self):
            self.rect.centerx += 5
        else:
            self.move_back("x")
        if keys[pg.K_w] and not map.collide(self):
            self.rect.centery -= 5
        elif keys[pg.K_s] and not map.collide(self):
            self.rect.centery += 5
        elif map.collide(self):
            self.move_back("y")
    def update(self, game_map):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        self.apply_gravity()
        game_map.collide(self)
        self.handle_movement(map)

    def move_back(self, mode):
        if mode == "x":
            self.rect.x = self.old_pos[0]
        elif mode == "y":
            self.rect.y = self.old_pos[1]