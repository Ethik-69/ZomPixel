#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Thibault, Romain -> images Ethan -> Code"
import sys
from levels import *
from time_made_home import *
from player import *
from Character import *

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

        self.button_next_level = None

        # Font pour l'acceuil
        self.welcome_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 110)
        self.welcome_font1 = pygame.font.Font('data/fonts/visitor1.ttf', 55)
        # Font pour le résultat en fin de niveau
        self.final_score_font = pygame.font.Font('data/fonts/visitor1.ttf', 30)
        # Font affichage hud/ath
        self.hud_font = pygame.font.Font('data/fonts/visitor1.ttf', 25)
        # Font de test
        self.test_font0 = pygame.font.Font('data/fonts/visitor1.ttf', 15)

        self.game_background_image = None
        self.welcome_background_image = None

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.welcome_background_image = pygame.image.load('data/img/title_screen.png').convert()
        self.score_image = pygame.image.load('data/img/score_background0.png')

        self.create_player()

        self.levels = Levels(self)
        self.levels.init_level()

        self.title_screen()

    #########################################
    """Ecran d'Accueil"""
    #########################################

    def title_screen_text(self):
        """Affiche les texts de l'ecran d'welcome"""
        title = self.welcome_font0.render("z.o.m.p.i.g.a.m.e", 1, (100, 20, 20))
        title_pos = title.get_rect(centerx=self.background.get_width()/2, centery=120)
        self.background.blit(title, title_pos)

        label_start = self.welcome_font1.render("Demarrer", 1, (0, 0, 0))
        label_start_pos = label_start.get_rect(centerx=self.background.get_width()/2, centery=660)
        self.background.blit(label_start, label_start_pos)
        
        label_question_mark = self.welcome_font1.render("?", 1, (0, 0, 0))
        label_question_mark_pos = label_question_mark.get_rect(centerx=self.background.get_width()/1.1, centery=660)
        self.background.blit(label_question_mark, label_question_mark_pos)

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        print('[*] Title Screen Init')
        title_screen = True
        self.background.blit(self.welcome_background_image, (0, 0))
        button_start = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.7, 609, 280, 106])

        self.title_screen_text()

        self.window.blit(self.background, (0, 0))

        pygame.display.flip()
        print('     - Ok')

        while title_screen:
            mouse_xy = pygame.mouse.get_pos()
            is_start = button_start.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_start:
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

    # --------------Collisions---------------

    def pnj_collide(self):
        """
        Tests de collisions
        rectangle-rectangle puis au pixel près
        """
        # Collision avec le joueur
        if not self.player.is_feeding:
            self.enemy_hit_list = pygame.sprite.spritecollide(self.player,
                                                              self.levels.current_level.pnj.enemy_list,
                                                              False)
            for enemy in self.enemy_hit_list:
                print('[*] Rect Collide - Player')
                if pygame.sprite.collide_mask(self.player, enemy) is not None:
                    if not enemy.underAttack and not self.player.is_feeding:
                        print('[*] Mask Collide - Player')
                        enemy.is_under_attack(self.player)
                        self.player.is_feeding = True

        # Collsision avec les autres zombies
        for zombie in self.levels.current_level.pnj.zombie_list:
            self.enemy_hit_list = pygame.sprite.spritecollide(zombie,
                                                              self.levels.current_level.pnj.enemy_list,
                                                              False)
            for enemy in self.enemy_hit_list:
                print('[*] Rect Collide - Zombie')
                if pygame.sprite.collide_mask(zombie, enemy) is not None:
                    if not enemy.underAttack and not zombie.is_feeding:
                        print('[*] Mask Collide - Zombie')
                        enemy.is_under_attack(zombie)
                        zombie.is_feeding = True

    def obstacle_collide(self):
        # Collision avec les objets (grosse refacto a faire)
        if not self.player.is_feeding:
            self.obstacles_collided = pygame.sprite.spritecollide(self.player,
                                                                  self.levels.current_level.obstacles.objects_list,
                                                                  False)
            for obstacle in self.obstacles_collided:
                print('[*] Collide Object')
                if pygame.sprite.collide_mask(self.player, obstacle) is not None:
                    if self.player.moveX < 0:  # gauche
                        self.player.moveX = 1
                    elif self.player.moveX > 0:  # droite
                        self.player.moveX = -1
                    if self.player.moveY < 0:  # haut
                        self.player.moveY = 1
                    elif self.player.moveY > 0:  # bas
                        self.player.moveY = -1

        for zombie in self.levels.current_level.pnj.zombie_list:
            if not zombie.is_feeding:
                self.obstacles_collided = pygame.sprite.spritecollide(zombie,
                                                                      self.levels.current_level.obstacles.objects_list,
                                                                      False)
                for obstacle in self.obstacles_collided:
                    print('[*] Collide Object')
                    if pygame.sprite.collide_mask(self.player, obstacle) is not None:
                        if zombie.moveX < 0:  # vas vers la gauche
                            zombie.action = 'right'
                        elif zombie.moveX > 0:  # vas vers la droite
                            zombie.action = 'left'
                        if zombie.moveY < 0:  # vas vers le haut
                            zombie.action = 'down'
                        elif zombie.moveY > 0:  # vas vers le bas
                            zombie.action = 'up'        
        
        for enemy in self.levels.current_level.pnj.enemy_list:
            if not enemy.is_under_attack:
                self.obstacles_collided = pygame.sprite.spritecollide(enemy,
                                                                      self.levels.current_level.obstacles.objects_list,
                                                                      False)
                for obstacle in self.obstacles_collided:
                    print('[*] Collide Object')
                    if pygame.sprite.collide_mask(self.player, obstacle) is not None:
                        if enemy.moveX < 0:  # vas vers la gauche
                            enemy.action = 'right'
                        elif enemy.moveX > 0:  # vas vers la droite
                            enemy.action = 'left'
                        if enemy.moveY < 0:  # vas vers le haut
                            enemy.action = 'down'
                        elif enemy.moveY > 0:  # vas vers le bas
                            enemy.action = 'up'

    # ---------------Level end---------------

    def init_score_screen(self):
        print('[*] Init Display Score')
        time = self.time.chronos['current_level'].Time  # temp qu'a mis le joueur pour terminer le niveau

        # Pose l'image destinée au score
        self.background.blit(self.score_image, (self.width/3, self.height/13))

        # Définit et pose les texts
        label_player_score = self.final_score_font.render(str(self.player.score) + ' Points', 1, (255, 255, 255))
        label_player_score_pos = label_player_score.get_rect(centerx=self.width/2, centery=self.height/1.8)
        self.background.blit(label_player_score, label_player_score_pos)

        label_player_time = self.final_score_font.render('Terminer en', 1, (255, 255, 255))
        label_player_time_pos = label_player_time.get_rect(centerx=self.width/2, centery=self.height/1.6)
        self.background.blit(label_player_time, label_player_time_pos)

        player_time = self.final_score_font.render(str(time[0]) + ':' + str(time[1]) + ':' + str(time[2]), 1, (255, 255, 255))
        player_time_pos = player_time.get_rect(centerx=self.width/2, centery=self.height/1.5)
        self.background.blit(player_time, player_time_pos)

        label_next_level = self.final_score_font.render('Niveau suivant', 1, (255, 255, 255))
        label_next_level_pos = label_player_score.get_rect(centerx=self.width/2.2, centery=self.height/1.3)
        self.background.blit(label_next_level, label_next_level_pos)

        # Pose le bouton niveau suivant
        self.button_next_level = pygame.draw.rect(self.window, [0, 0, 0], [self.background.get_width()/2.6, self.height/1.4, 250, 50])

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()
        print('     - Ok')

    def display_score(self):
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
        new_game = Game()
        pass

    #########################################
    """Boucle Principal"""
    #########################################

    def display_hud(self):
        current_lvl = self.hud_font.render('%s %s' % ('Niveau', self.levels.current_level_number), True, (0, 0, 0))
        score = self.hud_font.render('%s' % self.player.score, True, (0, 0, 0))  # player.score
        time = self.hud_font.render('%s:%s:%s' % (self.time.chronos['current_level'].Time[0],
                                                  self.time.chronos['current_level'].Time[1],
                                                  self.time.chronos['current_level'].Time[2]), True, (0, 0, 0))  # time

        self.window.blit(current_lvl, (50, 14))
        self.window.blit(score, (492, 14))
        self.window.blit(time, (880, 14))

    #########################################
    """Boucle Principal"""
    #########################################

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
            self.pnj_collide()
            self.obstacle_collide()
            self.time.update()
            self.player.update()
            self.levels.current_level.pnj.update()

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
                if not self.levels:
                    self.end_game()

            # ----------------------------------------------------------

            pygame.display.flip()
            self.clock.tick(100)

if __name__ == '__main__':
    game = Game()


    #  gestion collision objets. il touche un objet, par a l'opposer (il le touche tjrs donc traverse l'objet)
    #  collision objets/pnj ne fonctionne pas
    #  gestion multi devour img

