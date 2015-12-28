#!/usr/bin/env python
# -*- coding:utf-8 -*-
from character import *
import constants


class PNJ(object):
    def __init__(self, main, start_enemy_list, level):
        self.main = main
        self.level = level
        self.pnj_num = 0  # compteur pour différencier les pnjs
        self.init_pnj(start_enemy_list)

    def init_pnj(self, enemy_data):
        """Initialise les Personnages Non Joueur"""
        print('     - PNJ Init in Progress')
        for pos in enemy_data.keys():
            Humain(self.main, enemy_data[pos], pos, self.pnj_num)
            self.pnj_num += 1
            print('.'),

    def add_zombie(self, main, name, pos, num):
        """Instancie un zombie"""
        print('[*] ' + name + ' Going Zombie')
        Zombie(main, name, pos, num)
        print('[*] New Zombie')

    def add_enemy(self, pos):
        """Instancie un enemi"""
        print('[*] Add citizen' + str(self.pnj_num))
        Humain(self.main, 'citizen', pos, self.pnj_num)
        self.pnj_num += 1

    def remove_all_zombie(self):
        """Supprime tout les zombies"""
        print('[*] Remove Remaining Zombies')
        for zombie in self.main.zombie_sprites:
            self.main.zombie_sprites.remove(zombie)
            self.main.pnj_sprites.remove(zombie)
            self.main.all_sprites.remove(zombie)
        print('     - Ok')

    def player_circle_collide(self):
        # TODO: a mettre dans l'objet player
        """Collision circulaire enemis/joueur"""
        for enemy in self.main.enemy_sprites:
            if not enemy.is_under_attack and pygame.sprite.collide_circle(self.main.player, enemy):
                if not enemy.is_circle_collide:
                    print('[*] ' + enemy.name + str(enemy.num) + ' Collide Circle')
                    enemy.set_opposite_action()
                    enemy.is_circle_collide = True
                if not enemy.is_crazy:
                    enemy.become_crazy()

            elif enemy.is_circle_collide:
                enemy.is_circle_collide = False

    def player_collide(self):
        # TODO: a mettre dans l'objet player
        """Collision enemis/joueur"""
        if not self.main.player.is_feeding:
            enemy_hit_list = pygame.sprite.spritecollide(self.main.player,
                                                         self.main.enemy_sprites,
                                                         False)
            for enemy in enemy_hit_list:
                if not self.main.player.is_feeding and not enemy.is_under_attack:
                    if self.main.player.hitbox_rect.colliderect(enemy.hitbox_rect):
                            print('[*] Hitbox Collide - Player')
                            enemy.under_attack(self.main.player)
                            self.main.player.is_feeding = True

    def zombie_collide(self):
        # TODO: a eventuellement mettre dans l'objet zombie
        """Collsision enemis/zombies"""
        for zombie in self.main.zombie_sprites:
            if not zombie.is_feeding:
                enemy_hit_list = pygame.sprite.spritecollide(zombie, self.main.enemy_sprites, False)
                for enemy in enemy_hit_list:
                    if not enemy.is_under_attack:
                        if zombie.hitbox_rect.colliderect(enemy.hitbox_rect):
                                print('[*] Mask Collide - Zombie')
                                enemy.under_attack(zombie)
                                zombie.is_feeding = True

    def update(self):
        """Met les pnj à jour"""
        # Supprime les pnjs si ils sont 'mort'
        for pnj in self.main.pnj_sprites:
            if not pnj.is_alive:
                self.main.pnj_sprites.remove(pnj)
                self.main.all_sprites.remove(pnj)
                if pnj.is_human:
                    print('[*] Remove Human')
                    self.main.enemy_sprites.remove(pnj)
                else:
                    print('[*] Remove Human')
                    self.main.zombie_sprites.remove(pnj)

        # TODO: a mettre dans le main
        if len(self.main.enemy_sprites) == 0 and self.level.is_started:
            print('[*] Change Lvl => True')
            self.level.is_change_level = True

        self.player_collide()
        self.zombie_collide()
        self.player_circle_collide()


class Obstacles(object):
    def __init__(self, main):
        """Gère les différent obstacles"""
        self.main = main
        self.tree = False
        self.objects_list = pygame.sprite.Group()

    def create_all(self, objects_pos):
        """Instancie tout les obstacles"""
        for key in objects_pos.keys():
            for pos in objects_pos[key]:
                obstacle = Object(self.main, key, pos)
                self.objects_list.add(obstacle)
        print('[*] Create Objects Ok')

    def reset(self):
        """Supprime tout les objets instanciés"""
        for object in self.objects_list:
            self.main.all_sprites.remove(object)
            self.objects_list.remove(object)


class Object(pygame.sprite.Sprite):
    def __init__(self, main, name, pos):
        self._layer = 0
        pygame.sprite.Sprite.__init__(self, main.all_sprites)

        self.main = main
        self.name = name
        self.pos = pos

        self.image = main.obstacles_images[name]

        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.collision_rect = self.image.get_rect()
        self.collision_rect.x = self.rect.x
        self.collision_rect.y = self.rect.y
        self.collision_rect.inflate_ip(constants.OBSTACLES[name][1][0],
                                       constants.OBSTACLES[name][1][1])
        self.collision_rect.center = (self.rect.x + constants.OBSTACLES[name][2][0],
                                      self.rect.y + constants.OBSTACLES[name][2][1])

        self.mask = pygame.mask.from_surface(self.image)
