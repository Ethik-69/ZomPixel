#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from levels import *
from time_made_home import *
from player import *
from character import *
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

        self.frameCount = 0
        self.frameRate = 0

        self.player = None
        self.player_sprite = None

        self.run = None
        self.time = None
        self.clock = None
        self.levels = None
        self.click_pos_x = None
        self.click_pos_y = None
        self.enemy_hit_list = None
        self.obstacles_collided = None

        self.is_credit = False
        self.is_game_over = False
        self.is_display_score = False
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
        self.text_blit(self.welcome_font1, "Demarrer", (0, 0, 0), (self.background.get_width()/1.975, 660))
        self.text_blit(self.welcome_font1, "?", (0, 0, 0), (self.background.get_width()/1.095, 660))

    def title_screen(self):
        """Boucle de l'ecran d'accueil"""
        print('[*] Title Screen Init')
        title_screen = True
        self.background.blit(self.game_images['welcome_background_image'], (0, 0))
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

        self.time = Times()
        self.clock = pygame.time.Clock()

        self.load_all_images()

        self.create_player()
        self.levels = Levels(self)
        self.levels.init_level()
        # self.title_screen()
        self.main()

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

    def create_player(self):
        """Creation du joueur"""
        print('[*] Player Init')
        self.player_sprite = pygame.sprite.Group()
        self.player = Player('player', self.character_images['player'], 512, 354, self.width, self.height)
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
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_lvl_change:
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
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_accueil:
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

        self.text_blit(self.final_score_font, "Developper par:",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 400))

        self.text_blit(self.final_score_font, "Ethan CHAMIK",
                       (100, 20, 20), (constants.GAME_WIDTH/5, 500))

        self.text_blit(self.final_score_font, "Romain GUILLOT",
                       (100, 20, 20), (constants.GAME_WIDTH/2, 500))

        self.text_blit(self.final_score_font, "Thibault DESCAMPS",
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

        button_back = pygame.draw.rect(self.window, [255, 255, 255], [self.background.get_width()/2.7, 609, 280, 106])
        self.init_credit()

        self.window.blit(self.background, (0, 0))
        pygame.display.flip()

        while self.is_credit:
            mouse_xy = pygame.mouse.get_pos()
            is_back = button_back.collidepoint(mouse_xy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                elif event.type == MOUSEBUTTONDOWN and is_back:
                    self.is_credit = False
                    print('[*] Leaving Credit')
                    self.end_game()

    def end_game(self):
        print('[*] Start New Game')
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

    def main(self):
        print('[*] Launch Main')
        self.run = True
        self.levels.current_level.start()

        while self.run:
            mouse_xy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
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
            self.levels.current_level.update(self.levels.current_level.obstacles.objects_list)

            if self.player.dying:
                self.display_game_over('game_over')

            # ------------------------Display------------------------

            self.window.blit(self.background, (0, 0))
            self.display_hud()
            self.levels.current_level.pnj.draw()

            # Test d'affichage des rect de collision (hitbox)

            # for pnj in self.levels.current_level.pnj.enemy_list:
            #     if pnj.is_crazy:
            #         pygame.draw.rect(self.window, (255, 255, 255), pnj.hitbox_rect)
            #     else:
            #         pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

            # for pnj in self.levels.current_level.pnj.zombie_list:
            #     pygame.draw.rect(self.window, (0, 0, 0), pnj.hitbox_rect)

            # for object in self.levels.current_level.obstacles.objects_list:
            #     pygame.draw.rect(self.window, (0, 0, 0), object.collision_rect)

            # -----------------------------------------------

            # Si le joueur mange, ne l'affiche pas
            if not self.player.is_feeding:
                self.player_sprite.draw(self.window)
                # pygame.draw.rect(self.window, (100, 10, 10), self.player.hitbox_rect)  # Test

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


if __name__ == '__main__':
    while True:
        print('[*] Game Object Init')
        game = Game()
        game.start()

    # TODO: collision, rect plus petit pour pouvoir passer deriere les objets
    # TODO: circle collision pour les citoyen 'fou' une fois près d'un zombie
    # TODO: TEST !! =D <= c'est cool les test !
    # TODO: boutons -> vrai boutons
    # TODO: Refacto !
    # TODO: Recherche 'IA'

    # RETOUR: - Plus nerveux
        #     - Amélioration collision
