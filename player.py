# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

# Constants
MOVEMENT_SPEED = 5
GRAVITY = 0.5
class Portal(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

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
        if keys[pg.K_a]:
            self.rect.centerx -= 5
        elif keys[pg.K_d]:
            self.rect.centerx += 5
        if keys[pg.K_w]:
            self.rect.centery -= 5
        elif keys[pg.K_s]:
            self.rect.centery += 5


    def handle_portal(self, map, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
            pos[0], pos[1] = pos[0] - map.map_layer.get_center_offset()[0], pos[1] - map.map_layer.get_center_offset()[1]
            portal = Portal(self.image)
            portal.rect.center = pos
            map.group_add(portal)
            print(map.map_layer.get_center_offset())

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        #self.apply_gravity()