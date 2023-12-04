# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image =image
        self.rect = self.image.get_rect()

