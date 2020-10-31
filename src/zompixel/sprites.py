#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")


class SpriteSheet(object):
    """Gestion des feuilles de sprites"""

    def __init__(self):
        self.sheet = None

    def set_img(self, file_name):
        """Charge la feuille de sprite"""
        self.sheet = pygame.image.load("data/img/" + file_name).convert()

    def get_character_frames(self, walking_frames, x, y, width, height, flip=False):
        """Decoupe les frames demandées"""
        for x in x:
            img = self.get_image(x, y, width, height, self.sheet)

            if flip:
                img = pygame.transform.flip(img, True, False)

            walking_frames.append(img)

        return walking_frames

    @staticmethod
    def get_image(x, y, width, height, img):
        """Découpe l'image demandée"""
        image = pygame.Surface((width, height)).convert()
        image.blit(img, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image
