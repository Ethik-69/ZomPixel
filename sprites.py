#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame


class SpriteSheet(object):
    """Permet de 'découper' la planche de sprite pour avoir seulement l'image voulu"""
    def __init__(self, file_name):
        self.sheet = pygame.image.load(file_name).convert()

    def get_frames(self, walking_frames, x, y, width, height, flip=False):
        for x in x:
            img = self.get_image(x, y, width, height)
            if flip:
                img = pygame.transform.flip(img, True, False)
            walking_frames.append(img)
        return walking_frames

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height)).convert()
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image
