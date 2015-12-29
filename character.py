#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import constants
from sprites import *


class Character(pygame.sprite.Sprite):
    def __init__(self, main, name, pos, num):
        self._layer = 1
        self.pos_on_layer = None
        self.is_layer_change = False  # Pour effectuer le changement de layer
        self.groups_sprites = main.all_sprites, main.pnj_sprites
        pygame.sprite.Sprite.__init__(self, self.groups_sprites)
        self.main = main
        self.num = num
        self.name = name
        self.id_name = name + str(num)  # Pour identifier le bon chrono/rebour
        self.main.time.add_rebour(self.id_name)

        self.width = 75
        self.height = 125
        self.moveX, self.moveY = 0, 0
        self.x, self.y = pos[0], pos[1]

        self.is_alive = True
        self.attacker = None
        self.is_crazy = False
        self.is_under_attack = False
        self.is_circle_collide = False
        
        self.tick = 0  # "Temp" entre chaque changement de direction "aléatoire"
        self.max_tick = 50

        self.action = ''
        self.action_switch = {'up': self.move_up,
                              'down': self.move_down,
                              'left': self.move_left,
                              'right': self.move_right}

        self.time_target = 20  # Temp entre chaque frame
        self.time_num = 0
        self.current_image = 0
        self.stop_frame = main.character_images[name]['stop_frame']
        self.image = self.stop_frame
        self.frames_switch = {'up': main.character_images[name]['walking_frames_up'],
                              'down': main.character_images[name]['walking_frames_down'],
                              'left': main.character_images[name]['walking_frames_left'],
                              'right': main.character_images[name]['walking_frames_right']}

        # Rect de base
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        # Rect pour les collision avec les objets
        self.collision_rect = self.image.get_rect()
        self.collision_rect.inflate_ip(-5, -80)
        self.collision_rect.center = (self.rect.x + 37, self.rect.y + 95)

        # Hitbox (collision enemis/joueur/zombies)
        self.hitbox_rect = self.image.get_rect()
        self.hitbox_rect.inflate_ip(-5, -85)
        self.hitbox_rect.center = (self.rect.x + 37, self.rect.y + 70)

        # Pour les collisions "pixel perfect"
        self.mask = pygame.mask.from_surface(self.image)

    def collide_window_side(self):
        """Test de collision avec les bords de la fenetre"""
        if self.rect.x <= self.width/2 and self.moveX < 0:
            self.move_right()
            self.action = 'right'
        if self.rect.x > constants.GAME_WIDTH - self.width/2 and self.moveX > 0:
            self.move_left()
            self.action = 'left'
        if self.rect.y <= self.height/1.5 and self.moveY < 0:
            self.move_down()
            self.action = 'down'
        if self.rect.y > constants.GAME_HEIGHT - self.height and self.moveY > 0:
            self.move_up()
            self.action = 'up'

    def change_layer_test(self, obstacle):
        """Gère le changement de layer"""
        if self.collision_rect.top < obstacle.collision_rect.bottom - 2:
            if self.pos_on_layer != 'back':
                self.is_layer_change = True
                self.pos_on_layer = 'back'
        elif self.pos_on_layer != 'front':
            self.is_layer_change = True
            self.pos_on_layer = 'front'

    def move_alea(self):
        """Changement de direction "aléatoire" tout les x ticks"""
        self.tick += 1
        if self.tick == self.max_tick:
            self.tick = 0
            rand = random.randint(1, 6)
            if rand > 5:
                rand = 5
            self.action = self.ia_action_switch[rand]
            if self.action != '':
                self.action_switch[self.action]()
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
        """Met à jour l'image"""
        self.time_num += 1
        if self.time_num == self.time_target:
            self.time_num = 0
            self.current_image += 1
            if self.current_image == 12:
                self.current_image = 0

    def select_frame(self):
        """Selectionne la frame en fonction de l'action"""
        if self.action != 'self_devour' and self.action != '':
            self.image = self.frames_switch[self.action][self.current_image]
        elif self.is_under_attack:
            self.image = self.frames_switch[self.action][self.attacker.name][self.current_image]
        else:
            self.image = self.stop_frame


