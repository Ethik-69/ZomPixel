#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Thibault, Romain -> images Ethan -> Code"
from tests import *
from levels import *
from time_made_home import *
from player import *
from Character import *
from pygame.locals import *


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
        self.display_score = None
        self.enemy_hit_list = None
        self.is_mouse_button_down = False
        self.game_background_image = None
        self.accueil_background_image = None

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.font_init()
        self.game_init()
        self.title_screen()

    def font_init(self):
        """Initialise les polices"""
        print('[*] Font Init')
        # Font pour l'acceuil
        self.accueil_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 110)
        self.accueil_font1 = pygame.font.Font('data/fonts/visitor1.ttf', 55)
        # Font pour le score
        self.score_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 30)
        # Font de test
        self.test_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 15)
        print('     - Ok')

    def game_init(self):
        # Charge les images utiliser dans le jeu (pas toute pour le moment)
        print('[*] Load Images')
        self.accueil_background_image = pygame.image.load('data/img/title_screen.png').convert()
        self.score_image = pygame.image.load('data/img/score_background0.png')
        print('     - Ok')

        self.create_player()

        print('[*] Levels Init')
        self.levels = Levels(self)
        self.levels.init_level()
        print('[*] Levels Init Ok')

    #########################################
    """Ecran d'Accueil"""
    #########################################

    def title_screen_text(self):
        """Affiche les texts de l'ecran d'accueil"""
        title = self.accueil_font0.render("Z.o.m.P.i.x.e.l", 1, (100, 20, 20))
        title_pos = title.get_rect(centerx=self.background.get_width()/2, centery=120)
        self.background.blit(title, title_pos)

        label_demarrer = self.accueil_font1.render("Demarrer", 1, (0, 0, 0))
        label_demarrer_pos = label_demarrer.get_rect(centerx=self.background.get_width()/2, centery=660)
        self.background.blit(label_demarrer, label_demarrer_pos)

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        print('[*] Title Screen Init')
        title_screen = True
        self.background.blit(self.accueil_background_image, (0, 0))
        button_demarrer = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.7, 609, 280, 106])

        self.title_screen_text()

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()

        print('     - Ok')

        while title_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_demarrer = button_demarrer.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_demarrer:
                    title_screen = False
                    print('[*] Leaving Title Screen')

        self.main()

    #########################################
    """Initialisation du jeux"""
    #########################################

    def create_player(self):
        """Creation des groupe de sprites et du joueur"""
        print('[*] Player Init')
        self.player_sprite = pygame.sprite.Group()
        self.player = Player(self, 'zombie', 'character/zombie_sprite_sheet.png', 512, 354)
        self.player_sprite.add(self.player)
        print('     - Ok')

    #########################################
    """Gestion évènements"""
    #########################################

    # -------------Déplacements--------------

    def click_motion(self):
        """Gestion du click"""
        if self.click_pos_x is not None and self.click_pos_x < self.player.rect.x:
            self.player.action = 'left'
            self.player.move_left()
        if self.click_pos_x is not None and self.click_pos_x > self.player.rect.x:
            self.player.action = 'right'
            self.player.move_right()
        if self.click_pos_y is not None and self.click_pos_y < self.player.rect.y:
            self.player.action = 'up'
            self.player.move_up()
        if self.click_pos_y is not None and self.click_pos_y > self.player.rect.y:
            self.player.action = 'down'
            self.player.move_down()
        if self.click_pos_x == self.player.rect.x:
            self.player.moveX = 0
            self.click_pos_x = None
        if self.click_pos_y == self.player.rect.y:
            self.player.moveY = 0
            self.click_pos_y = None
        if self.click_pos_x is None and self.click_pos_y is None:
            self.player.action = ''

    def on_key_down(self, key):
        """Gestion du clavier"""
        if key == K_ESCAPE:
            self.run = False
        if key == K_LEFT:
            self.player.action = 'left'
            self.player.move_left()
        if key == K_RIGHT:
            self.player.action = 'right'
            self.player.move_right()
        if key == K_UP:
            self.player.action = 'up'
            self.player.move_up()
        if key == K_DOWN:
            self.player.action = 'down'
            self.player.move_down()

    def on_key_up(self, key):
        self.player.action = ''
        if key == K_LEFT:
            self.player.moveX = 0
        if key == K_RIGHT:
            self.player.moveX = 0
        if key == K_UP:
            self.player.moveY = 0
        if key == K_DOWN:
            self.player.moveY = 0

    # --------------Collisions---------------

    def collide_test(self):
        """
        Test de collision entre les personnages
        rectangle-rectangle puis au pixel près
        """
        # collision avec le joueur
        if not self.player.is_feeding:
            self.enemy_hit_list = pygame.sprite.spritecollide(self.player, self.levels.current_level.pnj.enemy_list, False)
            for enemy in self.enemy_hit_list:
                print('[*] Rect Collide - Player')
                if pygame.sprite.collide_mask(self.player, enemy) is not None:
                    if not enemy.underAttack and not self.player.is_feeding:
                        print('[*] Mask Collide - Player')
                        enemy.is_under_attack(self.player)
                        self.player.is_feeding = True

        # collsision avec les autres zombies
        for zombie in self.levels.current_level.pnj.zombie_list:
            self.enemy_hit_list = pygame.sprite.spritecollide(zombie, self.levels.current_level.pnj.enemy_list, False)
            for enemy in self.enemy_hit_list:
                print('[*] Rect Collide - Zombie')
                if pygame.sprite.collide_mask(zombie, enemy) is not None:
                    if not enemy.underAttack and not zombie.is_feeding:
                        print('[*] Mask Collide - Zombie')
                        enemy.is_under_attack(zombie)
                        zombie.is_feeding = True

    # ---------------Level end---------------

    def display_player_score(self):
        print('[*] Init Display Score')
        self.display_score = True
        time = self.time.chronos['current_level'].Time # temp qu'a mis le joueur pour terminer le niveau

        # Pose l'image destinée au score
        self.background.blit(self.score_image, (self.width/3, self.height/13))

        # Définit et pose les texts
        label_player_score = self.score_font0.render(str(self.player.score) + ' Points', 1, (255, 255, 255))
        label_player_score_pos = label_player_score.get_rect(centerx=self.width/2, centery=self.height/1.8)
        self.background.blit(label_player_score, label_player_score_pos)

        label_player_time = self.score_font0.render('Terminer en', 1, (255, 255, 255))
        label_player_time_pos = label_player_time.get_rect(centerx=self.width/2, centery=self.height/1.6)
        self.background.blit(label_player_time, label_player_time_pos)

        player_time = self.score_font0.render(str(time[0]) + ':' + str(time[1]) + ':' + str(time[2]), 1, (255, 255, 255))
        player_time_pos = player_time.get_rect(centerx=self.width/2, centery=self.height/1.5)
        self.background.blit(player_time, player_time_pos)

        label_next_level = self.score_font0.render('Niveau suivant', 1, (255, 255, 255))
        label_next_level_pos = label_player_score.get_rect(centerx=self.width/2.2, centery=self.height/1.3)
        self.background.blit(label_next_level, label_next_level_pos)

        # Pose le bouton niveau suivant
        button_next_level = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.6, self.height/1.4, 250, 50])

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()

        print('     - Ok')

        while self.display_score:
            mouse_xy = pygame.mouse.get_pos()
            is_lvl_change = button_next_level.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_lvl_change:
                    self.player.score = 0
                    self.display_score = False

    def fin(self):
        print('[*] Fin')

    #########################################
    """Boucle Principal"""
    #########################################

    def main(self):
        print('[*] Launch Main')
        self.run = True
        self.time0_Fps = time.clock()
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
                elif event.type == KEYDOWN:
                    self.on_key_down(event.key)
                elif event.type == KEYUP:
                    self.on_key_up(event.key)

            if self.is_mouse_button_down:
                self.click_pos_x = mouse_xy[0]
                self.click_pos_y = mouse_xy[1]

            self.click_motion()

            # -------------------------Update--------------------------

            self.collide_test()
            self.time.update()
            self.player.update()
            self.levels.current_level.pnj.update()

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.levels.current_level.pnj.draw()

            # Si le joueur mange ne l'affiche pas
            if not self.player.is_feeding:
                self.player_sprite.draw(self.window)

            test(self)  # affichage données de test

            # -----------------------Change Lvl------------------------

            if self.levels.current_level.is_change_level:
                print('[*] Level End')
                try:
                    self.levels.current_level.pnj.remove_zombie()
                    self.levels.current_level.is_change_level = False
                    self.display_player_score()
                    self.levels = self.levels.current_level.next_level()
                    if not self.levels:
                        self.fin()
                except Exception as E:
                    pass

            # ----------------------------------------------------------

            pygame.display.flip()
            self.clock.tick(100)

if __name__ == '__main__':
    game = Game()
