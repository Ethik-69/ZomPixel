#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from campagne import *
__author__ = "Thibault, Romain -> images Ethan -> Code"

try:
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)


class Game(object):
    """Class principal"""
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

        self.obstacles_images = {}
        self.game_images = {}
        self.sprite_sheet = SpriteSheet()
        self.character_images = constants.character_images

        self.button_next_level = None
        self.button_accueil = None

    def __getitem__(self):
        return self.width

    def text_blit(self, font, text, text_color, pos):
        text_to_blit = font.render(text, 1, text_color)
        text_to_blit_pos = text_to_blit.get_rect(centerx=pos[0], centery=pos[1])
        self.background.blit(text_to_blit, text_to_blit_pos)

    #########################################
    """Ecran d'Accueil"""
    #########################################

    def title_screen_text(self):
        """Initialise et pose sur le fond les texts de l'ecran d'accueil"""
        self.text_blit(self.welcome_font0, "z.o.m.p.i.g.a.m.e", (100, 20, 20), (self.background.get_width()/2, 120))
        self.text_blit(self.welcome_font1, "Campagne", (0, 0, 0), (self.background.get_width()/1.975, 400))
        self.text_blit(self.welcome_font1, "Survie", (0, 0, 0), (self.background.get_width()/1.975, 600))
        self.text_blit(self.welcome_font1, "?", (0, 0, 0), (self.background.get_width()/1.095, 660))

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        print('[*] Title Screen Init')
        title_screen = True
        self.background.blit(self.game_images['welcome_background_image'], (0, 0))
        button_campagne = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.7, 380, 280, 50])
        button_survival = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.7, 580, 280, 50])
        button_question_mark = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/1.14, 625, 75, 75])

        self.title_screen_text()

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()
        print('     - Ok')

        while title_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_campagne = button_campagne.collidepoint(mouse_xy)
            is_survival = button_survival.collidepoint(mouse_xy)
            is_help = button_question_mark.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_campagne:
                    title_screen = False
                    print('[*] Launch Campagne')
                    campagne = Campagne(self)
                elif event.type == MOUSEBUTTONDOWN and is_survival:
                    title_screen = False
                    print('[*] Launch Survival')
                elif event.type == MOUSEBUTTONDOWN and is_help:
                    self.help_screen()

    def help_screen_text(self):
        """Initialise et pose sur le fond les texts de l'ecran d'aide"""
        self.text_blit(self.welcome_font1,
                       "z.o.m.p.i.g.a.m.e",
                       (100, 20, 20), (self.background.get_width()/2, 50))

        self.text_blit(self.final_score_font,
                       "But: Manger les citoyens en moins de 30 secondes !",
                       (100, 20, 20), (self.background.get_width()/2, 150))

        self.text_blit(self.final_score_font,
                       "Si vous mangez un citoyen: +2 points.",
                       (100, 20, 20), (self.background.get_width()/2, 200))

        self.text_blit(self.final_score_font,
                       "Si l'un de vos zompies mange un citoyen: +1 point.",
                       (100, 20, 20), (self.background.get_width()/2, 250))

        self.text_blit(self.final_score_font,
                       "Cliquez pour deplacer le zompie principal.",
                       (100, 20, 20), (self.background.get_width()/2, 300))

        self.text_blit(self.final_score_font,
                       "Ou restez appuyer, il suivra votre souris.",
                       (100, 20, 20), (self.background.get_width()/2, 350))

        self.text_blit(self.final_score_font,
                       "Les bouches d'egouts sont des pieges mortels.",
                       (100, 20, 20), (self.background.get_width()/2, 400))

        self.text_blit(self.final_score_font,
                       "Le niveau zero vous servira d'entrainement ;)",
                       (100, 20, 20), (self.background.get_width()/2, 450))

        self.text_blit(self.final_score_font,
                       "Facebook: ZompiGame",
                       (100, 20, 20), (self.background.get_width()/2, 650))

        self.text_blit(self.welcome_font1,
                       "Retour",
                       (100, 20, 20), (self.background.get_width()/2, 700))

    def help_screen(self):
        """Boucle de l'écran d'aide"""
        print('[*] Help Screen')
        help_screen = True
        self.background.fill((0, 0, 0))

        button_back = pygame.draw.rect(self.window, [255, 255, 255], [self.background.get_width()/2.7, 609, 280, 106])
        self.help_screen_text()

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        while help_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_back:
                    help_screen = False
                    print('[*] Leaving Help Screen')
                    self.title_screen()

    #########################################
    """Initialisation du jeux"""
    #########################################

    def start(self):
        """Fini d'initialiser le jeu et le démarre"""
        self.font_init()
        self.loading_screen()
        self.load_all_images()
        self.title_screen()

    def font_init(self):
        print('[*] Load Font')
        # Font pour l'acceuil
        self.welcome_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 110)
        self.welcome_font1 = pygame.font.Font('data/fonts/visitor1.ttf', 55)
        # Font pour le résultat en fin de niveau
        self.final_score_font = pygame.font.Font('data/fonts/visitor1.ttf', 30)
        # Font affichage hud/ath
        self.hud_font = pygame.font.Font('data/fonts/visitor1.ttf', 25)
        # Font de test
        self.test_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 15)

    def loading_screen(self):
        self.text_blit(self.welcome_font0,
                       "Loading",
                       (100, 20, 20),
                       (self.background.get_width()/2, self.background.get_height()/2))

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def load_all_images(self):
        # Game images
        print('[*] Load Game Images')
        self.game_images['map'] = pygame.image.load('data/img/map.png').convert()
        self.game_images['welcome_background_image'] = pygame.image.load('data/img/title_screen.png').convert()
        self.game_images['score_image'] = pygame.image.load('data/img/score_background0.png')
        self.game_images['game_over_image'] = pygame.image.load('data/img/game_over_background.png')
        self.game_images['skull_image'] = pygame.image.load('data/img/objets/skull.png')
        self.game_images['hud'] = pygame.image.load('data/img/hud.png')

        # Characters images
        print('[*] Load PNJ Images')
        self.sprite_sheet.set_img(constants.player_img)
        self.character_images['player'] = self.get_frames(self.character_images['player'], 'player')

        self.sprite_sheet.set_img(constants.npc['citizen']['img'])
        self.character_images['citizen'] = self.get_frames(self.character_images['citizen'], 'citizen')

        self.sprite_sheet.set_img(constants.npc['punk']['img'])
        self.character_images['punk'] = self.get_frames(self.character_images['punk'], 'punk')

        self.sprite_sheet.set_img(constants.npc['citizen']['zombie_img'])
        self.character_images['z_citizen'] = self.get_frames(self.character_images['z_citizen'], 'z_citizen')

        self.sprite_sheet.set_img(constants.npc['punk']['zombie_img'])
        self.character_images['z_punk'] = self.get_frames(self.character_images['z_punk'], 'z_punk')

        # Objects images
        print('[*] Load Obstacles Images')
        for obstacle in constants.OBSTACLES:
            self.obstacles_images[obstacle] = pygame.image.load(constants.OBSTACLES[obstacle][0])

    def get_frames(self, character, name):
        character['walkingFramesLeft'] = self.sprite_sheet.get_character_frames(character['walkingFramesLeft'],
                                                                                constants.MOVING_SPRITE_X,
                                                                                0, 75, 125)

        character['walkingFramesRight'] = self.sprite_sheet.get_character_frames(character['walkingFramesRight'],
                                                                                 constants.MOVING_SPRITE_X,
                                                                                 0, 75, 125, True)

        character['walkingFramesUp'] = self.sprite_sheet.get_character_frames(character['walkingFramesUp'],
                                                                              constants.MOVING_SPRITE_X,
                                                                              125, 75, 125)

        character['walkingFramesDown'] = self.sprite_sheet.get_character_frames(character['walkingFramesDown'],
                                                                                constants.MOVING_SPRITE_X,
                                                                                250, 75, 125)

        character['stopFrame'] = self.sprite_sheet.get_image(0, 375, 75, 125, self.sprite_sheet.sheet)

        if name != 'player' and 'z_' not in name:
            character['attack']['by_player'] = self.get_action_frames(constants.npc[name]['attack_by_player'])
            character['attack']['by_citizen'] = self.get_action_frames(constants.npc[name]['attack_by_citizen'])
            character['attack']['by_punk'] = self.get_action_frames(constants.npc[name]['attack_by_punk'])

        return character

    def get_action_frames(self, file_name):
        frames = []
        self.sprite_sheet.set_img(file_name)
        frames = self.sprite_sheet.get_character_frames(frames,
                                                        constants.DYING_SPRITE_X,
                                                        0, 125, 125)
        return frames


if __name__ == '__main__':
    while True:
        print('[*] Game Object Init')
        game = Game()
        game.start()

    # TODO: if coli_rect.top > coli_rect_pnj.top: pnj.layer += 1
    # TODO: mode survie (enemy qui arrive indefiniment (+ temp en attendant les militaires)) avec deux maps au choix
    # Mettre l'acceuil dans un fichier ---- A vérifier
    # Mode actuel dans un autre --- A vérifier
    # Nouveau fichier pour le mode survie
    # Modification du menu (img)
    # Posibilité de choisir la carte (Rue ou Park)
    # Des enemy qui arrive indéfiniment avec un temp (if len(pnj) < 10: create pnj)
    #      //         //   de chaque cotés aléatoirement
    # Une image de fin avec le temp et le score
    # TODO: Passer devant et derriere les objets et les pnjs (layer)
    # TODO: boutons -> vrai boutons
    # TODO: Refacto !
    # TODO: Recherche 'IA'

    # RETOUR: - Plus nerveux
        #     - Amélioration collision