class Humain(Character):
    def __init__(self, main, name, pos, num):
        Character.__init__(self, main, name, pos, num)
        self.is_human = True
        self.zombie_image = main.character_images['z_' + name]

        self.all_dying_frames = {'player': main.character_images[name]['attack']['by_player'],
                                 'z_citizen': main.character_images[name]['attack']['by_citizen'],
                                 'z_punk': main.character_images[name]['attack']['by_punk']}
        self.frames_switch['self_devour'] = self.all_dying_frames

        self.ia_action_switch = {1: 'up',
                                 2: 'down',
                                 3: 'left',
                                 4: 'right',
                                 5: ''}

        main.enemy_sprites.add(self)

    def become_crazy(self):
        """Rend fou le pnj qui changera de direction plus souvent"""
        print('[*] ' + self.name + str(self.num) + ' Become Crazy')
        self.is_crazy = True
        self.max_tick = 20

    def set_opposite_action(self):
        # TODO: not opposite action but away from player
        """Inverse l'action du pnj (up/down, left/right)"""
        print('[*] Set Opposite Action For ' + self.id_name)
        if self.action == 'up':
            self.action = 'down'
        elif self.action == 'down':
            self.action = 'up'
        elif self.action == 'left':
            self.action = 'right'
        elif self.action == 'right':
            self.action = 'left'
        if self.action != '':
            self.action_switch[self.action]()

    def under_attack(self, attacker):
        """Initialise le fait que le pnj se fait manger"""
        print('[*] ' + self.id_name + ' Is Under Attack')
        self.is_under_attack = True
        self.attacker = attacker
        self.action = 'self_devour'  # Se faire dévorer
        self.current_image = 0
        self.main.time.rebours[self.id_name].start([00, 02, 00])

    def is_dying(self):
        """Mort du citoyen"""
        print('[*] ' + self.id_name + ' Is Dying')
        self.is_alive = False
        if self.attacker == self.main.player:
            self.going_zombie()
            self.main.player.score += 2
            self.main.player.final_score += 2
        else:
            self.main.player.score += 1
            self.main.player.final_score += 1

        try:  # pour le survival uniquement
            self.main.victims += 1
        except:
            pass
        try:
            self.attacker.is_feeding = False
        except:
            pass

    def going_zombie(self):
        """Choisie si le citoyen se reveil en zombie"""
        rand = random.randint(0, 100)
        print(self.main)
        if rand <= 30:
            self.main.levels.current_level.pnj.add_zombie(self.main,
                                                          'z_' + self.name,
                                                          (self.rect.x, self.rect.y),
                                                          self.num)

    def obstacle_collide(self, obstacles_list):
        """Collision pnj/objets"""
        # TODO: a mettre dans character
        if not self.is_under_attack:
            obstacles_collided = pygame.sprite.spritecollide(self, obstacles_list, False)
            for obstacle in obstacles_collided:
                self.change_layer_test(obstacle)

                if self.collision_rect.colliderect(obstacle.collision_rect):
                    print('[*] Enemy Collide Object')
                    if self.collision_rect.x <= obstacle.collision_rect.x and self.moveX > 0:  # vas vers la gauche
                        self.action = 'left'
                        self.action_switch[self.action]()
                    elif self.collision_rect.x >= obstacle.collision_rect.x and self.moveX < 0:  # vas vers la droite
                        self.action = 'right'
                        self.action_switch[self.action]()

                    if self.collision_rect.y <= obstacle.collision_rect.y and self.moveY > 0:  # vas vers le haut
                        self.action = 'up'
                        self.action_switch[self.action]()
                    elif self.collision_rect.y >= obstacle.collision_rect.y and self.moveY < 0:  # vas vers le bas
                        self.action = 'down'
                        self.action_switch[self.action]()

    def update(self, obstacles_list):
        """Met à jour le pnj"""
        if self.main.time.rebours[self.id_name].isFinish:
            self.is_dying()
        if not self.is_under_attack:
            self.move_alea()
            # Déplacement du pnj
            self.rect = self.rect.move([self.moveX, self.moveY])
            self.collision_rect = self.collision_rect.move([self.moveX, self.moveY])
            self.hitbox_rect = self.hitbox_rect.move([self.moveX, self.moveY])

        self.collide_window_side()
        self.obstacle_collide(obstacles_list)
        self.update_current_image()
        self.select_frame()


