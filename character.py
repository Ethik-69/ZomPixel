#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from sprites import *


class Character(pygame.sprite.Sprite):
    def __init__(self, main, name, pos, num):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.num = num
        self.name = name
        self.id_name = name + str(num)  # For chrono identification

        self.tick = 0
        self.width = 75
        self.height = 125
        self.moveX, self.moveY = 0, 0
        self.main.time.add_rebour(self.id_name)

        self.is_alive = True
        self.is_under_attack = False
        self.attacker = None

        self.action = ''
        self.actionSwitch = {'up': self.move_up,
                             'down': self.move_down,
                             'left': self.move_left,
                             'right': self.move_right}

        self.timeTarget = 20  # temp entre chaque frame
        self.timeNum = 0
        self.currentImage = 0
        self.stopFrame = main.character_images[name]['stopFrame']
        self.image = self.stopFrame
        self.framesSwitch = {'up': main.character_images[name]['walkingFramesUp'],
                             'down': main.character_images[name]['walkingFramesDown'],
                             'left': main.character_images[name]['walkingFramesLeft'],
                             'right': main.character_images[name]['walkingFramesRight']}

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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
        if self.tick == 50:
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

    def update_current_image(self):
        self.timeNum += 1
        if self.timeNum == self.timeTarget:
            self.timeNum = 0
            self.currentImage += 1
            if self.currentImage == 12:
                self.currentImage = 0

    def select_frame(self):
        """Selectionne la frame en fonction de l'action"""
        if self.action != 'self_devour' and self.action != '':
            self.image = self.framesSwitch[self.action][self.currentImage]
        elif self.is_under_attack:
            self.image = self.framesSwitch[self.action][self.attacker.name][self.currentImage]
        else:
            self.image = self.stopFrame


class Humain(Character):
    def __init__(self, main, name, pos, num):
        Character.__init__(self, main, name, pos, num)
        self.tick = 0
        self.allDyingFrames = {'player': main.character_images[name]['attack']['by_player'],
                               'z_citizen': main.character_images[name]['attack']['by_citizen'],
                               'z_punk': main.character_images[name]['attack']['by_punk']}
        self.zombie_image = main.character_images['z_' + name]
        self.framesSwitch['self_devour'] = self.allDyingFrames
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def under_attack(self, attacker):
        """Initialise le fait que le pnj en prend plein la tronche"""
        print('[*] ' + self.id_name + ' Is Under Attack')
        self.is_under_attack = True
        self.attacker = attacker
        self.action = 'self_devour'  # Se fait dévorer
        self.currentImage = 0
        self.main.time.rebours[self.id_name].start([00, 02, 00])

    def is_dying(self):
        """Mort du citoyen"""
        if self.main.time.rebours[self.id_name].isFinish:
            print('[*] ' + self.id_name + ' Is Dying')
            self.is_alive = False
            if self.attacker == self.main.player:
                self.going_zombie()
                self.main.player.score += 2
                self.main.player.final_score += 2
            else:
                self.main.player.score += 1
                self.main.player.final_score += 1
            try:
                self.attacker.is_feeding = False
                self.attacker.image = self.attacker.stopFrame
            except:
                pass

    def going_zombie(self):
        """Choisie si le citoyen se reveil en zombie"""
        rand = random.randint(0, 100)
        if rand <= 100:
            self.main.levels.current_level.pnj.add_zombie(self.main,
                                                          'z_' + self.name,
                                                          (self.rect.x, self.rect.y),
                                                          self.num)

    def obstacle_collide(self, obstacles_list):
        if not self.is_under_attack:
            obstacles_collided = pygame.sprite.spritecollide(self, obstacles_list, False)
            for obstacle in obstacles_collided:
                print('[*] Enemy Collide Object')
                if self.rect.x <= obstacle.rect.x and self.moveX > 0:  # vas vers la gauche
                    self.action = 'left'
                    self.actionSwitch[self.action]()
                elif self.rect.x >= obstacle.rect.x and self.moveX < 0:  # vas vers la droite
                    self.action = 'right'
                    self.actionSwitch[self.action]()
                    
                if self.rect.y <= obstacle.rect.y and self.moveY > 0:  # vas vers le haut
                    self.action = 'up'
                    self.actionSwitch[self.action]()
                elif self.rect.y >= obstacle.rect.y and self.moveY < 0:  # vas vers le bas
                    self.action = 'down'
                    self.actionSwitch[self.action]()

    def update(self, obstacles_list):
        """Actualisation des citoyens"""
        self.is_dying()
        if not self.is_under_attack:
            self.move_alea()
            self.rect = self.rect.move([self.moveX, self.moveY])
        self.collide_window_side()
        # self.obstacle_collide(obstacles_list)
        self.update_current_image()
        self.select_frame()


class Zombie(Character):
    def __init__(self, main, name, pos, num):
        Character.__init__(self, main, name, pos, num)
        self.tick = 0
        self.is_feeding = False
        self.main.time.rebours[self.id_name].start([00, 10, 00])  # x temp de vie (H:M:S)
        self.iaActionSwitch = {1: 'up',
                               2: 'down',
                               3: 'left',
                               4: 'right',
                               5: ''}

    def dying(self):
        """Déclare le zombie mort"""
        print('[*] ' + self.name + ' Is Dying')
        self.is_alive = False

    def obstacle_collide(self, obsctacles_list):
        if not self.is_feeding:
            obstacles_collided = pygame.sprite.spritecollide(self, obsctacles_list, False)
            for obstacle in obstacles_collided:
                print('[*] Zombie Collide Object')
                if self.rect.x <= obstacle.rect.x and self.moveX > 0:  # vas vers la gauche
                    self.action = 'left'
                    self.actionSwitch[self.action]()
                elif self.rect.x >= obstacle.rect.x and self.moveX < 0:  # vas vers la droite
                    self.action = 'right'
                    self.actionSwitch[self.action]()

                if self.rect.y <= obstacle.rect.y and self.moveY < 0:  # vas vers le haut
                    self.action = 'down'
                    self.actionSwitch[self.action]()
                elif self.rect.y >= obstacle.rect.y and self.moveY > 0:  # vas vers le bas
                    self.action = 'up'
                    self.actionSwitch[self.action]()

    def update(self, obstacles_list):
        if self.main.time.rebours[self.id_name].isFinish:  # si le rebour principal est fini le zombie meur
            self.dying()
        if self.is_feeding:
            self.image = self.stopFrame
        else:
            self.move_alea()
            self.rect = self.rect.move([self.moveX, self.moveY])
            self.collide_window_side()
            # self.obstacle_collide(obstacles_list)
            self.update_current_image()
            self.select_frame()
