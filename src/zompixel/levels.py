#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import pygame
import zompixel.constants as constants
from zompixel.manager import PNJ, Obstacles
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class Levels(object):
    """"Gère les niveaux"""

    def __init__(self, main):
        self.survival = None
        self.current_level = None
        self.current_level_number = 0

        self.pnj = None
        self.is_started = False
        self.is_change_level = False
        self.main = main
        self.main.time.add_chrono("current_level")

        self.hud_image = main.game_images["hud"]
        self.skull_image = main.game_images["skull_image"]
        self.game_background_image = main.game_images["map"]

        self.obstacles = Obstacles(self.main)

    def init_campagne_level(self):
        """Initialise le niveau en cour"""
        LOGGER.info("[*] Generation in Progress")
        self.current_level = Level(
            self.main, constants.LEVELS_LIST[self.current_level_number]
        )
        LOGGER.info("[*] Generation Ok")

    def init_survival_level(self, map_pos):
        """Initialise le survival"""
        self.current_level = SurvivalLevel(self.main, map_pos)

    def next_level(self):
        """Change le niveau en cour (suivant)"""
        LOGGER.info("[*] Next Level")
        self.is_started = False

        LOGGER.info("[*] Current Level Number " + str(self.current_level_number))
        self.current_level_number += 1

        LOGGER.info("[*] Next Level Number " + str(self.current_level_number))
        if self.current_level_number >= len(constants.LEVELS_LIST):
            return False

        self.main.background.fill((0, 0, 0))
        self.pnj.remove_all_zombie()
        self.obstacles.reset()
        self.init_campagne_level()
        self.is_change_level = False
        LOGGER.info("[*] Return levels ", self)
        return self  # Change le current_lvl du main


class Level(Levels):
    """Gère un niveau"""

    def __init__(self, main, lvl):
        Levels.__init__(self, main)
        self.current_level_number = lvl["number"]
        self.objects_pos = lvl["objects"]

        self.pos_x, self.pos_y = lvl["pos_level"][0], lvl["pos_level"][1]
        self.pos_player_x, self.pos_player_y = (
            lvl["pos_player"][0],
            lvl["pos_player"][1],
        )

        self.game_over = False

        LOGGER.info("[*] Init obj PNJ")
        self.pnj = PNJ(main, lvl["enemy"], self)
        LOGGER.info("[*] Init obj PNJ Ok")

    def start(self):
        """Re-initialise la position du joueur et le fond - créer les obstacles et lance le chrono"""
        LOGGER.info("[*] Level Start")
        self.main.player.reset(self.pos_player_x, self.pos_player_y)

        self.main.background.blit(self.game_background_image, (self.pos_x, self.pos_y))
        self.main.background.blit(self.hud_image, (-5, -2))
        self.skull_image = pygame.transform.scale(self.skull_image, (30, 35))
        self.main.background.blit(self.skull_image, (constants.GAME_WIDTH / 2.3, 7))

        self.obstacles.create_all(self.objects_pos)

        self.main.time.chronos["current_level"].start()
        self.is_started = True
        LOGGER.info("     - Ok")

    def update(self):
        """Met à jour le niveau"""
        self.pnj.update()

        if self.main.time.chronos["current_level"].Time == [00, 30, 00]:
            LOGGER.info("[*] Time Out")
            self.main.display_game_over("Time Out")


class SurvivalLevel(Levels):
    """Gère le survival"""

    def __init__(self, main, map_pos):
        Levels.__init__(self, main)
        self.is_game_over = False
        self.main = main
        self.max_pnj = 5  # Limite le nombre d'enemy

        self.objects_pos = constants.SURVIVAL[map_pos]["objects"]

        self.pos_x = constants.SURVIVAL[map_pos]["pos_map"][0]
        self.pos_y = constants.SURVIVAL[map_pos]["pos_map"][1]
        self.pos_player_x = constants.SURVIVAL[map_pos]["pos_player"][0]
        self.pos_player_y = constants.SURVIVAL[map_pos]["pos_player"][1]

        self.pnj = PNJ(self.main, constants.SURVIVAL[map_pos]["enemy"], self)

        self.main.time.add_chrono("survival")
        self.main.time.add_rebour("increase_pnj_number")
        LOGGER.info("[*] Init Survival Ok")

    def start(self):
        """Re-initialise la position du joueur et le fond - créer les obstacles et lance les chronos/rebours"""
        LOGGER.info("[*] Survival Start")
        self.main.player.reset(self.pos_player_x, self.pos_player_y)

        self.main.background.blit(self.game_background_image, (self.pos_x, self.pos_y))
        self.main.background.blit(self.hud_image, (-5, -2))
        self.skull_image = pygame.transform.scale(self.skull_image, (30, 35))
        self.main.background.blit(self.skull_image, (constants.GAME_WIDTH / 2.3, 7))

        self.obstacles.create_all(self.objects_pos)

        self.main.time.chronos["survival"].start()
        self.main.time.rebours["increase_pnj_number"].start([00, 20, 00])

    @staticmethod
    def random_pos():
        """Renvoi une position (x, y) 'aléatoire' """
        rand = random.randint(1, 2)
        if rand == 1:
            x = 0

        else:
            x = 900

        y = random.randint(50, 550)

        return x, y

    def update(self):
        """Met à jour le survival"""
        if self.main.time.chronos["survival"].Time == [2, 00, 00]:
            LOGGER.info("[*] Time Out")
            self.main.display_game_over("Time Out")

        if self.main.time.rebours["increase_pnj_number"].isFinish:
            self.max_pnj += 1
            self.main.time.rebours["increase_pnj_number"].start([00, 20, 00])

        if len(self.main.enemy_sprites) < self.max_pnj:
            self.pnj.add_enemy(self.random_pos())

        self.pnj.update()