class Zombie(Character):
    def __init__(self, main, name, pos, num):
        Character.__init__(self, main, name, pos, num)
        self.is_human = False
        self.is_feeding = False
        self.main.time.rebours[self.id_name].start([00, 20, 00])  # x temp de vie (H:M:S)
        self.ia_action_switch = {1: 'up',
                                 2: 'down',
                                 3: 'left',
                                 4: 'right',
                                 5: ''}
        self.radius = 200
        main.zombie_sprites.add(self)

    def dying(self):
        """Déclare le zombie définitivement mort"""
        print('[*] ' + self.name + ' Is Dying')
        self.is_alive = False

    def obstacle_collide(self, obsctacles_list):
        """Collision pnj/objets"""
        # TODO: a mettre dans character
        if not self.is_feeding:
            obstacles_collided = pygame.sprite.spritecollide(self, obsctacles_list, False)
            for obstacle in obstacles_collided:
                self.change_layer_test(obstacle)

                if obstacle.name == 'manhole':
                    if self.collision_rect.colliderect(obstacle.collision_rect):
                        self.is_alive = False

                if self.collision_rect.colliderect(obstacle.collision_rect):
                    print('[*] Zombie Collide Object')
                    if self.rect.x <= obstacle.collision_rect.x and self.moveX > 0:  # vas vers la gauche
                        self.action = 'left'
                        self.action_switch[self.action]()
                    elif self.rect.x >= obstacle.collision_rect.x and self.moveX < 0:  # vas vers la droite
                        self.action = 'right'
                        self.action_switch[self.action]()

                    if self.rect.y <= obstacle.collision_rect.y and self.moveY < 0:  # vas vers le haut
                        self.action = 'down'
                        self.action_switch[self.action]()
                    elif self.rect.y >= obstacle.collision_rect.y and self.moveY > 0:  # vas vers le bas
                        self.action = 'up'
                        self.action_switch[self.action]()

    def collide(self, enemy_sprites):
        """Collsision enemis/zombies"""
        if not self.is_feeding:
            enemy_hit_list = pygame.sprite.spritecollide(self, enemy_sprites, False)
            for enemy in enemy_hit_list:
                if not enemy.is_under_attack:
                    if self.hitbox_rect.colliderect(enemy.hitbox_rect):
                            print('[*] Mask Collide - Zombie')
                            enemy.under_attack(self)
                            self.is_feeding = True

    def update(self, obstacles_list, enemy_sprites):
        """Met à jour le pnj"""
        if self.main.time.rebours[self.id_name].isFinish:  # si le rebour principal est fini le zombie meur
            self.dying()
        if self.is_feeding:  # si le zombie est en train de manger, ne l'affiche pas
            self.rect.x = -100  # Hors de l'écran
            self.rect.y = -100
        elif self.rect.x == -100:
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.move_alea()

            self.rect = self.rect.move([self.moveX, self.moveY])
            self.collision_rect = self.collision_rect.move([self.moveX, self.moveY])
            self.hitbox_rect = self.hitbox_rect.move([self.moveX, self.moveY])
            self.x, self.y = self.rect.x, self.rect.y

            self.collide_window_side()
            self.obstacle_collide(obstacles_list)
            self.collide(enemy_sprites)

            self.update_current_image()
            self.select_frame()
