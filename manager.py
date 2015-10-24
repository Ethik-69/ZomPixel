#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sprites import *
from Character import *
from constants import *


class PNJ(object):
    def __init__(self, main, start_enemy_list, level):
        self.enemy_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.feeding_zombie_list = pygame.sprite.Group()
        self.main = main
        self.level = level
        self.init_pnj(start_enemy_list)

    def init_pnj(self, enemy_data):
        """Initialise les Personnages Non Joueur"""
        print('     - PNJ Init in Progress')
        pnj_num = 0  # compteur pour différencier les pnj
        for pos in enemy_data.keys():
            new_enemy = Humain(self.main, enemy_data[pos], pos, pnj_num)
            self.enemy_list.add(new_enemy)
            pnj_num += 1
            print('.'),

    def add_zombie(self, main, id_name, name, img, pos, num):
        print('[*] ' + name + ' Going Zombie')
        init_value = {'id_name': name, 'img': img, 'name': name}
        zombie = Zombie(main, init_value, pos, num)
        self.zombie_list.add(zombie)
        print('[*] New Zombie')

    def remove_zombie(self):
        print('[*] Remove Remaining Zombies')
        for zombie in self.zombie_list:
            self.zombie_list.remove(zombie)
        print('     - Ok')

    def update(self):
        """met les pnj a jour"""
        for enemy in self.enemy_list:
            if not enemy.isAlive:
                print('[*] Remove Humain')
                self.enemy_list.remove(enemy)

        for zombie in self.zombie_list:
            if not zombie.isAlive:
                print('[*] Remove Zombie')
                self.zombie_list.remove(zombie)

        if len(self.enemy_list) == 0 and self.level.is_started:
            print('[*] Change Lvl => True')
            self.level.is_change_level = True

        self.enemy_list.update()
        self.zombie_list.update()

    def draw(self):
        """dessine les enemies"""
        self.enemy_list.draw(self.main.window)

        # Ne pas afficher les zombie 'ia' qui se baffrent
        if len(self.zombie_list) != 0:
            for zombie in self.zombie_list:
                if zombie.is_feeding:
                    self.feeding_zombie_list.add(zombie)
                    self.zombie_list.remove(zombie)

            self.zombie_list.draw(self.main.window)

            for zombie in self.feeding_zombie_list:
                self.zombie_list.add(zombie)
                self.feeding_zombie_list.remove(zombie)


class Obstacles(object):
    def __init__(self, main):
        """
        Obstacle initialiser avec les position des objets sur la feuille de sprite
        Remplacés par [image, rect] correspondantent juste en dessous
        """
        self.main = main
        self.objects_list = pygame.sprite.Group()

        self.sprites = SpriteSheet('data/img/objets.png')

    def create_all(self, objects_pos):
        for key in objects_pos.keys():
            for pos in objects_pos[key]:
                obstacle = Object(self.main, key, constants.OBJECTS[key], pos, self.sprites)
                obstacle.display()
                self.objects_list.add(obstacle)


class Object(pygame.sprite.Sprite):
    def __init__(self, main, name, sprite_sheet_data, pos, sprite_sheet):
        pygame.sprite.Sprite.__init__(self)

        self.main = main
        self.name = name
        self.pos = pos

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.mask = pygame.mask.from_surface(self.image)

    def display(self):
        self.main.background.blit(self.image, self.pos)
