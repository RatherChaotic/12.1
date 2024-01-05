import pygame as pg
import map


class Cube(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]
        self.velocity = [0, 0]
        self.gravity = True

    def collide_with(self, object_rect):
        if object_rect.colliderect(self.rect):
            if self.old_pos[1] + 20 <= object_rect.y:
                self.rect.bottom = object_rect.y
                self.gravity = False
                if self.velocity[1] > 0:
                    self.velocity[1] = 0
                if self.velocity[0] < 0:
                    self.velocity[0] += 1
                elif self.velocity[0] > 0:
                    self.velocity[0] -= 1
            elif self.old_pos[1] + 20 >= object_rect.y + object_rect.height:
                self.rect.top = object_rect.y + object_rect.height
                self.gravity = True
            elif self.rect.left < object_rect.left:
                self.rect.right = object_rect.left
                self.gravity = True
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

            else:
                self.rect.left = object_rect.right
                self.gravity = True
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
        else:
            self.gravity = True
    def handle_physics(self, map):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

        collider_Rect = map.get_layer_as_rect("collision")
        self.collide_with(collider_Rect)
        if self.gravity:
            self.velocity[1] += 0.3

    def handle_movement(self, map):
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.rect.centerx, self.rect.centery = pg.mouse.get_pos()[0] - map.map_layer.get_center_offset()[0], pg.mouse.get_pos()[1] - map.map_layer.get_center_offset()[1]
            self.velocity[1] = 0

    def update(self, map):
        self.handle_physics(map)
        self.handle_movement(map)