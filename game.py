import sys
import pygame as pg
import entity
import map
from player import Player

# initialized pygame and the map
pg.init()
display = pg.display.set_mode((512, 512), pg.SCALED | pg.RESIZABLE)
map = map.Map(510, 510)
map.load("assets/maps/map1.tmx")

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
#jump_rigsht_images = [pg.image.load("assets\Pics\player_sprite\jump1.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\jump2.png").convert_alpha(),
                     #pg.image.load("assets\Pics\player_sprite\jump3.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\jump4.png").convert_alpha(),
                     #pg.image.load("assets\Pics\player_sprite\jump5.png").convert_alpha()]
#jump_left_images = [pg.image.load("assets\Pics\player_sprite\jump11.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\jump22.png").convert_alpha(),
                     #pg.image.load("assets\Pics\player_sprite\jump33.png").convert_alpha(), pg.image.load("assets\Pics\player_sprite\jump44.png").convert_alpha(),
                     #pg.image.load("assets\Pics\player_sprite\jump55.png").convert_alpha()]


class Game():
    def __init__(self):
    # initialize the player, cube, levels, and fps
        self.player = Player(right_idle_images, left_idle_images, move_right_images, move_left_images,scale_factor=0.75) #jump_right_images, jump_left_images)
        self.player.rect.center = map.get_layer_as_rect("start").center
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.levels = ["assets/maps/map1.tmx", "assets/maps/map2.tmx"]

        self.entity_list = []
        self.cube = entity.Cube(pg.image.load("assets/cube.png"))
        self.entity_list.append(self.cube)
        self.cube.disabled = True

    def loop(self):
        # main game loop
        while True:
            for event in pg.event.get():
                self.player.handle_portal(map, event)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    self.player.handle_movement()
                    self.player.handle_portal(map, event)

            # game loop
            if map.level_index == 1:
                if self.cube.rect.colliderect(map.get_layer_as_rect("trigger_2")):
                    if self.player.rect.colliderect(map.get_layer_as_rect("trigger_1")):
                        map.level_index += 1
                        map.load(self.levels[map.level_index])
            elif self.player.rect.colliderect(map.get_layer_as_rect("trigger_1")):
                map.level_index += 1
                map.load(self.levels[map.level_index])
                self.player.rect.center = map.get_layer_as_rect("start").center
                self.cube.disabled = False
                self.cube.rect.center = map.get_layer_as_rect("start").center

            # keybindings
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                self.cube.velocity[0], self.cube.velocity[1] = (pg.mouse.get_pos()[0] - map.map_layer.get_center_offset()[0]) - self.cube.rect.centerx, (pg.mouse.get_pos()[1] - map.map_layer.get_center_offset()[1]) - self.cube.rect.centery
            elif keys[pg.K_g]:
                self.cube.rect.center = (pg.mouse.get_pos()[0] - map.map_layer.get_center_offset()[0]), (pg.mouse.get_pos()[1] - map.map_layer.get_center_offset()[1])
                self.cube.velocity[1] = 1
            if keys[pg.K_3]:
                self.player.rect.centerx, self.player.rect.centery = pg.mouse.get_pos()[0] - map.map_layer.get_center_offset()[0], pg.mouse.get_pos()[1] - map.map_layer.get_center_offset()[1]
                self.player.velocity_y = 0
            elif keys[pg.K_4]:
                if self.cube.disabled:
                    self.cube.disabled = False
                else:
                    self.cube.disabled = True


            # entity / cube updates
            for entity in self.entity_list:
                if not entity.disabled:
                    map.group.add(entity)
                    map.collide(entity)
                    self.player.collide_with(entity.rect)
                    entity.update(self.player)
                elif entity.disabled:
                    map.group.remove(entity)
            map.group.add(self.player)

            # player and map updates
            self.player.update()
            self.player.portal_collision()
            self.player.update_portal()
            map.collide(self.player)
            self.clock.tick(self.FPS)
            map.update(self.player.rect.center)
            pg.display.flip()