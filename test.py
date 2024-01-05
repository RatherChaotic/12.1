import sys

import pygame as pg

import entity
import map
import player

pg.init()
display = pg.display.set_mode((512, 512), pg.SCALED | pg.RESIZABLE)
map = map.Map(510, 510)
map.load("assets/maps/flat.tmx")
player = player.Player(pg.image.load("assets/player.png"))
cube = entity.Cube(pg.image.load("assets/cube.png"))
FPS = 60
clock = pg.time.Clock()
levels = ["assets/maps/flat.tmx", "assets/maps/map1.tmx"]
entity_list = [player, cube]


def load_map(file_name):
    map.load(file_name)



while True:
    for event in pg.event.get():
        player.handle_portal(map, event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_3]:
        player.rect.centerx, player.rect.centery = 500, 500

    if player.rect.colliderect(map.get_layer_as_rect("trigger_1")):
        load_map(levels[map.level_index])
        map.level_index += 1

    for entity in entity_list:
        map.group.add(entity)
    cube.update(map)
    player.update()
    map.collide(player)
    clock.tick(FPS)
    map.update(player.rect.center)
    pg.display.flip()
