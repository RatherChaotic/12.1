# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image =image
        self.rect = self.image.get_rect()


    def handle_movement(self, map):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and map.collide(self.rect):
            self.rect.x -= 5
        elif keys[pg.K_d] and map.collide(self.rect):
            self.rect.x += 5
        if keys[pg.K_w] and map.collide(self.rect):
            self.rect.y -= 5
        elif keys[pg.K_s] and map.collide(self.rect):
            self.rect.y += 5