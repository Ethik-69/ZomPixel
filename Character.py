#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import constants
from sprites import *


class Character(pygame.sprite.Sprite):
    def __init__(self, main, init_values, pos, num):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.num = num
        self.id_name = init_values['name'] + str(num)  # For chrono identification
        self.name = init_values['name']
        self.isAlive = True
        self.underAttack = False
        self.attacker = None
        self.spriteSheet = None
        self.main.time.add_rebour(self.id_name)
        self.imgName = init_values['img']
        self.width = 75
        self.height = 125
        self.moveX, self.moveY = 0, 0
        self.walkingFramesUp = []
        self.walkingFramesDown = []
        self.walkingFramesRight = []
        self.walkingFramesLeft = []
        self.get_frame()
        self.image = self.stopFrame
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.timeTarget = 20  # temp entre chaque frame
        self.timeNum = 0
        self.currentImage = 0
        self.action = ''
        self.framesSwitch = {'up': self.walkingFramesUp,
                             'down': self.walkingFramesDown,
                             'left': self.walkingFramesLeft,
                             'right': self.walkingFramesRight}
        self.actionSwitch = {'up': self.move_up,
                             'down': self.move_down,
                             'left': self.move_left,
                             'right': self.move_right}

    def get_frame(self):
        """Charge les frames des personnages"""
        self.spriteSheet = SpriteSheet('data/img/' + self.imgName)

        self.walkingFramesLeft = self.spriteSheet.get_character_frames(self.walkingFramesLeft,
                                                             constants.MOVING_SPRITE_X,
                                                             0, 75, 125)

        self.walkingFramesRight = self.spriteSheet.get_character_frames(self.walkingFramesRight,
                                                              constants.MOVING_SPRITE_X,
                                                              0, 75, 125, True)

        self.walkingFramesDown = self.spriteSheet.get_character_frames(self.walkingFramesDown,
                                                             constants.MOVING_SPRITE_X,
                                                             250, 75, 125)

        self.walkingFramesUp = self.spriteSheet.get_character_frames(self.walkingFramesUp,
                                                           constants.MOVING_SPRITE_X,
                                                           125, 75, 125)

        self.stopFrame = self.spriteSheet.get_image(0, 375, self.width, self.height)

    def collide_window_side(self):
        """Test de collision avec les bords de la fenetre"""
        if self.rect.x <= self.width/2 and self.moveX < 0:
            self.move_right()
            self.action = 'right'
        if self.rect.x > self.main.width - self.width/2 and self.moveX > 0:
            self.move_left()
            self.action = 'left'
        if self.rect.y <= self.height/1.5 and self.moveY < 0:
            self.move_down()
            self.action = 'down'
        if self.rect.y > self.main.height - self.height and self.moveY > 0:
            self.move_up()
            self.action = 'up'

    def move_alea(self):
        """Choisi une direction aleatoire tout les x ticks"""
        self.tick += 1
        if self.tick == 200:
            self.tick = 0
            rand = random.randint(1, 6)
            if rand > 5:
                rand = 5
            self.action = self.iaActionSwitch[rand]
            if self.action != '':
                self.actionSwitch[self.action]()
            else:
                pass

    def move_up(self):
        self.moveY = -1

    def move_down(self):
        self.moveY = 1

    def move_right(self):
        self.moveX = 1

    def move_left(self):
        self.moveX = -1

    def select_frame(self):
        """Selectionne le frame en fonction de l'action et de l'image courante"""
        self.timeNum += 1
        if self.timeNum == self.timeTarget:
            self.timeNum = 0
            self.currentImage += 1
            if self.currentImage == 12:
                self.currentImage = 0
        # Selection frame
        if self.action != 'self_devour' and self.action != '':
            self.image = self.framesSwitch[self.action][self.currentImage]
        elif self.underAttack:
            self.image = self.framesSwitch[self.action][self.attacker.name][self.currentImage]
        else:
            self.image = self.stopFrame


