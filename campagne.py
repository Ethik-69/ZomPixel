#!/usr/bin/env python
# -*- coding:utf-8 -*-
from levels import *
from time_made_home import *
from player import *


class Campagne(object):
    def __init__(self, main):
        self.width = main.width
        self.height = main.height

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
        """Creation du joueur"""
        print('[*] Player Init')
        self.player = Player('player',
                             self.character_images['player'],
                             self.all_sprites,
                             512, 354,
                             self.width, self.height)
        self.time.add_rebour('player')
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

    # ------------Fin de niveau--------------

    def init_score_screen(self):
        """Initialisation de l'affichage du score en fin de niveau"""
        print('[*] Init Display Score')
        time = self.time.chronos['current_level'].Time  # temp qu'a mis le joueur pour terminer le niveau

        # Pose l'image destinée au score
        self.background.blit(self.game_images['score_image'], (self.width/3, self.height/13))

        # Définit et pose les texts
        self.text_blit(self.final_score_font,
                       str(self.player.score) + " Points",
                       (255, 255, 255), (self.width/2, self.height/1.8))

        self.text_blit(self.final_score_font,
                       "Termine en",
                       (255, 255, 255), (self.width/2, self.height/1.6))

        self.text_blit(self.final_score_font,
                       str(time[0]) + ':' + str(time[1]) + ':' + str(time[2]),
                       (255, 255, 255), (self.width/2, self.height/1.5))

        self.text_blit(self.final_score_font,
                       "Niveau suivant",
                       (255, 255, 255), (self.width/2, self.height/1.3))

        # Pose le bouton niveau suivant
        self.button_next_level = pygame.draw.rect(self.window, [0, 0, 0],
                                                  [self.background.get_width()/2.6, self.height/1.4, 250, 50])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

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
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_lvl_change:
                    self.player.score = 0
                    self.click_pos_x = 0
                    self.click_pos_y = 0
                    self.is_display_score = False

            pygame.display.flip()

    # --------------Mort Joueur--------------

    def init_game_over(self):
        print('[*] Init Game Over')
        # Pose l'image
        self.background.blit(self.game_images['game_over_image'], (self.width/6.6, self.height/3.5))
        self.background.blit(self.game_images['skull_image'], (self.width/3.15, self.height/2.1))
        self.background.blit(self.game_images['skull_image'], (self.width/1.55, self.height/2.1))

        # Définit et pose les texts
        self.text_blit(self.final_score_font, "Vous etes definitivement",
                       (255, 255, 255), (self.width/2, self.height/2.4))

        self.text_blit(self.welcome_font1, "M.O.R.T",
                       (255, 255, 255), (self.width/2, self.height/2.1))

        self.text_blit(self.final_score_font, 'Score final: ' + str(self.player.final_score),
                       (255, 255, 255), (self.width/2, self.height/1.8))

        self.text_blit(self.final_score_font, 'Accueil',
                       (255, 255, 255), (self.width/2, self.height/1.435))

        # Pose le bouton retour accueil
        self.button_accueil = pygame.draw.rect(self.window, [0, 0, 0],
                                               [self.background.get_width()/2.35, self.height/1.5, 145, 45])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def init_time_out(self):
        print('[*] Init Time Out')
        # Pose l'image
        self.background.blit(self.game_images['game_over_image'], (self.width/6.6, self.height/3.5))
        self.background.blit(self.game_images['skull_image'], (self.width/3.15, self.height/2.1))
        self.background.blit(self.game_images['skull_image'], (self.width/1.55, self.height/2.1))

        # Définit et pose les texts
        self.text_blit(self.welcome_font1, "Temps ecoule",
                       (255, 255, 255), (self.width/2, self.height/2.3))

        self.text_blit(self.final_score_font, 'Score final: ' + str(self.player.final_score),
                       (255, 255, 255), (self.width/2, self.height/1.95))

        self.text_blit(self.final_score_font, 'Accueil',
                       (255, 255, 255), (self.width/2, self.height/1.435))

        # Pose le bouton retour accueil
        self.button_accueil = pygame.draw.rect(self.window, [0, 0, 0],
                                               [self.background.get_width()/2.35, self.height/1.5, 145, 45])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def display_game_over(self, end_type):
        self.is_game_over = True

        if end_type == 'game_over':
            self.init_game_over()
        else:
            self.init_time_out()

        while self.is_game_over:
            self.display_hud()
            mouse_xy = pygame.mouse.get_pos()
            is_accueil = self.button_accueil.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_accueil:
                    self.is_game_over = False
                    self.end_game()

            pygame.display.flip()

    def init_credit(self):
        print('[*] Init Game Over')
        self.background.fill((0, 0, 0))

        # Définit et pose les texts
        self.text_blit(self.welcome_font1, "Pre-Alpha terminee !",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 100))

        self.text_blit(self.final_score_font, "Votre score final est de " + str(self.player.final_score),
                       (100, 20, 20), (constants.GAME_WIDTH/2, 200))

        self.text_blit(self.final_score_font, "Rejoignez nous sur Facebook: ZompiGame !",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 300))

        self.text_blit(self.final_score_font, "Cree par:",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 400))

        self.text_blit(self.final_score_font, "Ethan CHAMIK",
                       (100, 20, 20), (constants.GAME_WIDTH/5, 500))

        self.text_blit(self.final_score_font, "Thibault DESCAMPS",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 500))

        self.text_blit(self.final_score_font, "Romain GUILLOT",
                       (100, 20, 20), (constants.GAME_WIDTH/1.2, 500))

        self.text_blit(self.final_score_font, "Faites tournez ;)",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 600))

        self.text_blit(self.welcome_font1, "Retour",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 700))

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def display_credit(self):
        print('[*] Credit')
        self.is_credit = True
        self.background.fill((0, 0, 0))

        self.init_credit()

        self.window.blit(self.background, (0, 0))

        button_back = pygame.draw.rect(self.window, [100, 20, 20], [self.background.get_width()/2.55, 675, 215, 50], 2)

        pygame.display.flip()

        while self.is_credit:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_back:
                    self.is_credit = False
                    print('[*] Leaving Credit')
                    self.end_game()

    def end_game(self):
        print('[*] Campagne End')
        self.run = False

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

    def layer_change(self):
        if self.player.is_layer_change:
            print('[*] Change Player Layer')
            self.all_sprites.change_layer(self.player, constants.LAYER_POS[self.player.pos_on_layer])
            self.player.is_layer_change = False
        for pnj in self.pnj_sprites:
            if pnj.is_layer_change:
                print('[*] Change ' + pnj.name + ' Layer')
                self.all_sprites.change_layer(pnj, constants.LAYER_POS[pnj.pos_on_layer])
                pnj.is_layer_change = False

    def test(self):
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
        print('[*] Launch Campagne')
        self.run = True
        self.levels.current_level.start()

        print('[*] Start')
        while self.run:
            mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
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
            self.pnj_sprites.update(self.levels.current_level.obstacles.objects_list)
            self.player.update(self.levels.current_level.obstacles.objects_list)
            self.levels.current_level.update()

            if self.player.dying:
                self.display_game_over('game_over')

            self.layer_change()

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()

            self.levels.current_level.obstacles.objects_list.draw(self.window)

            self.all_sprites.draw(self.window)

            # self.test()
            self.display_credit()
            # -----------------------Change Lvl------------------------

            if self.levels.current_level.is_change_level:
                print('[*] Level End')
                self.levels.current_level.pnj.remove_zombie()
                self.levels.current_level.is_change_level = False
                self.display_score()
                self.levels = self.levels.current_level.next_level()
                if not self.levels:
                    print('[*] Game End')
                    self.display_credit()
                else:
                    self.levels.current_level.start()
                    print('[*] Current Level Number' + str(self.levels.current_level_number))

            # ----------------------------------------------------------

            pygame.display.flip()
            self.clock.tick(100)
        print('[*] Fin de la boucle Campagne')