import sys

import pygame as pg

import entity
import map
from player import Player

pg.init()
display = pg.display.set_mode((512, 512), pg.SCALED | pg.RESIZABLE)
map = map.Map(510, 510)
map.load("assets/maps/flat.tmx")

right_idle_images = [pg.image.load("assets\Pics\player_sprite\idle1.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\idle2.png").convert_alpha(),
                     pg.image.load("assets\Pics\player_sprite\idle3.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\idle4.png").convert_alpha()]
left_idle_images = [pg.image.load("assets\Pics\player_sprite\idle11.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\idle22.png").convert_alpha(),
                     pg.image.load("assets\Pics\player_sprite\idle33.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\idle44.png").convert_alpha()]
move_right_images = [pg.image.load("assets\Pics\player_sprite\walk1.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk3.png").convert_alpha(),
                     pg.image.load("assets\Pics\player_sprite\walk4.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk5.png").convert_alpha(),
                     pg.image.load("assets\Pics\player_sprite\walk6.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk7.png").convert_alpha(),
                     pg.image.load("assets\Pics\player_sprite\walk8.png").convert_alpha()]
move_left_images = [pg.image.load("assets\Pics\player_sprite\walk11.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk33.png").convert_alpha(),
                    pg.image.load("assets\Pics\player_sprite\walk44.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk55.png").convert_alpha(),
                    pg.image.load("assets\Pics\player_sprite\walk66.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\walk77.png").convert_alpha(),
                    pg.image.load("assets\Pics\player_sprite\walk88.png").convert_alpha()]

player = Player(right_idle_images, left_idle_images, move_right_images, move_left_images)

FPS = 60
clock = pg.time.Clock()
levels = ["assets/maps/flat.tmx", "assets/maps/map1.tmx"]
entity_list = []
cube = entity.Cube(pg.image.load("assets/cube.png"))
entity_list.append(cube)

def load_map(file_name):
    map.load(file_name)


while True:
    for event in pg.event.get():
        player.handle_portal(map, event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_e]:
        cube.velocity[0], cube.velocity[1] = pg.mouse.get_pos()[0] - cube.rect.centerx, pg.mouse.get_pos()[1] - cube.rect.centery
    if keys[pg.K_3]:
        player.rect.centerx, player.rect.centery = pg.mouse.get_pos()[0] - map.map_layer.get_center_offset()[0], pg.mouse.get_pos()[1] - map.map_layer.get_center_offset()[1]
        player.velocity_y = 0
    elif keys[pg.K_4]:
        print(cube.gravity)
    if player.rect.colliderect(map.get_layer_as_rect("trigger_1")):
        load_map(levels[map.level_index])
        map.level_index += 1

    for entity in entity_list:
        map.group.add(entity)
        player.collide_with(entity.rect)
        map.collide(entity)
        entity.update(player)
    map.group.add(player)

    player.update()

    map.collide(player)
    clock.tick(FPS)
    map.update(player.rect.center)
    pg.display.flip()