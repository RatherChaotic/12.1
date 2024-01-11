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
        Handle collision between self and object_rect.

        Args:
            object_rect: The rectangle representing the object to collide with.

        """
        # Check if self collides with object_rect and is above it
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y:
            # Handle top collision
            self.gravity = False
            self.rect.bottom = object_rect.y
            # Stop vertical velocity
            if self.velocity[1] > 0:
                self.velocity[1] = 0
            # Slow down horizontal velocity
            if self.velocity[0] < 0:
                self.velocity[0] += 1
            elif self.velocity[0] > 0:
                self.velocity[0] -= 1

        # Check if self collides with object_rect and is below it
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height:
            self.gravity = False
            # Handle bottom collision
            self.rect.top = object_rect.y + object_rect.height

        # Check if self collides with object_rect and is to the left of it
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left:
            self.gravity = True
            # Handle left collision
            self.rect.right = object_rect.left + 1  # Adjusted the position by adding 1            # Stop horizontal velocity
            if self.velocity[0] > 0:
                self.velocity[0] = 0

        # Check if self collides with object_rect and is to the right of it
        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:
            self.gravity = True
            # Handle right collision
            self.rect.left = object_rect.right
            # Stop horizontal velocity
            if self.velocity[0] < 0:
                self.velocity[0] = 0

        # No collision, gravity is active
        else:
            self.gravity = True

        # Add debugging print statements
        print("New Position after Collision:", self.rect.topleft)
        print("Velocity after Collision:", self.velocity)

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
