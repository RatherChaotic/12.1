import pygame as pg
import map, player, misc

misc = misc.Misc()


class Cube(pg.sprite.Sprite):
    def __init__(self, image):
        """Initialize the object with the given image."""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.old_pos = [0, 0]
        self.velocity = [0, 0]
        self.teleported = False
        self.gravity = True
        self.disabled = False

    def collide_with(self, object_rect):
        print("Current Position before Collision:", self.rect.topleft)

        """
        Check for collision with an object and update the position accordingly.

        Args:
            object_rect (Rect): The rectangle of the object to check collision with.
        """
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y:
            # Colliding from top
            self.rect.bottom = object_rect.y
            self.gravity = False
            if self.velocity[1] > 0:
                self.velocity[1] = 0
            if self.velocity[0] < 0:
                self.velocity[0] += 1
            elif self.velocity[0] > 0:
                self.velocity[0] -= 1
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height:
            # Colliding from bottom
            self.rect.top = object_rect.y + object_rect.height
            self.gravity = False
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left:
            # Colliding from left
            self.rect.right = object_rect.left
            self.gravity = True
            if self.velocity[0] > 0:
                self.velocity[0] = 0
        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:
            # Colliding from right
            self.rect.left = object_rect.right
            self.gravity = True
            if self.velocity[0] < 0:
                self.velocity[0] = 0
        else:
            # No collision
            self.gravity = True

        # Add debugging print statements
        #print("New Position after Collision:", self.rect.topleft)
        #print("Velocity after Collision:", self.velocity)

    def portal_collision(self, player):
        """
        Checks for collision between the player and portals, and handles teleportation.
        """

        # Check if the player collides with portal 0 and both portals are active
        if self.rect.colliderect(player.portals[0].rect) and not self.teleported and (
                player.portals[1].active and player.portals[0].active):
            self.teleported = True
            self.rect.center = player.portals[1].rect.center

        # Check if the player collides with portal 1 and both portals are active
        elif self.rect.colliderect(player.portals[1].rect) and not self.teleported and (
                player.portals[1].active and player.portals[0].active):
            self.teleported = True
            self.rect.center = player.portals[0].rect.center

        # Reset teleportation flag if player is not colliding with any portals
        elif not self.rect.colliderect(player.portals[1].rect) and not self.rect.colliderect(player.portals[0].rect):
            self.teleported = False

    def handle_physics(self, player):
        """
        Update the position of the object based on its velocity and handle collisions with portals.

        Args:
            player (Player): The player object.
        """
        # Update the x and y coordinates of the object's center based on its velocity
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

        # Check for collision with portals
        self.portal_collision(player)

        # Apply gravity to the object's velocity if enabled
        if self.gravity:
            self.velocity[1] += 0.3

    def update(self, player):
        """
        Update the game state by handling physics for the player.

        Args:
            player: The player object to update.
        """
        self.handle_physics(player)
