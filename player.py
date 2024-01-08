# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

# Constants
MOVEMENT_SPEED = 3
GRAVITY = 0.3
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
            if self.image_index == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]



class Player(pg.sprite.Sprite):
    def __init__(self, right_idle_images, left_idle_images, move_right_images, move_left_images):
        super().__init__()
        self.right_idle_images = right_idle_images
        self.left_idle_images = left_idle_images
        self.move_right_images = move_right_images
        self.move_left_images = move_left_images

        self.animation_speed = 5
        self.animation_counter = 0

        # Set initial images and rect
        self.image = self.right_idle_images[0] 
        self.rect = self.image.get_rect()

        self.old_pos = [0, 0]
        self.speed = MOVEMENT_SPEED
        self.velocity_y = 0  # vert velocity
        self.velocity_x = 0  # horiz velocity
        self.gravity = True
        portal_b_images = [pg.image.load("assets/portal_b_0.png").convert_alpha(), pg.image.load("assets/portal_b_1.png").convert_alpha()]
        portal_o_images = [pg.image.load("assets/portal_o_0.png").convert_alpha(), pg.image.load("assets/portal_o_1.png").convert_alpha()]
        self.portal_b = Portal(portal_b_images, 0)
        self.portal_o = Portal(portal_o_images, 1)
        self.portals = [self.portal_b, self.portal_o]

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter % self.animation_speed == 0:
            if self.velocity_x > 0:
                self.image = self.move_right_images[self.animation_counter % len(self.move_right_images)]
            elif self.velocity_x < 0:
                self.image = self.move_left_images[self.animation_counter % len(self.move_left_images)]
            else:
                # Adjust idle animation based on facing direction
                if self.image == self.right_idle_images[0]:
                    self.image = self.right_idle_images[self.animation_counter % len(self.right_idle_images)]
                else:
                    self.image = self.left_idle_images[self.animation_counter % len(self.left_idle_images)]

    def handle_movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            if not self.velocity_x <= -5:
                self.velocity_x -= MOVEMENT_SPEED
        elif keys[pg.K_d]:
            if not self.velocity_x >= 5:
                self.velocity_x += MOVEMENT_SPEED
        if keys[pg.K_w]:
            if self.velocity_y == 0:
                if not self.velocity_y <= -5:
                    self.velocity_y -= MOVEMENT_SPEED * 2


    def handle_portal(self, map, event):
        pos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
        pos[0], pos[1] = pos[0] - map.map_layer.get_center_offset()[0], pos[1] - map.map_layer.get_center_offset()[1]
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.reset_portal()
            self.portals[0].rect.centerx, self.portals[0].rect.centery = pos
            map.group_add(self.portals[0])
            self.portals[0].active = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.reset_portal()
            self.portals[1].rect.centerx, self.portals[1].rect.centery = pos
            map.group_add(self.portals[1])
            self.portals[1].active = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            for portal in self.portals:
                portal.active = False
                map.group_pop(portal)
                portal.rect.center = [-100, 0]

    def reset_portal(self):
        for portal in self.portals:
            portal.image = portal.images[0]
            portal.animation_counter = 0

    def update_portal(self):
        for portal in self.portals:
            if portal.active:
                portal.update_animation()
            else:
                self.reset_portal()

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

    def collide_with(self, object_rect):
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y:
            self.rect.bottom = object_rect.y
            self.gravity = False
            if self.velocity_y > 0:
                self.velocity_y = 0
            if self.velocity_x < 0:
                self.velocity_x += 1
            elif self.velocity_x > 0:
                self.velocity_x -= 1
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height:
            self.rect.top = object_rect.y + object_rect.height
            self.gravity = True
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left:
            self.rect.right = object_rect.left
            self.gravity = True
            if self.velocity_x > 0:
                self.velocity_x = 0

        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:
            self.rect.left = object_rect.right
            self.gravity = True
            if self.velocity_x < 0:
                self.velocity_x = 0
        else:
            self.gravity = True

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        self.portal_collision()
        self.handle_movement()
        self.update_portal()
        self.rect.centery += self.velocity_y
        self.rect.centerx += self.velocity_x
        if self.gravity:
            self.apply_gravity()
        self.update_animation()