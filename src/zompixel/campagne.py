#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import pygame
from zompixel.levels import Levels
from zompixel.player import Player
import zompixel.constants as constants
from zompixel.utils.time_made_home import Times
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class Campagne(object):
    def __init__(self, main):
        self.window = main.window
        self.background = main.background

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.pnj_sprites = pygame.sprite.LayeredUpdates()
        self.enemy_sprites = pygame.sprite.LayeredUpdates()
        self.zombie_sprites = pygame.sprite.LayeredUpdates()

        self.game_images = main.game_images
        self.obstacles_images = main.obstacles_images
        self.character_images = main.character_images

        self.is_mouse_button_down = main.is_mouse_button_down

        self.hud_font = main.hud_font
        self.welcome_font0 = main.welcome_font0
        self.welcome_font1 = main.welcome_font1
        self.final_score_font = main.final_score_font

        self.button_accueil = None
        self.button_next_level = None

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.frameRate = 0
        self.frameCount = 0

        self.run = None
        self.player = None
        self.click_pos_x = None
        self.click_pos_y = None
        self.enemy_hit_list = None
        self.obstacles_collided = None

        self.is_credit = False
        self.is_game_over = False
        self.is_display_score = False

        self.create_player()

        self.levels = Levels(self)
        self.levels.init_campagne_level()
        self.main()

    def text_blit(self, font, text, text_color, pos):
        text_to_blit = font.render(text, 1, text_color)
        text_to_blit_pos = text_to_blit.get_rect(centerx=pos[0], centery=pos[1])
        self.background.blit(text_to_blit, text_to_blit_pos)

    def create_player(self):
        """Création du joueur"""
        LOGGER.info("[*] Player Init")

        self.player = Player(
            "player",
            self.character_images["player"],
            self.all_sprites,
            512,
            354,
            constants.GAME_WIDTH,
            constants.GAME_HEIGHT,
        )

        self.time.add_rebour("player")
        LOGGER.info("     - Ok")

    #########################################
    """Gestion évènements"""
    #########################################

    # -------------Déplacements--------------

    def click_motion(self):
        """Gestion du déplacement du joueur au click"""
        if self.click_pos_x == self.player.rect.x:
            self.player.moveX = 0
            self.click_pos_x = None

        if self.click_pos_y == self.player.rect.y:
            self.player.moveY = 0
            self.click_pos_y = None

        if self.click_pos_x is not None:
            if self.click_pos_x < self.player.rect.x:
                self.player.action = "left"
                self.player.move_left()

            elif self.click_pos_x > self.player.rect.x:
                self.player.action = "right"
                self.player.move_right()

        if self.click_pos_y is not None:
            if self.click_pos_y < self.player.rect.y:
                self.player.action = "up"
                self.player.move_up()

            elif self.click_pos_y > self.player.rect.y:
                self.player.action = "down"
                self.player.move_down()

        if self.click_pos_x is None and self.click_pos_y is None:
            self.player.action = ""

    # ------------Fin de niveau--------------

    def init_score_screen(self):
        """Initialisation de l'affichage du score en fin de niveau"""
        LOGGER.info("[*] Init Display Score")
        time = self.time.chronos[
            "current_level"
        ].Time  # temp qu'a mis le joueur pour terminer le niveau

        # Pose l'image
        self.background.blit(
            self.game_images["score_image"],
            (constants.GAME_WIDTH / 6.5, constants.GAME_HEIGHT / 4),
        )

        # Définit et pose les texts
        self.text_blit(
            self.final_score_font,
            str(self.player.score) + " Points",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2),
        )

        self.text_blit(
            self.final_score_font,
            "Termine en",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.8),
        )

        self.text_blit(
            self.final_score_font,
            str(time[0]) + ":" + str(time[1]) + ":" + str(time[2]),
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.7),
        )

        self.text_blit(
            self.final_score_font,
            "Niveau suivant",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.5),
        )

        self.window.blit(self.background, (0, 0))

        # Pose le bouton changement de niveau
        self.button_next_level = pygame.draw.rect(
            self.window,
            [255, 255, 255],
            [constants.GAME_WIDTH / 2.64, constants.GAME_HEIGHT / 1.555, 245, 35],
            2,
        )

        pygame.display.flip()
        LOGGER.info("     - Ok")

    def display_score(self):
        """"Boucle de l'affichage du score"""
        self.is_display_score = True
        self.init_score_screen()

        while self.is_display_score:
            self.display_hud()
            mouse_xy = pygame.mouse.get_pos()
            is_lvl_change = self.button_next_level.collidepoint(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_lvl_change:
                    self.player.score = 0
                    self.click_pos_x = 0
                    self.click_pos_y = 0
                    self.is_display_score = False

            pygame.display.flip()

    # --------------Mort Joueur--------------

    def init_game_over(self):
        """Initiasile le game_over"""
        LOGGER.info("[*] Init Game Over")

        # Pose les images
        self.background.blit(
            self.game_images["game_over_image"],
            (constants.GAME_WIDTH / 6.6, constants.GAME_HEIGHT / 3.5),
        )

        self.background.blit(
            self.game_images["skull_image"],
            (constants.GAME_WIDTH / 3.15, constants.GAME_HEIGHT / 2.1),
        )

        self.background.blit(
            self.game_images["skull_image"],
            (constants.GAME_WIDTH / 1.55, constants.GAME_HEIGHT / 2.1),
        )

        # Définit et pose les texts
        self.text_blit(
            self.final_score_font,
            "Vous etes definitivement",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2.3),
        )

        self.text_blit(
            self.welcome_font1,
            "M.O.R.T",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.95),
        )

        self.text_blit(
            self.final_score_font,
            "Score final: " + str(self.player.final_score),
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.7),
        )

        self.text_blit(
            self.final_score_font,
            "Accueil",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.55),
        )

        self.window.blit(self.background, (0, 0))

        # Pose le bouton de retour à l'accueil
        self.button_accueil = pygame.draw.rect(
            self.window,
            [255, 255, 255],
            [constants.GAME_WIDTH / 2.3, constants.GAME_HEIGHT / 1.6, 130, 30],
            2,
        )

        pygame.display.flip()
        LOGGER.info("     - Ok")

    def init_time_out(self):
        """Initialise le time out"""
        LOGGER.info("[*] Init Time Out")

        # Pose les images
        self.background.blit(
            self.game_images["game_over_image"],
            (constants.GAME_WIDTH / 6.6, constants.GAME_HEIGHT / 3.5),
        )

        self.background.blit(
            self.game_images["skull_image"],
            (constants.GAME_WIDTH / 3.15, constants.GAME_HEIGHT / 1.9),
        )

        self.background.blit(
            self.game_images["skull_image"],
            (constants.GAME_WIDTH / 1.55, constants.GAME_HEIGHT / 1.9),
        )

        # Définit et pose les texts
        self.text_blit(
            self.welcome_font1,
            "Temps ecoule",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2.2),
        )

        self.text_blit(
            self.final_score_font,
            "Score final: " + str(self.player.final_score),
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.8),
        )

        self.text_blit(
            self.final_score_font,
            "Accueil",
            (255, 255, 255),
            (constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 1.55),
        )

        self.window.blit(self.background, (0, 0))

        # Pose le bouton de retour à l'accueil
        self.button_accueil = pygame.draw.rect(
            self.window,
            [255, 255, 255],
            [constants.GAME_WIDTH / 2.3, constants.GAME_HEIGHT / 1.6, 130, 30],
            2,
        )

        pygame.display.flip()
        LOGGER.info("     - Ok")

    def display_game_over(self, end_type):
        """Boucle du game over"""
        self.is_game_over = True

        if end_type == "game_over":
            self.init_game_over()

        else:
            self.init_time_out()

        while self.is_game_over:
            self.display_hud()
            mouse_xy = pygame.mouse.get_pos()
            is_accueil = self.button_accueil.collidepoint(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_accueil:
                    self.is_game_over = False
                    self.end_game()

            pygame.display.flip()

    def init_credit(self):
        """Initialise les crédits"""
        LOGGER.info("[*] Init Game Over")
        self.background.fill((0, 0, 0))

        # Définit et pose les texts
        self.text_blit(
            self.welcome_font1,
            "Pre-Alpha terminee !",
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 100),
        )

        self.text_blit(
            self.final_score_font,
            "Votre score final est de " + str(self.player.final_score),
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 200),
        )

        self.text_blit(
            self.final_score_font,
            "Rejoignez nous sur Facebook: ZompiGame !",
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 300),
        )

        self.text_blit(
            self.final_score_font,
            "Cree par:",
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 400),
        )

        self.text_blit(
            self.final_score_font,
            "Ethan CHAMIK",
            (100, 20, 20),
            (constants.GAME_WIDTH / 5, 500),
        )

        self.text_blit(
            self.final_score_font,
            "Thibault DESCAMPS",
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 500),
        )

        self.text_blit(
            self.final_score_font,
            "Romain GUILLOT",
            (100, 20, 20),
            (constants.GAME_WIDTH / 1.2, 500),
        )

        self.text_blit(
            self.final_score_font,
            "Faites tournez ;)",
            (100, 20, 20),
            (constants.GAME_WIDTH / 2, 600),
        )

        self.text_blit(
            self.welcome_font1, "Retour", (100, 20, 20), (constants.GAME_WIDTH / 2, 700)
        )

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        LOGGER.info("     - Ok")

    def display_credit(self):
        """Boucle des crédits"""
        LOGGER.info("[*] Credit")
        self.is_credit = True
        self.background.fill((0, 0, 0))

        self.init_credit()

        self.window.blit(self.background, (0, 0))

        button_back = pygame.draw.rect(
            self.window, [100, 20, 20], [constants.GAME_WIDTH / 2.55, 675, 215, 50], 2
        )

        pygame.display.flip()

        while self.is_credit:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_back:
                    self.is_credit = False
                    LOGGER.info("[*] Leaving Credit")
                    self.end_game()

    def end_game(self):
        LOGGER.info("[*] Campagne End")
        self.run = False

    #########################################
    """Boucle Principal"""
    #########################################

    def display_hud(self):
        """Pose l'ATH (affichage tête haute) (score - temps.....)"""
        current_lvl = self.hud_font.render(
            "%s %s" % ("Niveau", self.levels.current_level_number), True, (0, 0, 0)
        )

        score = self.hud_font.render(
            "%s" % self.player.score, True, (0, 0, 0)
        )  # player.score

        time = self.hud_font.render(
            "%s:%s:%s"
            % (
                self.time.chronos["current_level"].Time[0],
                self.time.chronos["current_level"].Time[1],
                self.time.chronos["current_level"].Time[2],
            ),
            True,
            (0, 0, 0),
        )  # time

        self.window.blit(current_lvl, (50, 14))
        self.window.blit(score, (492, 14))
        self.window.blit(time, (878, 14))

    def layer_change(self):
        """Change le joueur et les pnjs de layer"""
        if self.player.is_layer_change:
            LOGGER.info("[*] Change Player Layer")
            self.all_sprites.change_layer(
                self.player, constants.LAYER_POS[self.player.pos_on_layer]
            )
            self.player.is_layer_change = False

        for pnj in self.pnj_sprites:
            if pnj.is_layer_change:
                LOGGER.info("[*] Change " + pnj.name + " Layer")
                self.all_sprites.change_layer(
                    pnj, constants.LAYER_POS[pnj.pos_on_layer]
                )
                pnj.is_layer_change = False

    def test(self):
        """Test"""
        for pnj in self.enemy_sprites:
            if pnj.is_crazy:
                pygame.draw.rect(self.window, (255, 255, 255), pnj.hitbox_rect)

            else:
                pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

        for pnj in self.zombie_sprites:
            pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

        for object in self.levels.current_level.obstacles.objects_list:
            pygame.draw.rect(self.window, (0, 0, 0), object.collision_rect)

        pygame.draw.rect(self.window, (100, 10, 10), self.player.collision_rect)

    def main(self):
        """Boucle principal de la campagne"""
        LOGGER.info("[*] Launch Campagne")
        self.run = True
        self.levels.current_level.start()

        LOGGER.info("[*] Start")
        while self.run:
            mouse_xy = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_mouse_button_down = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_mouse_button_down = False

            # -------------------------Update--------------------------

            if self.is_mouse_button_down:
                self.click_pos_x = mouse_xy[0] - self.player.width / 2
                self.click_pos_y = mouse_xy[1] - self.player.height / 2

            self.click_motion()
            self.time.update()
            self.enemy_sprites.update(self.levels.current_level.obstacles.objects_list)
            self.zombie_sprites.update(
                self.levels.current_level.obstacles.objects_list, self.enemy_sprites
            )
            self.player.update(
                self.levels.current_level.obstacles.objects_list, self.enemy_sprites
            )
            self.levels.current_level.update()
            self.layer_change()

            if self.player.dying:
                self.display_game_over("game_over")

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()

            self.levels.current_level.obstacles.objects_list.draw(self.window)

            self.all_sprites.draw(self.window)

            # self.test()

            # -----------------------Change Lvl------------------------
            if len(self.enemy_sprites) == 0 and self.levels.current_level.is_started:
                LOGGER.info("[*] Change Lvl => True")
                self.levels.current_level.is_change_level = True

            if self.levels.current_level.is_change_level:
                LOGGER.info("[*] Level End")
                self.click_pos_x = None
                self.click_pos_y = None
                self.display_score()
                self.levels = self.levels.current_level.next_level()

                if not self.levels:
                    LOGGER.info("[*] Game End")
                    self.display_credit()

                else:
                    self.levels.current_level.start()
                    LOGGER.info(
                        "[*] Current Level Number"
                        + str(self.levels.current_level_number)
                    )

            # ----------------------------------------------------------

            pygame.display.flip()
            self.clock.tick(100)

        LOGGER.info("[*] Fin de la boucle Campagne")
