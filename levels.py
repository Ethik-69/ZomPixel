#!/usr/bin/env python
# -*- coding:utf-8 -*-
import constants
from random import randint
from manager import *


class Levels(object):
    """"Class principal des niveaux"""
    def __init__(self, main):
        self.survival = None
        self.current_level = None
        self.current_level_number = 0

        self.is_started = False
        self.main = main
        self.main.time.add_chrono('current_level')

        self.hud_image = main.game_images['hud']
        self.skull_image = main.game_images['skull_image']
        self.game_background_image = main.game_images['map']

        self.obstacles = Obstacles(self.main)

    def init_campagne_level(self):
        """Initialisation des niveaux"""
        print('[*] Generation in Progress')
        self.current_level = Level(self.main, constants.LEVELS_LIST[self.current_level_number])
        print('[*] Generation Ok')

    def init_survival_level(self, map_pos):
        self.current_level = SurvivalLevel(self.main, map_pos)

    def next_level(self):
        """Passe au niveau suivant"""
        print('[*] Next Level')
        self.is_started = False
        print('[*] Current Level Number ' + str(self.current_level_number))
        self.current_level_number += 1
        print('[*] Next Level Number ' + str(self.current_level_number))
        if self.current_level_number == len(constants.LEVELS_LIST):
            return False
        self.main.background.fill((0, 0, 0))
        self.init_campagne_level()
        print('[*] Return levels ', self)
        return self  # pour que le current lvl du main change


class Level(Levels):
    """Class secondaire des niveau"""
    def __init__(self, main, lvl):
        Levels.__init__(self, main)
        self.current_level_number = lvl['number']
        self.objects_pos = lvl['objects']

        self.pos_x, self.pos_y = lvl['pos_level'][0], lvl['pos_level'][1]
        self.pos_player_x, self.pos_player_y = lvl['pos_player'][0], lvl['pos_player'][1]

        self.is_change_level = False
        self.game_over = False
        self.main.time.chronos['current_level'].start()

        print('[*] Init obj PNJ')
        self.pnj = PNJ(main, lvl['enemy'], self)
        print('[*] Init obj PNJ Ok')

    def start(self):
        """Re-initialise la position du joueur - re-initialise le fond - créer les obstacles et lance le chrono"""
        print('[*] Level Start')
        self.main.player.reset(self.pos_player_x, self.pos_player_y)

        self.main.background.blit(self.game_background_image, (self.pos_x, self.pos_y))
        self.main.background.blit(self.hud_image, (-5, -2))
        self.skull_image = pygame.transform.scale(self.skull_image, (30, 35))
        self.main.background.blit(self.skull_image, (constants.GAME_WIDTH/1.99, 7))

        self.obstacles.create_all(self.objects_pos)

        self.main.time.chronos['current_level'].reset()
        self.is_started = True
        print('     - Ok')

    def update(self):
        self.pnj.update(self.obstacles.objects_list)
        if self.main.time.chronos['current_level'].Time == [00, 30, 00]:
            print('[*] Time Out')
            self.main.display_game_over('Time Out')


class SurvivalLevel(Levels):
    def __init__(self, main, map_pos):
        Levels.__init__(self, main)
        self.is_game_over = False
        self.main = main
        self.max_pnj = 5  # Limite le nombre d'enemy

        self.objects_pos = constants.SURVIVAL[map_pos]['objects']

        self.pos_x = constants.SURVIVAL[map_pos]['pos_map'][0]
        self.pos_y = constants.SURVIVAL[map_pos]['pos_map'][1]
        self.pos_player_x = constants.SURVIVAL[map_pos]['pos_player'][0]
        self.pos_player_y = constants.SURVIVAL[map_pos]['pos_player'][1]

        self.pnj = PNJ(self.main, constants.SURVIVAL[map_pos]['enemy'], self)
        
        self.main.time.add_chrono('survival')
        self.main.time.add_rebour('increase_pnj_number')
        print('[*] Init Survival Ok')

    def start(self):
        print('[*] Survival Start')
        self.main.player.reset(self.pos_player_x, self.pos_player_y)

        self.main.background.blit(self.game_background_image, (self.pos_x, self.pos_y))
        self.main.background.blit(self.hud_image, (-5, -2))
        self.skull_image = pygame.transform.scale(self.skull_image, (30, 35))
        self.main.background.blit(self.skull_image, (constants.GAME_WIDTH/1.99, 7))

        self.obstacles.create_all(self.objects_pos)

        self.main.time.chronos['survival'].start()
        self.main.time.rebours['increase_pnj_number'].start([00, 20, 00])

    def random_pos(self):
        rand = randint(1, 2)
        if rand == 1:
            x = 0
        else:
            x = 990
        y = randint(0, 600)
        return x, y

    def update(self):
        if self.main.time.rebours['increase_pnj_number'].isFinish:
            self.max_pnj += 1
            self.main.victims -= 1 # hack pour que l'enemy en plus ne compte pas
            self.main.time.rebours['increase_pnj_number'].start([00, 20, 00])
        if len(self.pnj.enemy_list) < self.max_pnj:
            self.pnj.add_enemy(self.random_pos())
            self.main.victims += 1
        self.pnj.update(self.obstacles.objects_list)
        if self.main.time.chronos['survival'].Time == [01, 00, 00]:
            print('[*] Time Out')
            self.main.display_game_over('Time Out')
