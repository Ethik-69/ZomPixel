#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Character import *


class PNJ(object):
    def __init__(self, main, start_enemy_list, level):
        self.enemy_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.feeding_zombie_list = pygame.sprite.Group()
        self.main = main
        self.level = level
        self.init_pnj(start_enemy_list)

    def init_pnj(self, start_enemy_list):
        """Initialise les Personnages Non Joueur"""
        print('     - PNJ Init in Progress')
        for enemy in start_enemy_list:
            new_enemy = Humain(self.main, enemy['nom'], enemy['img'],
                               enemy['pos_x'], enemy['pos_y'])
            self.enemy_list.add(new_enemy)
            print('.'),

    def add_zombie(self, main, name, img, x, y):
        print('[*] ' + name + ' Going Zombie')
        zombie = Zombie(main, 'z_' + name, img, x, y)
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
