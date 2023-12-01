# Map Loading Files
# Created by https://github.com/RatherChaotic

import pygame as pg
import pytmx as tmx
import pyscroll as ps
class Map(object):
    def __init__(self):
        self.frame = None
        self.map_layer = None
        self.map_data = None
        self.tmx_data = None

    def load(self, filename):
        self.tmx_data = tmx.load_pygame(filename)
        self.map_data = ps.data.TiledMapData(self.tmx_data)
        self.map_layer = ps.BufferedRenderer(self.map_data, (pg.display.get_surface().get_width(), pg.display.get_surface().get_height()), clamp_camera=True)
        self.group = ps.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    def draw(self):
        self.group.center(pg.mouse.get_pos())
        self.group.draw(pg.display.get_surface())
        

    def update(self):
        self.draw()