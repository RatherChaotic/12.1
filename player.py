# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

# Constants
MOVEMENT_SPEED = 5
GRAVITY = 0.2
class Portal(pg.sprite.Sprite):
    def __init__(self, images, id):
        super().__init__()
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.ident = id
        self.created = False
        self.active = False
        self.teleported = False
        self.animation_speed = 5 
        self.animation_counter = 0

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter % self.animation_speed == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def update_portal(self):
        self.update_animation()
        for portal in self.portals:
            portal.update_portal()

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]
        self.speed = MOVEMENT_SPEED
        self.velocity_y = -2  # vert velocity
        portal_b_images = [pg.image.load("assets/portal_b_0.png","assets/portal_b_1.png").convert_alpha()]
        portal_o_images = [pg.image.load("assets/portal_o_0.png", "assets/portal_o_1.png").convert_alpha()]
        self.portal_b = Portal(portal_b_images, 0)
        self.portal_o = Portal(portal_o_images, 1)
        self.portals = [self.portal_b, self.portal_o]

    def handle_movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.centerx -= 5
        elif keys[pg.K_d]:
            self.rect.centerx += 5
        if keys[pg.K_w]:
            self.rect.centery -= 5


    def handle_portal(self, map, event):
        pos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
        pos[0], pos[1] = pos[0] - map.map_layer.get_center_offset()[0], pos[1] - map.map_layer.get_center_offset()[1]
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.portals[0].rect.centerx, self.portals[0].rect.centery = pos
            map.group_add(self.portals[0])
            self.portals[0].active = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.portals[1].rect.centerx, self.portals[1].rect.centery = pos
            map.group_add(self.portals[1])
            self.portals[1].active = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            for portal in self.portals:
                portal.active = False
                map.group_pop(portal)
                portal.rect.center = [-100, 0]

    def portal_collision(self):
            if self.portals[0].rect.colliderect(self.rect) and not self.portals[1].teleported and (self.portals[1].active and self.portals[0].active):
                self.rect.center = self.portals[1].rect.center
                self.portals[0].teleported = True
            elif self.portals[1].rect.colliderect(self.rect) and not self.portals[0].teleported and (self.portals[1].active and self.portals[0].active):
                self.rect.center = self.portals[0].rect.center
                self.portals[1].teleported = True
            elif not self.portals[1].rect.colliderect(self.rect) and not self.portals[0].rect.colliderect(self.rect):
                self.portals[0].teleported = False
                self.portals[1].teleported = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        self.handle_movement()
        self.portal_collision()
        self.apply_gravity()