class Humain(Character):
    def __init__(self, main, init_values, pos, num):
        Character.__init__(self, main, init_values, pos, num)
        self.tick = 0
        self.img_attack_by_player = init_values['attack_by_player']
        self.img_attack_by_citizen = init_values['attack_by_citizen']
        self.img_attack_by_punk = init_values['attack_by_punk']
        self.spriteSheet = None
        self.dyingFrames = []
        self.allDyingFrames = {}
        self.zombie_image = init_values['zombie_img']
        self.get_actions_frames()
        self.framesSwitch['self_devour'] = self.allDyingFrames
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def get_actions_frames(self):
        """Recupère les frames des actions"""
        self.spriteSheet = SpriteSheet('data/img/' + self.img_attack_by_citizen)
        self.dyingFrames = self.spriteSheet.get_character_frames(self.dyingFrames, constants.DYING_SPRITE_X, 0, 125, 125)
        self.allDyingFrames['citizen'] = self.dyingFrames
        self.dyingFrames = []

        self.spriteSheet = SpriteSheet('data/img/' + self.img_attack_by_player)
        self.dyingFrames = self.spriteSheet.get_character_frames(self.dyingFrames, constants.DYING_SPRITE_X, 0, 125, 125)
        self.allDyingFrames['player'] = self.dyingFrames
        self.dyingFrames = []

        self.spriteSheet = SpriteSheet('data/img/' + self.img_attack_by_punk)
        self.dyingFrames = self.spriteSheet.get_character_frames(self.dyingFrames, constants.DYING_SPRITE_X, 0, 125, 125)
        self.allDyingFrames['punk'] = self.dyingFrames
        self.dyingFrames = []

    def is_under_attack(self, attacker):
        """Initialise le fait que le pnj en prend plein la tronche"""
        print('[*] ' + self.id_name + ' Is Under Attack')
        self.underAttack = True
        self.attacker = attacker
        self.action = 'self_devour' # Se fait dévorer
        self.currentImage = 0
        self.main.time.rebours[self.id_name].start([00, 02, 00])

    def is_dying(self):
        """Mort du citoyen"""
        if self.main.time.rebours[self.id_name].isFinish:
            print('[*] ' + self.id_name + ' Is Dying')
            self.isAlive = False
            if self.attacker == self.main.player:
                self.going_zombie()
                self.main.player.score += 2
            else:
                self.main.player.score += 1
            try:
                self.attacker.is_feeding = False
                self.attacker.image = self.attacker.stopFrame
            except Exception as E:
                pass

    def going_zombie(self):
        """Choisie si le citoyen se reveil en zombie"""
        rand = random.randint(0, 100)
        if rand <= 100:
            self.main.levels.current_level.pnj.add_zombie(self.main,
                                                          self.id_name,
                                                          self.name,
                                                          self.zombie_image,
                                                          (self.rect.x, self.rect.y),
                                                          self.num)

    def update(self):
        """Actualisation des citoyens"""
        self.is_dying()
        if not self.underAttack:
            self.move_alea()
            self.rect.x += self.moveX
            self.rect.y += self.moveY
        self.collide_window_side()
        self.select_frame()


class Zombie(Character):
    def __init__(self, main, init_values, pos, num):
        Character.__init__(self, main, init_values, pos, num)
        self.tick = 0
        self.is_feeding = False
        self.main.time.rebours[self.id_name].start([00, 10, 00]) # x temp de vie (H:M:S)
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def dying(self):
        """Déclare le zombie mort"""
        print('[*] ' + self.name + ' Is Dying')
        self.isAlive = False

    def update(self):
        if self.main.time.rebours[self.id_name].isFinish:  # si le rebour principal est fini le zombie meur
            self.dying()
        if self.is_feeding:
            self.image = self.stopFrame
        else:
            self.move_alea()
            self.rect.x += self.moveX
            self.rect.y += self.moveY
            self.collide_window_side()
            self.select_frame()
