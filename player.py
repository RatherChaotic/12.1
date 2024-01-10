# Player Loading File
# Created by https://github.com/RatherChaotic

import pygame as pg
import map

# Constants
MOVEMENT_SPEED = 3
GRAVITY = 0.3
class Portal(pg.sprite.Sprite):
    def __init__(self, images, id):
        """
        Initialize the object with a list of images and an ID.

        Parameters:
        - images: list of images
        - id: the ID of the object
        """
        super().__init__()

        # Set the list of images
        self.images = images

        # Set the initial image index
        self.image_index = 0

        # Set the initial image
        self.image = self.images[self.image_index]

        # Get the rectangle of the image
        self.rect = self.image.get_rect()

        # Set the ID of the object
        self.ident = id

        # Set the created flag to False
        self.created = False

        # Set the active flag to False
        self.active = False

        # Set the animation speed to 5
        self.animation_speed = 5

        # Set the animation counter to 0
        self.animation_counter = 0

    def update_animation(self):
        """
        Update the animation by incrementing the animation counter and changing the image if necessary.
        """

        # Increment the animation counter
        self.animation_counter += 1

        # Check if it's time to change the image
        if self.animation_counter % self.animation_speed == 0:
            if self.image_index == 0:
                # Change the image index
                self.image_index = (self.image_index + 1) % len(self.images)

            # Update the image
            self.image = self.images[self.image_index]



