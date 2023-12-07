import pygame as pg
import map, player
pg.init()
display = pg.display.set_mode((720, 480), pg.SCALED | pg.RESIZABLE)
map = map.Map(510, 510)
map.load("assets/map1.tmx")
player = player.Player(pg.image.load("assets/player.png"))
map.group_add(player)
FPS = 60
clock = pg.time.Clock()
3
while True:
    for event in pg.event.get():
        player.handle_portal(map, event)
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    keys = pg.key.get_pressed()
    if keys[pg.K_1]:
        print('test')
        map.load("assets/map2.tmx")
        map.group_add(player)
        map.update(player.rect.center)
    elif keys[pg.K_2]:
        map.load("assets/map1.tmx")
        map.group_add(player)
        map.update(player.rect.center)
    elif keys[pg.K_3]:
        player.rect.centerx, player.rect.centery = 500, 500
    player.update()
    player.rect.clamp_ip(map.map_layer.map_rect)
    map.collide(player)
    clock.tick(FPS)
    map.update(player.rect.center)
    pg.display.flip()