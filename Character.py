#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import constants
from sprites import *


class Character(pygame.sprite.Sprite):
    def __init__(self, main, name, name_image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.name = name
        self.isAlive = True
        self.underAttack = False
        self.main.time.add_rebour(self.name)
        self.imgName = name_image
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
        self.rect.x = x
        self.rect.y = y
        self.timeTarget = 30 # temp entre chaque frame
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

        self.walkingFramesLeft = self.spriteSheet.get_frames(self.walkingFramesLeft, constants.MOVING_SPRITE_X, 0, 75, 125)
        self.walkingFramesRight = self.spriteSheet.get_frames(self.walkingFramesRight, constants.MOVING_SPRITE_X, 0, 75, 125, True)
        self.walkingFramesUp = self.spriteSheet.get_frames(self.walkingFramesUp, constants.MOVING_SPRITE_X, 125, 75, 125)
        self.walkingFramesDown = self.spriteSheet.get_frames(self.walkingFramesDown, constants.MOVING_SPRITE_X, 250, 75, 125)

        self.stopFrame = self.spriteSheet.get_image(0, 375, self.width, self.height)

    def collide_window_side(self):
        if self.rect.x <= self.width/2 and self.moveX < 0:
            self.move_right()
            self.action = 'right'
        if self.rect.x > self.main.width - self.width/2 and self.moveX > 0:
            self.move_left()
            self.action = 'left'
        if self.rect.y <= self.height/3 and self.moveY < 0:
            self.move_down()
            self.action = 'down'
        if self.rect.y > self.main.height - self.height/3 and self.moveY > 0:
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
        # Gestion frames
        self.timeNum += 1
        if self.timeNum == self.timeTarget:
            self.timeNum = 0
            self.currentImage += 1
            if self.currentImage == 4 and self.action != 'self_devour':
                self.currentImage = 0
            if self.currentImage == 8:
                self.currentImage = 0
        # Selection frame
        if self.action != '':
            self.image = self.framesSwitch[self.action][self.currentImage]
        elif self.underAttack:
            self.image = self.framesSwitch[self.action]
        else:
            self.image = self.stopFrame


class Humain(Character):
    def __init__(self, main, name, name_image, x, y):
        Character.__init__(self, main, name, name_image, x, y)
        self.tick = 0
        self.attacker = None
        self.dyingFramesLeft = []
        self.get_action_frame()
        self.framesSwitch['self_devour'] = self.dyingFramesLeft
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def get_action_frame(self):
        """Recupère les frames des actions"""
        self.spriteSheet = SpriteSheet('data/img/' + 'actions/citizen_attack_sprite_sheet.png')
        self.dyingFramesLeft = self.spriteSheet.get_frames(self.dyingFramesLeft, constants.DYING_SPRITE_X, 0, 125, 125)

    def is_under_attack(self, attacker):
        print('[*] ' + self.name + ' Is Under Attack')
        self.underAttack = True
        self.attacker = attacker
        self.action = 'self_devour' # Se fait dévorer
        self.currentImage = 0
        self.main.time.rebours[self.name].start([00, 02, 00])

    def is_dying(self):
        """Mort du citoyen"""
        if self.main.time.rebours[self.name].isFinish:
            print('[*] ' + self.name + ' Is Dying')
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
            self.main.levels.current_level.pnj.add_zombie(self.main, self.name, 'character/zombie_citizen_sprite_sheet.png', self.rect.x, self.rect.y)

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
    def __init__(self, main, name, name_image, x, y):
        Character.__init__(self, main, name, name_image, x, y)
        self.tick = 0
        self.is_feeding = False
        self.main.time.rebours[self.name].start([00, 10, 00]) # x temp de vie (H:M:S)
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def dying(self):
        print('[*] ' + self.name + ' Is Dying')
        self.isAlive = False

    def update(self):
        if self.main.time.rebours[self.name].isFinish:  # si le rebour principal est fini le zombie meur
            self.dying()
        if self.is_feeding:
            self.image = self.stopFrame
        else:
            self.move_alea()
            self.rect.x += self.moveX
            self.rect.y += self.moveY
            self.collide_window_side()
            self.select_frame()
