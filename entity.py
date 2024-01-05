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

    def handle_physics(self, map):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

        collider_Rect = map.get_layer_as_rect("collision")
        if self.rect.colliderect(collider_Rect):
            if self.old_pos[1] + 20 <= collider_Rect.y:
                self.rect.bottom = collider_Rect.y
                self.gravity = False
                if self.velocity[1] > 0:
                    self.velocity[1] = 0
                if self.velocity[0] < 0:
                    self.velocity[0] += 1
                elif self.velocity[0] > 0:
                    self.velocity[0] -= 1
            elif self.old_pos[1] + 20 >= collider_Rect.y + collider_Rect.height:
                self.rect.top = collider_Rect.y + collider_Rect.height
                self.gravity = True
            elif self.rect.left < collider_Rect.left:
                self.rect.right = collider_Rect.left
                self.gravity = True
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

            else:
                self.rect.left = collider_Rect.right
                self.gravity = True
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
        else:
            self.gravity = True
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