#!/usr/bin/env python
# -*- coding:utf-8 -*-
import constants
from sprites import *


class Player(pygame.sprite.Sprite):
    def __init__(self, main, name, name_image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.dying = False
        self.is_feeding = False
        self.main = main
        self.name = name
        self.imgName = name_image
        self.width = 75
        self.height = 125
        self.main.time.add_rebour(self.name)
        self.moveX, self.moveY = 0, 0
        self.walkingFramesUp = []
        self.walkingFramesDown = []
        self.walkingFramesRight = []
        self.walkingFramesLeft = []
        self.get_frame()
        self.image = self.stopFrame
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) # pour les tests de collision pixel/pixel
        self.rect.x = x
        self.rect.y = y
        self.timeTarget = 40
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

    def __getitem__(self):
        return self.score

    def get_frame(self):
        """Charge les frames du joueur"""
        self.spriteSheet = SpriteSheet('data/img/' + self.imgName)

        self.walkingFramesLeft = self.spriteSheet.get_frames(self.walkingFramesLeft, constants.MOVING_SPRITE_X, 0, 75, 125)
        self.walkingFramesRight = self.spriteSheet.get_frames(self.walkingFramesRight, constants.MOVING_SPRITE_X, 0, 75, 125, True)
        self.walkingFramesUp = self.spriteSheet.get_frames(self.walkingFramesUp, constants.MOVING_SPRITE_X, 125, 75, 125)
        self.walkingFramesDown = self.spriteSheet.get_frames(self.walkingFramesDown, constants.MOVING_SPRITE_X, 250, 75, 125)

        self.stopFrame = self.spriteSheet.get_image(0, 375, self.width, self.height)

    def move_up(self):
        self.moveY = -1

    def move_down(self):
        self.moveY = 1

    def move_right(self):
        self.moveX = 1

    def move_left(self):
        self.moveX = -1

    def collide_window_side(self):
        """Test de collision avec le bord de la fenêtre"""
        if self.rect.x <= self.width/2 and self.moveX < 0:
            self.moveX = 0
        if self.rect.x > self.main.width - self.width/2 and self.moveX > 0:
            self.moveX = 0
        if self.rect.y <= self.height/3 and self.moveY < 0:
            self.moveY = 0
        if self.rect.y > self.main.height - self.height/3 and self.moveY > 0:
            self.moveY = 0

    def update(self):
        """Actualisation du joueur"""
        if self.is_feeding: # si le joueur est en train de manger, ne l'affiche pas
            self.image = None
        else:
            self.collide_window_side()
            self.rect.x += self.moveX
            self.rect.y += self.moveY
            self.timeNum += 1
            if self.timeNum == self.timeTarget:
                self.timeNum = 0
                self.currentImage += 1
                if self.currentImage == 4:
                    self.currentImage = 0
            if self.action != '':
                self.image = self.framesSwitch[self.action][self.currentImage]
            else:
                self.image = self.stopFrame
