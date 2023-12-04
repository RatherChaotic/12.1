# Map Loading Files
# Created by https://github.com/RatherChaotic

import pygame as pg
import pytmx as tmx
import pyscroll as ps


# Initialize Class
class Map(object):
    def __init__(self):
        self.frame = None
        self.map_layer = None
        self.map_data = None
        self.tmx_data = None

    # Load the map files and initialize the pyscroller
    def load(self, filename):
        self.tmx_data = tmx.load_pygame(filename)
        self.map_data = ps.data.TiledMapData(self.tmx_data)
        self.map_layer = ps.BufferedRenderer(self.map_data, (
            pg.display.get_surface().get_width(), pg.display.get_surface().get_height()), clamp_camera=True)
        self.group = ps.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    # Draw the map
    def draw(self, center):
        self.group.center(center)
        self.group.draw(pg.display.get_surface())

    def group_add(self, addition):
        self.group.add(addition)

    # Check for collisions
    def collide(self, player):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, tmx.TiledObjectGroup):
                if layer.name == "collision":
                    for obj in layer:
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        if rect.colliderect(player.rect):
                            player.move_back()


    def update(self, center):
        self.draw(center)
