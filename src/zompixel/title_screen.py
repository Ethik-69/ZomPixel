#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import pygame
from zompixel.campagne import Campagne
from zompixel.survival import Survival
import zompixel.constants as constants
from zompixel.sprites import SpriteSheet
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class TitleScreen(object):
    """Menu principal"""

    def __init__(self):
        pygame.init()
        self.width = constants.GAME_WIDTH
        self.height = constants.GAME_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ZompiGame")
        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()

        self.is_mouse_button_down = False

        self.hud_font = None
        self.test_font0 = None
        self.welcome_font0 = None
        self.welcome_font1 = None
        self.final_score_font = None
        self.final_score_font1 = None

        self.obstacles_images = {}
        self.game_images = {}
        self.sprite_sheet = SpriteSheet()
        self.character_images = constants.character_images

    def __getitem__(self):
        return self.width

    def text_blit(self, font, text, text_color, pos):
        """Pose du text sur l'arrière plan"""
        text_to_blit = font.render(text, 1, text_color)
        text_to_blit_pos = text_to_blit.get_rect(centerx=pos[0], centery=pos[1])
        self.background.blit(text_to_blit, text_to_blit_pos)

    #########################################
    """Initialisation du jeux"""
    #########################################

    def start(self):
        """Initialiser le jeu et le démarre"""
        self.font_init()
        self.loading_screen()
        self.load_all_images()
        self.title_screen()

    def font_init(self):
        """Initialise les polices du jeu"""
        LOGGER.info("[*] Load Font")
        # Font pour l'acceuil
        self.welcome_font0 = pygame.font.Font("data/fonts/visitor1.ttf", 110)
        self.welcome_font1 = pygame.font.Font("data/fonts/visitor1.ttf", 55)
        # Font pour le résultat en fin de niveau
        self.final_score_font = pygame.font.Font("data/fonts/visitor1.ttf", 30)
        self.final_score_font1 = pygame.font.Font("data/fonts/visitor1.ttf", 40)
        # Font affichage hud/ath
        self.hud_font = pygame.font.Font("data/fonts/visitor1.ttf", 25)
        # Font de test
        self.test_font0 = pygame.font.Font("data/fonts/visitor1.ttf", 15)

    def loading_screen(self):
        """Affiche l'écran de chargement"""
        self.text_blit(
            self.welcome_font0,
            "Loading",
            (100, 20, 20),
            (self.background.get_width() / 2, self.background.get_height() / 2),
        )

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def load_all_images(self):
        """Charge toutes les images du jeu"""
        # Game images
        LOGGER.info("[*] Load Game Images")
        self.game_images["map"] = pygame.image.load("data/img/map.png").convert()
        self.game_images["welcome_background_image"] = pygame.image.load(
            "data/img/title_screen.png"
        ).convert()
        self.game_images["score_image"] = pygame.image.load(
            "data/img/score_background0.png"
        )
        self.game_images["game_over_image"] = pygame.image.load(
            "data/img/game_over_background.png"
        )
        self.game_images["skull_image"] = pygame.image.load("data/img/objets/skull.png")
        self.game_images["hud"] = pygame.image.load("data/img/hud.png")
        self.game_images["map_choice_park"] = pygame.image.load(
            "data/img/survival_map_choice_park.png"
        )
        self.game_images["map_choice_street"] = pygame.image.load(
            "data/img/survival_map_choice_street.png"
        )

        # Characters images
        LOGGER.info("[*] Load PNJ Images")
        self.sprite_sheet.set_img(constants.player_img)
        self.character_images["player"] = self.get_frames(
            self.character_images["player"], "player"
        )

        self.sprite_sheet.set_img(constants.npc["citizen"]["img"])
        self.character_images["citizen"] = self.get_frames(
            self.character_images["citizen"], "citizen"
        )

        self.sprite_sheet.set_img(constants.npc["punk"]["img"])
        self.character_images["punk"] = self.get_frames(
            self.character_images["punk"], "punk"
        )

        self.sprite_sheet.set_img(constants.npc["citizen"]["zombie_img"])
        self.character_images["z_citizen"] = self.get_frames(
            self.character_images["z_citizen"], "z_citizen"
        )

        self.sprite_sheet.set_img(constants.npc["punk"]["zombie_img"])
        self.character_images["z_punk"] = self.get_frames(
            self.character_images["z_punk"], "z_punk"
        )

        # Objects images
        LOGGER.info("[*] Load Obstacles Images")
        for obstacle in constants.OBSTACLES:
            self.obstacles_images[obstacle] = pygame.image.load(
                constants.OBSTACLES[obstacle][0]
            )

    def get_frames(self, character, name):
        character["walking_frames_left"] = self.sprite_sheet.get_character_frames(
            character["walking_frames_left"], constants.MOVING_SPRITE_X, 0, 75, 125
        )

        character["walking_frames_right"] = self.sprite_sheet.get_character_frames(
            character["walking_frames_right"],
            constants.MOVING_SPRITE_X,
            0,
            75,
            125,
            True,
        )

        character["walking_frames_up"] = self.sprite_sheet.get_character_frames(
            character["walking_frames_up"], constants.MOVING_SPRITE_X, 125, 75, 125
        )

        character["walking_frames_down"] = self.sprite_sheet.get_character_frames(
            character["walking_frames_down"], constants.MOVING_SPRITE_X, 250, 75, 125
        )

        character["stop_frame"] = self.sprite_sheet.get_image(
            0, 375, 75, 125, self.sprite_sheet.sheet
        )

        if (
            name != "player" and "z_" not in name
        ):  # si le personnage est un citoyen (!player/!zombie)
            character["attack"]["by_player"] = self.get_action_frames(
                constants.npc[name]["attack_by_player"]
            )
            character["attack"]["by_citizen"] = self.get_action_frames(
                constants.npc[name]["attack_by_citizen"]
            )
            character["attack"]["by_punk"] = self.get_action_frames(
                constants.npc[name]["attack_by_punk"]
            )

        return character

    def get_action_frames(self, file_name):
        frames = []
        self.sprite_sheet.set_img(file_name)
        frames = self.sprite_sheet.get_character_frames(
            frames, constants.DYING_SPRITE_X, 0, 125, 125
        )
        return frames

    #########################################
    """Ecran d'Accueil"""
    #########################################

    def title_screen_text(self):
        """Initialise et pose sur le fond les texts de l'ecran d'accueil"""
        self.text_blit(
            self.welcome_font0,
            "z.o.m.p.i.g.a.m.e",
            (100, 20, 20),
            (self.background.get_width() / 2, 120),
        )
        self.text_blit(
            self.welcome_font1,
            "Campagne",
            (100, 20, 20),
            (self.background.get_width() / 1.975, 300),
        )
        self.text_blit(
            self.welcome_font1,
            "Survie",
            (100, 20, 20),
            (self.background.get_width() / 1.975, 400),
        )
        self.text_blit(
            self.welcome_font1,
            "Info",
            (100, 20, 20),
            (self.background.get_width() / 2, 500),
        )

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        LOGGER.info("[*] Title Screen Init")
        title_screen = True
        self.background.fill((0, 0, 0))
        self.title_screen_text()

        self.window.blit(self.background, (0, 0))

        button_campagne = pygame.draw.rect(
            self.window,
            [100, 20, 20],
            [self.background.get_width() / 2.72, 275, 280, 50],
            2,
        )
        button_survival = pygame.draw.rect(
            self.window,
            [100, 20, 20],
            [self.background.get_width() / 2.43, 375, 190, 50],
            2,
        )
        button_question_mark = pygame.draw.rect(
            self.window,
            [100, 20, 20],
            [self.background.get_width() / 2.34, 473, 145, 50],
            2,
        )

        pygame.display.flip()
        LOGGER.info("     - Ok")

        while title_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_campagne = button_campagne.collidepoint(mouse_xy)
            is_survival = button_survival.collidepoint(mouse_xy)
            is_help = button_question_mark.collidepoint(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_campagne:
                    title_screen = False
                    LOGGER.info("[*] Launch Campagne")
                    campagne = Campagne(self)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_survival:
                    title_screen = False
                    LOGGER.info("[*] Launch Survival")
                    survival = Survival(self)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_help:
                    self.help_screen()

    def help_screen_text(self):
        """Initialise et pose sur le fond les texts de l'ecran d'info"""
        self.text_blit(
            self.final_score_font1,
            "Campagne:",
            (100, 20, 20),
            (self.background.get_width() / 2, 50),
        )

        self.text_blit(
            self.final_score_font,
            "But: Manger les citoyens en moins de 30 secondes !",
            (100, 20, 20),
            (self.background.get_width() / 2, 80),
        )

        self.text_blit(
            self.final_score_font,
            "Le niveau zero vous servira d'entrainement ;)",
            (100, 20, 20),
            (self.background.get_width() / 2, 110),
        )

        self.text_blit(
            self.final_score_font1,
            "Survival:",
            (100, 20, 20),
            (self.background.get_width() / 2, 200),
        )

        self.text_blit(
            self.final_score_font,
            "Vous avez deux minutes pour manger le plus de citoyens",
            (100, 20, 20),
            (self.background.get_width() / 2, 230),
        )

        self.text_blit(
            self.final_score_font,
            "A chaque fois que vous en tuerez un, un autre apparaitras",
            (100, 20, 20),
            (self.background.get_width() / 2, 260),
        )

        self.text_blit(
            self.final_score_font,
            "Toute les vingt secondes, le nomrbe de citoyen augmentera",
            (100, 20, 20),
            (self.background.get_width() / 2, 290),
        )

        self.text_blit(
            self.final_score_font1,
            "General:",
            (100, 20, 20),
            (self.background.get_width() / 2, 400),
        )

        self.text_blit(
            self.final_score_font,
            "Si vous mangez un citoyen: +2 points.",
            (100, 20, 20),
            (self.background.get_width() / 2, 430),
        )

        self.text_blit(
            self.final_score_font,
            "Si l'un de vos zompies mange un citoyen: +1 point.",
            (100, 20, 20),
            (self.background.get_width() / 2, 460),
        )

        self.text_blit(
            self.final_score_font,
            "Cliquez pour deplacer le zompie principal.",
            (100, 20, 20),
            (self.background.get_width() / 2, 490),
        )

        self.text_blit(
            self.final_score_font,
            "Ou restez appuyer, il suivra votre souris.",
            (100, 20, 20),
            (self.background.get_width() / 2, 520),
        )

        self.text_blit(
            self.final_score_font,
            "Les bouches d'egouts sont des pieges mortels.",
            (100, 20, 20),
            (self.background.get_width() / 2, 550),
        )

        self.text_blit(
            self.welcome_font1,
            "Retour",
            (100, 20, 20),
            (self.background.get_width() / 2, 700),
        )

    def help_screen(self):
        """Boucle de l'écran d'aide"""
        LOGGER.info("[*] Help Screen")
        help_screen = True
        self.background.fill((0, 0, 0))

        self.help_screen_text()

        self.window.blit(self.background, (0, 0))

        button_back = pygame.draw.rect(
            self.window,
            [100, 20, 20],
            [self.background.get_width() / 2.55, 675, 215, 50],
            2,
        )

        pygame.display.flip()

        while help_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN and is_back:
                    help_screen = False
                    LOGGER.info("[*] Leaving Help Screen")
                    self.title_screen()
