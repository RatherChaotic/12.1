# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]

    def handle_movement(self, map):
        keys = pg.key.get_pressed()
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
    def update(self, map):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement(map)

    def move_back(self, mode):
        if mode == "x":
            self.rect.x = self.old_pos[0]
        elif mode == "y":
            self.rect.y = self.old_pos[1]