import pygame as pg
import map, player
import sys

pg.init()
display = pg.display.set_mode((512, 512), pg.SCALED | pg.RESIZABLE)
map = map.Map(510, 510)
map.load("assets/maps/flat.tmx")
player = player.Player(pg.image.load("assets/player.png"))
map.group_add(player)
FPS = 60
clock = pg.time.Clock()
levels = ["assets/maps/flat.tmx", "assets/maps/map1.tmx"]


def load_map(file_name):
    map.load(file_name)
    map.group_add(player)


while True:
    for event in pg.event.get():
        player.handle_portal(map, event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_3]:
        player.rect.centerx, player.rect.centery = 500, 500

    if map.collide_layer(player, "trigger_1"):
        load_map(levels[map.level_index])
        map.level_index += 1

    player.update()
    player.rect.clamp_ip(map.map_layer.map_rect)
    map.collide(player)
    clock.tick(FPS)
    map.update(player.rect.center)
    pg.display.flip()
