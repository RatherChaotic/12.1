# Game File
# Created by https://github.com/RatherChaotic

import map
import player
import pygame as pg

class Game(object):
    def __init__(self):
        self.map = map.Map()
        self.player = player.Player()
        self.map.load("assets/map1.tmx")

    def update(self):
        self.map.update(self.player)
        self.player.update(self.map)

    def draw(self):
        self.map.draw(self.player)

