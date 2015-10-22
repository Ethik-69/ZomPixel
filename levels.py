#!/usr/bin/env python
# -*- coding:utf-8 -*-
from manager import *


class Levels(object):
    """"Class principal des niveaux"""
    def __init__(self, main):
        self.game_background_image = pygame.image.load('data/img/map.png').convert()
        self.hud_image = pygame.image.load('data/img/hud.png')

        self.current_level = None
        self.current_level_number = 0

        self.is_started = False
        self.main = main
        self.main.time.add_chrono('current_level')

        self.obstacles = Obstacles(self.main)

    def init_level(self):
        """Initialisation des niveaux"""
        print('[*] Generation in Progress')
        self.current_level = Level(self.main, constants.LEVELS_LIST[self.current_level_number])
        print('     - Ok')

    def next_level(self):
        print('[*] Next Level')
        self.is_started = False
        self.current_level_number += 1
        print('[*] Next Level Number ' + str(self.current_level_number))
        if self.current_level_number == len(constants.LEVELS_LIST):
            return False
        self.main.background.fill((0, 0, 0))
        self.init_level()
        self.current_level.start()
        return self  # pour que le current lvl du main change


class Level(Levels):
    """Class secondaire des niveau"""
    def __init__(self, main, lvl):
        Levels.__init__(self, main)
        self.number = lvl['number']
        self.objects_pos = lvl['objects']

        self.pos_x, self.pos_y = lvl['pos_level'][0], lvl['pos_level'][1]
        self.pos_player_x, self.pos_player_y = lvl['pos_player'][0], lvl['pos_player'][1]

        self.is_change_level = False
        self.main.time.chronos['current_level'].start()

        print('[*] Init obj PNJ')
        self.pnj = PNJ(main, lvl['enemy'], self)
        print('[*] Init obj PNJ Ok')

    def start(self):
        """Lance le niveau"""
        print('[*] Level Start')
        self.main.player.rect.x, self.main.player.rect.y = self.pos_player_x, self.pos_player_y
        self.main.background.blit(self.game_background_image, (self.pos_x, self.pos_y))

        self.main.background.blit(self.hud_image, (-5, -2))

        self.obstacles.create_all(self.objects_pos)

        self.is_started = True
        self.main.time.chronos['current_level'].reset()
        print('     - Ok')
