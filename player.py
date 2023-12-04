# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = (0, 0)

    def handle_movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.centerx -= 5
        elif keys[pg.K_d]:
            self.rect.centerx += 5
        if keys[pg.K_w]:
            self.rect.centery -= 5
        elif keys[pg.K_s]:
            self.rect.centery += 5

    def update(self, map):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        map.collide(self)

    def move_back(self):
        self.rect.x, self.rect.y = self.old_pos