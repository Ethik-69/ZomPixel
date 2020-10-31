#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class Player(pygame.sprite.Sprite):
    def __init__(self, name, images, all_sprites, x, y, width, height):
        self._layer = 1
        self.pos_on_layer = None
        self.is_layer_change = False  # Pour effectuer le changement de layer
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

        self.action = ""
        self.action_switch = {
            "up": self.move_up,
            "down": self.move_down,
            "left": self.move_left,
            "right": self.move_right,
        }

        # Gestion des frames
        self.time_target = 40
        self.time_num = 0
        self.current_image = 0
        self.stop_frame = images["stop_frame"]
        self.image = self.stop_frame
        self.frames_switch = {
            "up": images["walking_frames_up"],
            "down": images["walking_frames_down"],
            "left": images["walking_frames_left"],
            "right": images["walking_frames_right"],
        }

        # Rect de base
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Rect pour les collision avec les objets
        self.collision_rect = self.image.get_rect()
        self.collision_rect.inflate_ip(-5, -80)
        self.collision_rect.center = (self.rect.x + 37, self.rect.y + 95)

        # Hitbox (collision enemis/joueur)
        self.hitbox_rect = self.image.get_rect()
        self.hitbox_rect.inflate_ip(-5, -85)
        self.hitbox_rect.center = (self.rect.x + 37, self.rect.y + 70)

        # Pour les circle collisions
        self.radius = 200

        # Pour les collisions "pixel perfect" (pixel/pixel)
        self.mask = pygame.mask.from_surface(self.image)

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
        """Reinitialise la position du joueur"""
        self.rect.x = x
        self.rect.y = y
        self.collision_rect.center = (self.rect.x + 37, self.rect.y + 95)
        self.hitbox_rect.center = (self.rect.x + 37, self.rect.y + 70)

    def collide_window_side(self):
        """Test de collision avec les bords de la fenêtre"""
        if self.rect.x <= self.width / 2 and self.moveX < 0:
            self.moveX = 0

        if self.rect.x > self.game_width - self.width / 2 and self.moveX > 0:
            self.moveX = 0

        if self.rect.y <= self.height / 3 and self.moveY < 0:
            self.moveY = 0

        if self.rect.y > self.game_height - self.height and self.moveY > 0:
            self.moveY = 0

    def change_layer_test(self, obstacle):
        """Gère le changement de layer"""
        if self.collision_rect.top < obstacle.collision_rect.bottom - 2:
            if self.pos_on_layer != "back":
                self.is_layer_change = True
                self.pos_on_layer = "back"

        elif self.pos_on_layer != "front":
            self.is_layer_change = True
            self.pos_on_layer = "front"

    def obstacle_collide(self, obstacles_list):
        """Collision joueur-objets"""
        if not self.is_feeding:
            obstacles_collided = pygame.sprite.spritecollide(
                self, obstacles_list, False
            )

            for obstacle in obstacles_collided:
                self.change_layer_test(obstacle)

                LOGGER.info("[*] Player Collide Object")
                if obstacle.name == "manhole":
                    if self.collision_rect.colliderect(obstacle.collision_rect):
                        self.dying = True
                        LOGGER.info("[*] Launch Game Over")

                elif self.collision_rect.colliderect(obstacle.collision_rect):
                    if (
                        self.collision_rect.x <= obstacle.collision_rect.x
                        and self.moveX > 0
                    ):
                        self.moveX = 0

                    if (
                        self.collision_rect.x >= obstacle.collision_rect.x
                        and self.moveX < 0
                    ):
                        self.moveX = 0

                    if (
                        self.collision_rect.y <= obstacle.collision_rect.y
                        and self.moveY > 0
                    ):
                        self.moveY = 0

                    if (
                        self.collision_rect.y >= obstacle.collision_rect.y
                        and self.moveY < 0
                    ):
                        self.moveY = 0

    def circle_collide(self, enemy_sprites):
        """Collision circulaire enemis/joueur"""
        for enemy in enemy_sprites:
            if not enemy.is_under_attack and pygame.sprite.collide_circle(self, enemy):
                if not enemy.is_circle_collide:
                    LOGGER.info(
                        "[*] " + enemy.name + str(enemy.num) + " Collide Circle"
                    )
                    enemy.set_opposite_action()
                    enemy.is_circle_collide = True

                if not enemy.is_crazy:
                    enemy.become_crazy()

            elif enemy.is_circle_collide:
                enemy.is_circle_collide = False

    def collide(self, enemy_sprites):
        """Collision enemis/joueur"""
        if not self.is_feeding:
            enemy_hit_list = pygame.sprite.spritecollide(self, enemy_sprites, False)

            for enemy in enemy_hit_list:
                if not self.is_feeding and not enemy.is_under_attack:
                    if self.hitbox_rect.colliderect(enemy.hitbox_rect):
                        LOGGER.info("[*] Hitbox Collide - Player")
                        enemy.under_attack(self)
                        self.is_feeding = True

    def update(self, obstacles_list, enemy_sprites):
        """Met à jour le joueur"""
        if self.is_feeding:  # si le joueur est en train de manger, ne l'affiche pas
            self.rect.x = -100  # Hors de l'écran
            self.rect.y = -100

        elif self.rect.x == -100:
            self.rect.x, self.rect.y = self.x, self.y

        else:
            self.collide_window_side()
            self.obstacle_collide(obstacles_list)
            self.circle_collide(enemy_sprites)
            self.collide(enemy_sprites)

            # Déplace le joueur
            self.rect = self.rect.move([self.moveX, self.moveY])
            self.collision_rect = self.collision_rect.move([self.moveX, self.moveY])
            self.hitbox_rect = self.hitbox_rect.move([self.moveX, self.moveY])
            self.x, self.y = self.rect.x, self.rect.y

            # Met à jour la frame
            self.time_num += 1
            if self.time_num == self.time_target:
                self.time_num = 0
                self.current_image += 1

                if self.current_image == 4:
                    self.current_image = 0

            if self.action != "":
                self.image = self.frames_switch[self.action][self.current_image]

            else:
                self.image = self.stop_frame
