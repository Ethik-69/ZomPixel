#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from player import *
from levels import *
from db_manager import *
from time_made_home import *


class Survival(object):
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

        self.hud_font = main.hud_font
        self.welcome_font0 = main.welcome_font0
        self.welcome_font1 = main.welcome_font1
        self.final_score_font = main.final_score_font
        self.final_score_font1 = main.final_score_font1

        self.button_send = None
        self.button_share = None
        self.button_welcome = None

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.frameRate = 0
        self.frameCount = 0

        self.victims = 0
        self.run = None
        self.levels = None
        self.player = None
        self.click_pos_x = None
        self.click_pos_y = None
        self.enemy_hit_list = None
        self.obstacles_collided = None
        self.is_map_choice_screen = None
        self.is_mouse_button_down = None

        self.is_game_over = False
        self.is_result_db = False
        self.is_display_send_db = False

        self.create_player()

        self.map_choice_screen()

    def text_blit(self, font, text, text_color, pos):
        text_to_blit = font.render(text, 1, text_color)
        text_to_blit_pos = text_to_blit.get_rect(centerx=pos[0], centery=pos[1])
        self.background.blit(text_to_blit, text_to_blit_pos)

    def init_map_choice(self):
        """Initialisation de l'écran de choix de la map"""
        self.is_map_choice_screen = True
        self.background.fill((0, 0, 0))

        button_back = pygame.draw.rect(self.window, [255, 255, 255], [constants.GAME_WIDTH/2.7, 609, 280, 106])
        button_park = pygame.draw.rect(self.window, [255, 255, 255], [constants.GAME_WIDTH/1.8, 200, 300, 300])
        button_street = pygame.draw.rect(self.window, [255, 255, 255], [constants.GAME_WIDTH/7, 200, 300, 300])

        self.text_blit(self.final_score_font,
                       "Choisissez une carte",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 100))

        self.text_blit(self.welcome_font1,
                       "Retour",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 700))

        self.background.blit(self.game_images['map_choice_park'], (constants.GAME_WIDTH/1.8, 200))
        self.background.blit(self.game_images['map_choice_street'], (constants.GAME_WIDTH/7, 200))

        self.window.blit(self.background, (0, 0))

        return button_back, button_park, button_street

    def map_choice_screen(self):
        """Boucle du choix de la map"""
        print('[*] Start Map Choice Screen')
        button_back, button_park, button_street = self.init_map_choice()

        pygame.display.flip()

        while self.is_map_choice_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)
            is_park = button_park.collidepoint(mouse_xy)
            is_street = button_street.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_back:
                    self.is_map_choice_screen = False
                    print('[*] Leaving Suvival Mode')
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and is_park:
                    self.is_map_choice_screen = False
                    print('[*] Park Choice')
                    self.main('park')
                elif event.type == pygame.MOUSEBUTTONDOWN and is_street:
                    self.is_map_choice_screen = False
                    print('[*] Street Choice')
                    self.main('street')

    def create_player(self):
        """Creation du joueur"""
        print('[*] Player Init')
        self.player = Player('player',
                             self.character_images['player'],
                             self.all_sprites,
                             512, 354,
                             constants.GAME_WIDTH, constants.GAME_HEIGHT)
        self.time.add_rebour('player')
        print('     - Ok')

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

    def init_game_over(self):
        """Initialise le game over"""
        print('[*] Init Game Over')
        # Pose les images
        self.background.blit(self.game_images['game_over_image'], (constants.GAME_WIDTH/6.6, constants.GAME_HEIGHT/3.5))
        self.background.blit(self.game_images['skull_image'], (constants.GAME_WIDTH/3.15, constants.GAME_HEIGHT/2.1))
        self.background.blit(self.game_images['skull_image'], (constants.GAME_WIDTH/1.55, constants.GAME_HEIGHT/2.1))

        # Définit et pose les texts
        self.text_blit(self.final_score_font, "Vous etes definitivement",
                       (255, 255, 255), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/2.4))

        self.text_blit(self.welcome_font1, "M.O.R.T",
                       (255, 255, 255), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/2.1))

        self.text_blit(self.final_score_font, 'Score final: ' + str(self.player.final_score),
                       (255, 255, 255), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/1.8))

        self.text_blit(self.final_score_font, 'Temp: ' + '%s:%s:%s' % (self.time.chronos['survival'].Time[0],
                                                                       self.time.chronos['survival'].Time[1],
                                                                       self.time.chronos['survival'].Time[2]),
                       (255, 255, 255), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/1.92))

        self.text_blit(self.final_score_font, 'Accueil',
                       (255, 255, 255), (constants.GAME_WIDTH/2.7, constants.GAME_HEIGHT/1.6))

        self.text_blit(self.final_score_font, 'Partager',
                       (255, 255, 255), (constants.GAME_WIDTH/1.7, constants.GAME_HEIGHT/1.65))

        self.text_blit(self.final_score_font, 'mon score',
                       (255, 255, 255), (constants.GAME_WIDTH/1.7, constants.GAME_HEIGHT/1.55))

        self.window.blit(self.background, (0, 0))

        # Pose les boutons de retour à l'accueil et de partage du score
        self.button_welcome = pygame.draw.rect(self.window, [255, 255, 255],
                                               [constants.GAME_WIDTH/3.4, constants.GAME_HEIGHT/1.68, 145, 45], 2)

        self.button_share = pygame.draw.rect(self.window, [255, 255, 255],
                                             [constants.GAME_WIDTH/2.02, constants.GAME_HEIGHT/1.73, 185, 75], 2)

        pygame.display.flip()
        print('     - Ok')

    def display_game_over(self, end_type):
        """Boucle du game over"""
        self.is_game_over = True

        if end_type == 'game_over':
            self.init_game_over()
        elif end_type == 'Time Out':
            self.init_game_over()

        while self.is_game_over:
            self.display_hud()
            mouse_xy = pygame.mouse.get_pos()
            is_welcome = self.button_welcome.collidepoint(mouse_xy)
            is_share = self.button_share.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and is_welcome:
                    self.is_game_over = False
                    self.end_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and is_share:
                    self.is_game_over = False
                    self.is_display_send_db = True
                    self.display_send_to_db()

            pygame.display.flip()

    def draw_send_to_db(self, current_string):
        """
        Affichage de l'écran d'envoi du score
        Est appeler à chaque tour de boucle pour afficher ce que l'utilisateur tape
        """
        self.background.fill((0, 0, 0))

        self.text_blit(self.welcome_font1, 'Entrez votre nom',
                       (100, 20, 20), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/3.5))

        self.text_blit(self.final_score_font, 'Envoyer',
                       (100, 20, 20), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/1.5))

        if len(current_string) != 0:
            self.text_blit(self.final_score_font1, current_string,
                           (255, 255, 255), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/2.3))

        self.window.blit(self.background, (0, 0))

        self.button_send = pygame.draw.rect(self.window, [100, 20, 20],
                                            [constants.GAME_WIDTH/2.34, constants.GAME_HEIGHT/1.548, 145, 30], 2)

    def display_send_to_db(self):
        """Boucle de l'écran d'envoi du score à la DB"""
        current_string = []
        self.draw_send_to_db(current_string)

        while self.is_display_send_db:
            mouse_xy = pygame.mouse.get_pos()
            is_send = self.button_send.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    elif event.key == pygame.K_BACKSPACE:
                        current_string = current_string[0:-1]
                    elif event.key == pygame.K_RETURN:
                        self.is_display_send_db = False
                        self.final_send_to_db(''.join(current_string))
                    elif event.key == pygame.K_MINUS:
                        current_string.append("_")
                    elif event.key <= 127:
                        current_string.append(chr(event.key))
                elif event.type == pygame.MOUSEBUTTONDOWN and is_send:
                    self.is_display_send_db = False
                    self.final_send_to_db(''.join(current_string))

            self.draw_send_to_db(''.join(current_string))
            pygame.display.flip()

    def final_send_to_db(self, player_name):
        """Envoi le nom, le score, le temp et le nombre de victimes à la DB"""
        print('[*] Send to DB')
        data_base = DataBase()
        if player_name is not None:
            data_base.create_connection()
            if data_base.connection is not None:
                data_base.make_full_insert(player_name,
                                           self.player.final_score,
                                           '%s:%s:%s' % (self.time.chronos['survival'].Time[0],
                                                         self.time.chronos['survival'].Time[1],
                                                         self.time.chronos['survival'].Time[2]),
                                           self.victims)
                data_base.close_connection()
                self.send_result('Envoi reussi')
            else:
                self.send_result('Envoi echoue')
        else:
            self.display_send_to_db()

    def send_result(self, text):
        """Boucle d'affiche du résultat de l'envoi (réussi/échoué)"""
        self.is_result_db = True
        self.background.fill((0, 0, 0))

        self.text_blit(self.welcome_font1, text,
                       (100, 20, 20), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/2.5))

        self.text_blit(self.final_score_font, 'Accueil',
                       (100, 20, 20), (constants.GAME_WIDTH/2, constants.GAME_HEIGHT/1.5))

        self.window.blit(self.background, (0, 0))

        self.button_welcome = pygame.draw.rect(self.window, [100, 20, 20],
                                               [constants.GAME_WIDTH/2.34, constants.GAME_HEIGHT/1.548, 145, 30], 2)

        pygame.display.flip()

        while self.is_result_db:
            mouse_xy = pygame.mouse.get_pos()
            is_welcome = self.button_welcome.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and is_welcome:
                    self.is_result_db = False
                    self.end_game()

            pygame.display.flip()

    def end_game(self):
        print('[*] Survival End')
        self.run = False

    def display_hud(self):
        """Pose l'ATH (affichage tête haute) (score - temps.....)"""
        nb_victims = self.hud_font.render('%s %s' % ('Mort:', self.victims), True, (0, 0, 0))
        score = self.hud_font.render('%s' % self.player.score, True, (0, 0, 0))
        time = self.hud_font.render('%s:%s:%s' % (self.time.chronos['survival'].Time[0],
                                                  self.time.chronos['survival'].Time[1],
                                                  self.time.chronos['survival'].Time[2]), True, (0, 0, 0))

        self.window.blit(nb_victims, (50, 14))
        self.window.blit(score, (490, 14))
        self.window.blit(time, (878, 14))

    def layer_change(self):
        """Change le joueur et les pnjs de layer"""
        if self.player.is_layer_change:
            print('[*] Change Player Layer')
            self.all_sprites.change_layer(self.player, constants.LAYER_POS[self.player.pos_on_layer])
            self.player.is_layer_change = False
        for pnj in self.pnj_sprites:
            if pnj.is_layer_change:
                print('[*] Change ' + pnj.name + ' Layer')
                self.all_sprites.change_layer(pnj, constants.LAYER_POS[pnj.pos_on_layer])
                pnj.is_layer_change = False

    def test(self, input):
        """Test"""
        if 'hitbox' in input:
            pygame.draw.rect(self.window, (100, 10, 10), self.player.hitbox_rect)
            for pnj in self.enemy_sprites:
                if pnj.is_crazy:
                    pygame.draw.rect(self.window, (255, 255, 255), pnj.hitbox_rect)
                else:
                    pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

            for pnj in self.zombie_sprites:
                pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

        if 'collide' in input:
            pygame.draw.rect(self.window, (100, 10, 10), self.player.collision_rect)
            for pnj in self.enemy_sprites:
                pygame.draw.rect(self.window, (255, 255, 255), pnj.collision_rect)
            for pnj in self.zombie_sprites:
                pygame.draw.rect(self.window, (0, 0, 0), pnj.collision_rect)

        if 'objects' in input:
            for object in self.levels.current_level.obstacles.objects_list:
                pygame.draw.rect(self.window, (0, 0, 0), object.collision_rect)

    def main(self, map_pos):
        """Boucle principal du survival"""
        print('[*] Launch Survival')
        self.levels = Levels(self)
        self.levels.init_survival_level(map_pos)
        self.run = True
        self.levels.current_level.start()

        print('[*] Start')
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
            self.zombie_sprites.update(self.levels.current_level.obstacles.objects_list,
                                       self.enemy_sprites)
            self.player.update(self.levels.current_level.obstacles.objects_list,
                               self.enemy_sprites)
            self.levels.current_level.update()

            if self.player.dying:
                self.display_game_over('game_over')

            self.layer_change()

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()
            self.all_sprites.draw(self.window)

            self.test('hitbox')

            pygame.display.flip()
            self.clock.tick(100)
        print('[*] Fin de la boucle survival')
