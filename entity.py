import pygame as pg
import map, player, misc

misc = misc.Misc()


class Cube(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]
        self.velocity = [0, 0]
        self.teleported = False
        self.gravity = True
        self.disabled = False

    def collide_with(self, object_rect):
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y:
            self.gravity = False
            self.rect.bottom = object_rect.y
            if self.velocity[1] > 0:
                self.velocity[1] = 0
            if self.velocity[0] < 0:
                self.velocity[0] += 1
            elif self.velocity[0] > 0:
                self.velocity[0] -= 1
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height:

            self.gravity = False
            self.rect.top = object_rect.y + object_rect.height
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left:

            self.gravity = True
            self.rect.right = object_rect.left
            if self.velocity[0] > 0:
                self.velocity[0] = 0

        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:

            self.gravity = True
            self.rect.left = object_rect.right
            if self.velocity[0] < 0:
                self.velocity[0] = 0
        else:
            self.gravity = True

    def portal_collision(self, player):
        if self.rect.colliderect(player.portals[0].rect) and not self.teleported and (
                player.portals[1].active and player.portals[0].active):
            self.teleported = True
            self.rect.center = player.portals[1].rect.center
        elif self.rect.colliderect(player.portals[1].rect) and not self.teleported and (
                player.portals[1].active and player.portals[0].active):
            self.teleported = True
            self.rect.center = player.portals[0].rect.center
        elif not self.rect.colliderect(player.portals[1].rect) and not self.rect.colliderect(player.portals[0].rect):
            self.teleported = False

    def handle_physics(self, player):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]
        self.portal_collision(player)
        if self.gravity:
            self.velocity[1] += 0.3

    def update(self, player):
        self.handle_physics(player)
