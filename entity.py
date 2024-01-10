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

    def collide_with(self, object_rect):
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y + 10:
            # Handle top collision
            self.gravity = False
            self.rect.bottom = object_rect.y
            if self.velocity[1] > 0:
                self.velocity[1] = 0
            if self.velocity[0] < 0:
                self.velocity[0] += 1
            elif self.velocity[0] > 0:
                self.velocity[0] -= 1
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height - 10 and not (self.old_pos[1] <= object_rect.y + 10):
            # Handle bottom collision
            self.rect.top = object_rect.y + object_rect.height
            self.gravity = True
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left and not (self.old_pos[1] <= object_rect.y + 10):
            # Handle left collision
            self.rect.right = object_rect.left + 1  # Adjusted the position by adding 1
            if self.velocity[0] > 0:
                self.velocity[0] = 0
            self.gravity = True
        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:
            # Handle right collision
            self.rect.left = object_rect.right
            if self.velocity[0] < 0:
                self.velocity[0] = 0
            self.gravity = True
        elif self.gravity is False:
            self.gravity = True

        # Add debugging print statements
        print("New Position after Collision:", self.rect.topleft)
        print("Velocity after Collision:", self.velocity)

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
