#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sprites import *


class Player(pygame.sprite.Sprite):
    def __init__(self, name, images, all_sprites, x, y, width, height):
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.game_width = width
        self.game_height = height
        self.name = name
        self.width = 75
        self.height = 125
        self.moveX, self.moveY = 0, 0
        self.x, self.y = x, y

        self.score = 0
        self.final_score = 0

        self.dying = False
        self.is_feeding = False

        self.action = ''
        self.actionSwitch = {'up': self.move_up,
                             'down': self.move_down,
                             'left': self.move_left,
                             'right': self.move_right}

        self.timeTarget = 40
        self.timeNum = 0
        self.currentImage = 0
        self.stopFrame = images['stopFrame']
        self.framesSwitch = {'up': images['walkingFramesUp'],
                             'down': images['walkingFramesDown'],
                             'left': images['walkingFramesLeft'],
                             'right': images['walkingFramesRight']}
        self.image = self.stopFrame

        # Rect de base
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Rect pour les collision avec les objets
        self.collision_rect = self.image.get_rect()
        self.collision_rect.inflate_ip(-5, -80)
        self.collision_rect.center = (self.rect.x + 37, self.rect.y + 95)

        # Hitbox
        self.hitbox_rect = self.image.get_rect()
        self.hitbox_rect.inflate_ip(-5, -85)
        self.hitbox_rect.center = (self.rect.x + 37, self.rect.y + 70)

        # Pour les circle collisions
        self.radius = 200

        # Pour les collisions "pixel perfect"
        self.mask = pygame.mask.from_surface(self.image)  # pour les tests de collision pixel/pixel

    def __getitem__(self):
        """Renvoi le score du joueur"""
        return self.score

    def move_up(self):
        self.moveY = -1

    def move_down(self):
        self.moveY = 1

    def move_right(self):
        self.moveX = 1

    def move_left(self):
        self.moveX = -1

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.collision_rect.center = (self.rect.x + 37, self.rect.y + 95)
        self.hitbox_rect.center = (self.rect.x + 37, self.rect.y + 70)

    def collide_window_side(self):
        """Test de collision avec le bord de la fenêtre"""
        if self.rect.x <= self.width/2 and self.moveX < 0:
            self.moveX = 0
        if self.rect.x > self.game_width - self.width/2 and self.moveX > 0:
            self.moveX = 0
        if self.rect.y <= self.height/3 and self.moveY < 0:
            self.moveY = 0
        if self.rect.y > self.game_height - self.height and self.moveY > 0:
            self.moveY = 0
            
    def obstacle_collide(self, obstacles_list):
        """Collision joeur-objets et pnj-objet (en cour)"""
        if not self.is_feeding:
            obstacles_collided = pygame.sprite.spritecollide(self, obstacles_list, False)
            for obstacle in obstacles_collided:
                print('[*] Player Collide Object')
                if obstacle.name == 'manhole':
                    if pygame.sprite.collide_mask(self, obstacle):
                        self.dying = True
                        print('[*] Launch Game Over')

                elif self.collision_rect.colliderect(obstacle.collision_rect):
                    if self.collision_rect.x <= obstacle.collision_rect.x and self.moveX > 0:
                        self.moveX = 0
                    if self.collision_rect.x >= obstacle.collision_rect.x and self.moveX < 0:
                        self.moveX = 0
                    if self.collision_rect.y <= obstacle.collision_rect.y and self.moveY > 0:
                        self.moveY = 0
                    if self.collision_rect.y >= obstacle.collision_rect.y and self.moveY < 0:
                        self.moveY = 0

    def update(self, obstacles_list):
        """Actualisation du joueur"""
        if self.is_feeding:  # si le joueur est en train de manger, ne l'affiche pas
            self.rect.x = -100
            self.rect.y = -100
        elif self.rect.x == -100:
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.collide_window_side()
            self.obstacle_collide(obstacles_list)
            self.rect = self.rect.move([self.moveX, self.moveY])
            self.collision_rect = self.collision_rect.move([self.moveX, self.moveY])
            self.hitbox_rect = self.hitbox_rect.move([self.moveX, self.moveY])
            self.x, self.y = self.rect.x, self.rect.y
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
