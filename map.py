# Map Loading Files
# Created by https://github.com/RatherChaotic

import pygame as pg
import pytmx as tmx
import pyscroll as ps

class Map(object):
    def __init__(self, width, height):  # Accept width and height as arguments
        self.frame = None
        self.map_layer = None
        self.map_data = None
        self.tmx_data = None
        self.width = width  # Store width as an attribute
        self.height = height  # Store height as an attribute

    def load(self, filename):
        self.tmx_data = tmx.load_pygame(filename)
        self.map_data = ps.data.TiledMapData(self.tmx_data)
        self.map_layer = ps.BufferedRenderer(self.map_data, (
            pg.display.get_surface().get_width(), pg.display.get_surface().get_height()), clamp_camera=True)
        self.group = ps.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    def draw(self, center):
        self.group.center(center)
        self.group.draw(pg.display.get_surface())

    def group_add(self, addition):
        self.group.add(addition)

    def collide(self, player):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, tmx.TiledObjectGroup):
                if layer.name == "collision":
                    for obj in layer:
                        rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        if rect.colliderect(player.rect):
                            if player.old_pos[1]+20 <= obj.y:
                                player.rect.bottom = obj.y
                                player.velocity_y = 0
                            elif player.rect.left < rect.left:
                                player.rect.right = rect.left
                            else:
                                player.rect.left = rect.right

    def update(self, center):
        self.draw(center)