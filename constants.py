#!/usr/bin/env python
# -*- coding:utf-8 -*-


MOVING_SPRITE_X = [0, 75, 150, 225]
DYING_SPRITE_X = [0, 125, 250, 375, 500, 625, 750, 875]


citizen0 = {'nom': 'citizen0', 'pos_x': 255, 'pos_y': 200, 'img': 'character/citizen_sprite_sheet.png'}
citizen1 = {'nom': 'citizen1', 'pos_x': 255, 'pos_y': 400, 'img': 'character/citizen_sprite_sheet.png'}
citizen2 = {'nom': 'citizen2', 'pos_x': 655, 'pos_y': 200, 'img': 'character/citizen_sprite_sheet.png'}
citizen3 = {'nom': 'citizen3', 'pos_x': 655, 'pos_y': 400, 'img': 'character/citizen_sprite_sheet.png'}
citizen4 = {'nom': 'citizen4', 'pos_x': 500, 'pos_y': 640, 'img': 'character/citizen_sprite_sheet.png'}
citizen5 = {'nom': 'citizen5', 'pos_x': 500, 'pos_y': 250, 'img': 'character/citizen_sprite_sheet.png'}
citizen6 = {'nom': 'citizen6', 'pos_x': 550, 'pos_y': 300, 'img': 'character/citizen_sprite_sheet.png'}


LEVEL0 = {'number': 0,
          'enemy': [citizen0, citizen1],
          'objects': [],
          'pos_level': [0, 0],
          'pos_player': [512, 354]}

LEVEL1 = {'number': 1,
          'enemy': [citizen0, citizen1, citizen2, citizen3],
          'objects': [],
          'pos_level': [-1024, 0],
          'pos_player': [512, 354]}

LEVEL2 = {'number': 2,
          'enemy': [citizen0, citizen1, citizen2, citizen3, citizen4, citizen5],
          'objects': [],
          'pos_level': [0, -768],
          'pos_player': [512, 354]}

LEVEL3 = {'number': 3,
          'enemy': [citizen0, citizen1, citizen2, citizen3, citizen4, citizen5, citizen6],
          'objects': [],
          'pos_level': [-2048, 0],
          'pos_player': [512, 354]}

LEVEL4 = {'number': 4,
          'enemy': [citizen0, citizen1, citizen2, citizen3, citizen4, citizen5, citizen6],
          'objects': [],
          'pos_level': [-1024, -768],
          'pos_player': [512, 354]}

LEVELS_LIST = [LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4]
