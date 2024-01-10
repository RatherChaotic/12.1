# Map Loading Files
# Created by https://github.com/RatherChaotic

import pygame as pg
import pytmx as tmx
import pyscroll as ps


class Map(object):
    def __init__(self, width, height):
        """
        Initialize the class with the given width and height.

        Args:
            width (int): The width of the frame.
            height (int): The height of the frame.
        """
        self.frame = None  # Initialize the frame attribute
        self.map_layer = None  # Initialize the map_layer attribute
        self.map_data = None  # Initialize the map_data attribute
        self.tmx_data = None  # Initialize the tmx_data attribute
        self.width = width  # Store the width as an attribute
        self.height = height  # Store the height as an attribute
        self.level_index = 0  # Initialize the level_index attribute

    def load(self, filename):
        """
        Load the TiledMapData from a file.

        Args:
            filename (str): The path to the Tiled map file.

        Returns:
            None
        """
        # Load the Tiled map data using the pygame module
        self.tmx_data = tmx.load_pygame(filename)

        # Create a TiledMapData object from the tmx data
        self.map_data = ps.data.TiledMapData(self.tmx_data)

        # Create a BufferedRenderer object for rendering the map
        # Use the dimensions of the display surface as the buffer size
        buffer_size = (pg.display.get_surface().get_width(), pg.display.get_surface().get_height())
        self.map_layer = ps.BufferedRenderer(self.map_data, buffer_size, clamp_camera=True)

        # Create a PyscrollGroup object for managing sprites on the map
        # Set the map layer as the map_layer parameter and default_layer as 4
        self.group = ps.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    def draw(self, center):
        """
        Draw the group at the specified center position on the display surface.

        Args:
            center: A tuple representing the center position of the group.

        Returns:
            None
        """
        # Set the center of the group
        self.group.center(center)

        # Draw the group on the display surface
        self.group.draw(pg.display.get_surface())

    def group_add(self, addition):
        """
        Add an element to the group.

        Args:
            addition: The element to be added to the group.
        """
        self.group.add(addition)

    def group_pop(self, removal):
        """
        Remove an element from the group.

        Args:
            removal: The element to be removed from the group.
        """
        self.group.remove(removal)

    def collide(self, entity):
        """
        Detects collision between the entity and the collision objects in the map.

        Args:
            entity (Entity): The entity to check for collision.
        """
        # Iterate through the visible layers in the map
        for layer in self.tmx_data.visible_layers:
            # Check if the layer is an object group
            if isinstance(layer, tmx.TiledObjectGroup):
                # Check if the object group is named "collision"
                if layer.name == "collision":
                    # Iterate through each object in the object group
                    for obj in layer:
                        # Create a rectangle representing the object's position and size
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        # Call the entity's collide_with() method to handle the collision
                        entity.collide_with(rect)

    def get_layer_as_rect(self, layer_name):
        """
        Get the layer as a rectangle object based on the given layer name.

        Args:
            layer_name (str): The name of the layer to retrieve.

        Returns:
            pg.Rect: The rectangle object representing the layer.

        Raises:
            ValueError: If the layer with the given name is not found.
        """
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, tmx.TiledObjectGroup):
                if layer.name == layer_name:
                    for obj in layer:
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        return rect
        raise ValueError(f"No layer found with name {layer_name}")

    def get_layer(self, layer_name):
        """
        Retrieve a layer by its name from the Tiled map.

        Args:
            layer_name (str): The name of the layer to retrieve.

        Returns:
            tmx.TiledObjectGroup or None: The layer with the specified name, or None if it is not found.
        """
        # Iterate over all visible layers in the Tiled map
        for layer in self.tmx_data.visible_layers:
            # Check if the layer is an object group
            if isinstance(layer, tmx.TiledObjectGroup):
                # Check if the layer name matches the desired name
                if layer.name == layer_name:
                    return layer
        return None

    def update(self, center):
        """
        Update the object's position and redraw it.

        Args:
            center (tuple): The new center coordinates of the object.

        Returns:
            None
        """
        self.draw(center)