class Player(pg.sprite.Sprite):
    def __init__(self, right_idle_images, left_idle_images, move_right_images, move_left_images, scale_factor=0.75):
        """
        Initialize the object with the given parameters.

        Args:
            right_idle_images (list): List of images for idle animation when facing right.
            left_idle_images (list): List of images for idle animation when facing left.
            move_right_images (list): List of images for movement animation when moving right.
            move_left_images (list): List of images for movement animation when moving left.
            scale_factor (float, optional): Scale factor for resizing the images. Defaults to 0.75.
        """

        super().__init__()

        # Scale the images and store them in respective attributes
        self.right_idle_images = [
            pg.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img
            in right_idle_images]
        self.left_idle_images = [
            pg.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img
            in left_idle_images]
        self.move_right_images = [
            pg.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img
            in move_right_images]
        self.move_left_images = [
            pg.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))) for img
            in move_left_images]

        self.animation_speed = 10
        self.animation_counter = 0

        self.scale_factor = scale_factor

        # Set initial images and rect
        self.image = self.right_idle_images[0]
        self.rect = self.image.get_rect()

        self.old_pos = [0, 0]
        self.speed = MOVEMENT_SPEED
        self.velocity_y = 0  # vertical velocity
        self.velocity_x = 0  # horizontal velocity
        self.gravity = True

        # Initialize portal images
        portal_b_images = [pg.image.load("assets/portal_b_0.png").convert_alpha(),
                           pg.image.load("assets/portal_b_1.png").convert_alpha()]
        portal_o_images = [pg.image.load("assets/portal_o_0.png").convert_alpha(),
                           pg.image.load("assets/portal_o_1.png").convert_alpha()]

        # Create portal objects
        self.portal_b = Portal(portal_b_images, 0)
        self.portal_o = Portal(portal_o_images, 1)

        self.teleported = False

        # Store the portal objects in a list
        self.portals = [self.portal_b, self.portal_o]

    def update_animation(self):
        """
        Update the animation of the player character.
        """
        # Increment the animation counter
        self.animation_counter += 1

        # Check if it's time to update the animation
        if self.animation_counter % self.animation_speed == 0:
            # Determine which image to display based on the direction of movement
            if self.velocity_x > 0:
                image_to_display = self.move_right_images[self.animation_counter % len(self.move_right_images)]
            elif self.velocity_x < 0:
                image_to_display = self.move_left_images[self.animation_counter % len(self.move_left_images)]
            else:
                # Adjust idle animation based on facing direction
                if self.image == self.right_idle_images[0]:
                    image_to_display = self.right_idle_images[self.animation_counter % len(self.right_idle_images)]
                else:
                    image_to_display = self.left_idle_images[self.animation_counter % len(self.left_idle_images)]

            # Apply scaling to the player's image
            scaled_image = pg.transform.scale(image_to_display, (int(image_to_display.get_width() * self.scale_factor),
                                                                 int(image_to_display.get_height() * self.scale_factor)))

            # Update the player's rect dimensions
            self.rect.size = scaled_image.get_size()

            # Assign the scaled image to self.image
            self.image = scaled_image

    def handle_movement(self):
        """
        Handles the movement of the character based on the pressed keys.
        """
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            # Move left if velocity_x is not already at its minimum
            if not self.velocity_x <= -5:
                self.velocity_x -= MOVEMENT_SPEED

        elif keys[pg.K_d]:
            # Move right if velocity_x is not already at its maximum
            if not self.velocity_x >= 5:
                self.velocity_x += MOVEMENT_SPEED

        if keys[pg.K_w]:
            # Jump if velocity_y is 0 and not already at its minimum
            if self.velocity_y == 0:
                if not self.velocity_y <= -5:
                    self.velocity_y -= MOVEMENT_SPEED * 2

    def handle_portal(self, map, event):
        """
        Handle portal events.

        Args:
            map (Map): The map object.
            event (Event): The event object.

        Returns:
            None
        """

        # Get the mouse position
        pos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]

        # Adjust the position based on the map's center offset
        pos[0], pos[1] = pos[0] - map.map_layer.get_center_offset()[0], pos[1] - map.map_layer.get_center_offset()[1]

        # Handle left mouse button click event
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.reset_portal()
            self.portals[0].rect.centerx, self.portals[0].rect.centery = pos
            map.group_add(self.portals[0])
            self.portals[0].active = True

        # Handle right mouse button click event
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.reset_portal()
            self.portals[1].rect.centerx, self.portals[1].rect.centery = pos
            map.group_add(self.portals[1])
            self.portals[1].active = True

        # Handle 'r' key press event
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
            # Deactivate all portals and reset their positions
            for portal in self.portals:
                portal.active = False
                map.group_pop(portal)
                portal.rect.center = [-100, 0]

    def reset_portal(self):
        """
        Resets the portals by setting the image to the first image in the images list
        and resetting the animation counter to 0.
        """
        for portal in self.portals:
            portal.image = portal.images[0]
            portal.animation_counter = 0

    def update_portal(self):
        """
        Update the portals in the game.

        This function iterates over all the portals in the `portals` list and updates their animation.
        If a portal is not active, it calls the `reset_portal()` method.

        Parameters:
        - self: The current instance of the class.

        Returns:
        - None
        """
        for portal in self.portals:
            if portal.active:
                portal.update_animation()
            else:
                self.reset_portal()

    def portal_collision(self):
        """
        Check for collision with portals and handle teleportation.

        If the player collides with an active portal and has not been teleported
        already, teleport the player to the other active portal. Set the
        'teleported' flag to True to prevent continuous teleportation.

        If the player does not collide with any portal, reset the 'teleported'
        flag to False.

        Args:
            self (Player): The player object.

        Returns:
            None
        """
        if (
                self.portals[0].rect.colliderect(self.rect)
                and not self.teleported
                and (self.portals[1].active and self.portals[0].active)
        ):
            self.rect.center = self.portals[1].rect.center
            self.teleported = True
        elif (
                self.portals[1].rect.colliderect(self.rect)
                and not self.teleported
                and (self.portals[1].active and self.portals[0].active)
        ):
            self.rect.center = self.portals[0].rect.center
            self.teleported = True
        elif (
                not self.portals[1].rect.colliderect(self.rect)
                and not self.portals[0].rect.colliderect(self.rect)
        ):
            self.teleported = False

    def apply_gravity(self):
        """
        Apply gravity to the object's velocity in the y-axis.
        """
        # Update the y-velocity by adding the constant GRAVITY
        self.velocity_y += GRAVITY

    def collide_with(self, object_rect):
        """
        Check for collision with an object and update the position accordingly.

        Args:
            object_rect (Rect): The rectangle of the object to check collision with.
        """
        if object_rect.colliderect(self.rect) and self.old_pos[1] <= object_rect.y:
            # Colliding from top
            self.rect.bottom = object_rect.y
            self.gravity = False
            if self.velocity_y > 0:
                self.velocity_y = 0
            if self.velocity_x < 0:
                self.velocity_x += 1
            elif self.velocity_x > 0:
                self.velocity_x -= 1
        elif object_rect.colliderect(self.rect) and self.old_pos[1] >= object_rect.y + object_rect.height:
            # Colliding from bottom
            self.rect.top = object_rect.y + object_rect.height
            self.gravity = False
        elif object_rect.colliderect(self.rect) and self.rect.left < object_rect.left:
            # Colliding from left
            self.rect.right = object_rect.left
            self.gravity = True
            if self.velocity_x > 0:
                self.velocity_x = 0
        elif object_rect.colliderect(self.rect) and self.rect.right > object_rect.right:
            # Colliding from right
            self.rect.left = object_rect.right
            self.gravity = True
            if self.velocity_x < 0:
                self.velocity_x = 0
        else:
            # No collision
            self.gravity = True

    def update(self):
        """
        Update the state of the object.
        """
        # Save the current position
        self.old_pos = self.rect.x, self.rect.y

        # Check for collision with portals
        self.portal_collision()

        # Handle movement based on velocity
        self.handle_movement()

        # Update the state of the portals
        self.update_portal()

        # Update the vertical position
        self.rect.centery += self.velocity_y

        # Update the horizontal position
        self.rect.centerx += self.velocity_x

        # Apply gravity if enabled
        if self.gravity:
            self.apply_gravity()

        # Update the animation
        self.update_animation()
