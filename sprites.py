#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame


class SpriteSheet(object):
    """Permet de 'découper' la planche de sprite pour avoir seulement l'image voulu"""
    def __init__(self):
        self.sheet = None

    def get_character_frames(self, walking_frames, x, y, width, height, file_name, flip=False):
        """Decoupe les frames demander"""
        self.sheet = pygame.image.load(file_name).convert()
        for x in x:
            img = self.get_image(x, y, width, height, self.sheet)
            if flip:
                img = pygame.transform.flip(img, True, False)
            walking_frames.append(img)
        return walking_frames

    def get_image(self, x, y, width, height, img, solo_use=False):
        """Découpe l'image demander"""
        if solo_use:
            img = pygame.image.load(img).convert()
        image = pygame.Surface((width, height)).convert()
        image.blit(img, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image
