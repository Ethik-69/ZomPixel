#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Thibault, Romain -> images Ethan -> Code"
import sys
from levels import *
from time_made_home import *
from player import *
from character import *

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
        self.width = 1024
        self.height = 768
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ZomPixel")
        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()

        self.frameCount = 0
        self.frameRate = 0

        self.run = None
        self.levels = None
        self.score_image = None
        self.click_pos_x = None
        self.click_pos_y = None
        self.is_display_score = None
        self.enemy_hit_list = None
        self.obstacles_collided = None
        self.is_mouse_button_down = False

        self.game_background_image = None
        self.welcome_background_image = None

        self.button_next_level = None

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
        self.text_blit(self.welcome_font1, "Demarrer", (0, 0, 0), (self.background.get_width()/2, 660))
        self.text_blit(self.welcome_font1, "?", (0, 0, 0), (self.background.get_width()/1.1, 660))

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        print('[*] Title Screen Init')
        title_screen = True
        self.background.blit(self.welcome_background_image, (0, 0))
        button_start = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.7, 609, 280, 106])
        button_question_mark = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/1.14, 625, 75, 75])

        self.title_screen_text()

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()
        print('     - Ok')

        while title_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_start = button_start.collidepoint(mouse_xy)
            is_help = button_question_mark.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_start:
                    title_screen = False
                    print('[*] Leaving Title Screen')
                elif event.type == MOUSEBUTTONDOWN and is_help:
                    self.help_screen()

        self.main()

    def help_screen_text(self):
        """Initialise et pose sur le fond les texts de l'ecran d'aide"""
        self.text_blit(self.welcome_font1, "z.o.m.p.i.g.a.m.e", (100, 20, 20), (self.background.get_width()/2, 50))
        self.text_blit(self.final_score_font, "But: Manger les citoyens le plus vite possible", (100, 20, 20), (self.background.get_width()/2, 150))
        self.text_blit(self.final_score_font, "Si vous mangez un citoyen: +2 point", (100, 20, 20), (self.background.get_width()/2, 250))
        self.text_blit(self.final_score_font, "Si l'un de vos zombie mange un citoyen: +1 point", (100, 20, 20), (self.background.get_width()/2, 350))
        self.text_blit(self.final_score_font, "Cliquez pour deplacer le zombie principal", (100, 20, 20), (self.background.get_width()/2, 450))
        self.text_blit(self.welcome_font1, "Retour", (100, 20, 20), (self.background.get_width()/2, 700))

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

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.welcome_background_image = pygame.image.load('data/img/title_screen.png').convert()
        self.score_image = pygame.image.load('data/img/score_background0.png')

        self.create_player()
        self.levels = Levels(self)
        self.levels.init_level()
        self.title_screen()

    def font_init(self):
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
        self.text_blit(self.welcome_font0, "Loading", (100, 20, 20), (self.background.get_width()/2, self.background.get_height()/2))

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

    def create_player(self):
        """Creation du joueur"""
        print('[*] Player Init')
        self.player_sprite = pygame.sprite.Group()
        self.player = Player('player', 'character/player/zombie_sprite_sheet.png', 512, 354, self.width, self.height)
        self.time.add_rebour('player')
        self.player_sprite.add(self.player)
        print('     - Ok')

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
                self.player.action = 'left'
                self.player.move_left()
            elif self.click_pos_x > self.player.rect.x:
                self.player.action = 'right'
                self.player.move_right()
        if self.click_pos_y is not None:
            if self.click_pos_y < self.player.rect.y:
                self.player.action = 'up'
                self.player.move_up()
            elif self.click_pos_y > self.player.rect.y:
                self.player.action = 'down'
                self.player.move_down()

        if self.click_pos_x is None and self.click_pos_y is None:
            self.player.action = ''

    # --------------Level end----------------

    def init_score_screen(self):
        """Initialisation de l'affichage du score en fin de niveau"""
        print('[*] Init Display Score')
        time = self.time.chronos['current_level'].Time  # temp qu'a mis le joueur pour terminer le niveau

        # Pose l'image destinée au score
        self.background.blit(self.score_image, (self.width/3, self.height/13))

        # Définit et pose les texts
        self.text_blit(self.final_score_font, str(self.player.score) + " Points", (255, 255, 255), (self.width/2, self.height/1.8))
        self.text_blit(self.final_score_font, "Terminer en", (255, 255, 255), (self.width/2, self.height/1.6))
        self.text_blit(self.final_score_font, str(time[0]) + ':' + str(time[1]) + ':' + str(time[2]), (255, 255, 255), (self.width/2, self.height/1.5))
        self.text_blit(self.final_score_font, "Niveau suivant", (255, 255, 255), (self.width/2, self.height/1.3))

        # Pose le bouton niveau suivant
        self.button_next_level = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.6, self.height/1.4, 250, 50])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def display_score(self):
        """"Boucle de l'affichage du score"""
        self.is_display_score = True
        self.init_score_screen()

        while self.is_display_score:
            mouse_xy = pygame.mouse.get_pos()
            is_lvl_change = self.button_next_level.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_lvl_change:
                    self.player.score = 0
                    self.click_pos_x = 0
                    self.click_pos_y = 0
                    self.is_display_score = False

    def end_game(self):
        print('[*] Start New Game')
        new_game = Game()
        pass

    #########################################
    """Boucle Principal"""
    #########################################

    def display_hud(self):
        """Affichage Tête Haute (score - temps.....)"""
        current_lvl = self.hud_font.render('%s %s' % ('Niveau', self.levels.current_level_number), True, (0, 0, 0))
        score = self.hud_font.render('%s' % self.player.score, True, (0, 0, 0))  # player.score
        time = self.hud_font.render('%s:%s:%s' % (self.time.chronos['current_level'].Time[0],
                                                  self.time.chronos['current_level'].Time[1],
                                                  self.time.chronos['current_level'].Time[2]), True, (0, 0, 0))  # time

        self.window.blit(current_lvl, (50, 14))
        self.window.blit(score, (492, 14))
        self.window.blit(time, (878, 14))

    def main(self):
        print('[*] Launch Main')
        self.run = True
        self.levels.current_level.start()

        while self.run:
            mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.is_mouse_button_down = True
                elif event.type == MOUSEBUTTONUP:
                    self.is_mouse_button_down = False

            # -------------------------Update--------------------------

            if self.is_mouse_button_down:
                self.click_pos_x = mouse_xy[0] - self.player.width / 2
                self.click_pos_y = mouse_xy[1] - self.player.height / 2

            self.click_motion()
            self.time.update()
            self.player.update(self.levels.current_level.obstacles.objects_list)
            self.levels.current_level.pnj.update(self.levels.current_level.obstacles.objects_list)

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()
            self.levels.current_level.pnj.draw()

            # Si le joueur mange, ne l'affiche pas
            if not self.player.is_feeding:
                self.player_sprite.draw(self.window)

            # -----------------------Change Lvl------------------------

            if self.levels.current_level.is_change_level:
                print('[*] Level End')
                self.levels.current_level.pnj.remove_zombie()
                self.levels.current_level.is_change_level = False
                self.display_score()
                self.levels = self.levels.current_level.next_level()
                print(self.levels)
                if not self.levels:
                    print('[*] Game End')
                    self.end_game()

                self.levels.current_level.start()
                print('[*] Current Level Number' + str(self.levels.current_level_number))

            # ----------------------------------------------------------

            pygame.display.flip()
            self.clock.tick(100)

if __name__ == '__main__':
    # import cProfile
    # cProfile.run('Game()')

    # from pycallgraph import PyCallGraph
    # from pycallgraph.output import GraphvizOutput

    # with PyCallGraph(output=GraphvizOutput()):
        game = Game()
        game.start()

    # TODO: Gestion collision objets. (zombie/enemy)
    # TODO: Charger toute les images au debut
    # TODO: Refacto
