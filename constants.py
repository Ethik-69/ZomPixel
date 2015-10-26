#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Les constants utilisées pour le jeu:
- Personnages
- Objets
- Niveaux
- Liste des niveaux
"""

MOVING_SPRITE_X = [0, 75, 150, 225, 300, 375, 450, 525, 600, 675, 750, 825]
DYING_SPRITE_X = [0, 125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375]


citizen = {'name': 'citizen',
           'img': 'character/citizen/citizen_sprite_sheet.png',
           'attack_by_player': 'character/citizen/citizen_attack_by_player.png',
           'attack_by_citizen': 'character/citizen/citizen_attack_by_citizen.png',
           'attack_by_punk': 'character/citizen/citizen_attack_by_punk.png',
           'zombie_img': 'character/citizen/zombie_citizen_sprite_sheet.png'}


punk = {'name': 'punk',
        'img': 'character/punk/punk_sprite_sheet.png',
        'attack_by_player': 'character/punk/punk_attack_by_player.png',
        'attack_by_citizen': 'character/punk/punk_attack_by_citizen.png',
        'attack_by_punk': 'character/punk/punk_attack_by_punk.png',
        'zombie_img': 'character/punk/zombie_punk_sprite_sheet.png'}


OBJECTS = {'manhole_cover': [0, 250, 75, 75],
           'bush': [100, 100, 50, 50],  # buisson
           'blue_car': [0, 20, 230, 120],
           'police_car': [200, 0, 230, 120],
           'yellow_car': [400, 0, 230, 120],
           'cone': [450, 100, 50, 50],
           'working_fence': [0, 150, 100, 50],
           'fence': [550, 100, 50, 50],
           'dich': [550, 100, 50, 50],
           'skull': [100, 100, 50, 50]}


LEVEL0 = {'number': 0,
          'enemy': {(255, 200): citizen,
                    (800, 300): punk},
          'objects': {'manhole_cover': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [],
                      'dich': [],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [0, -1534],
          'pos_player': [512, 354]}

LEVEL1 = {'number': 1,
          'enemy': {(255, 200): citizen,
                    (200, 300): citizen,
                    (255, 400): punk},
          'objects': {'manhole_cover': [],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [-1024, 0],
          'pos_player': [512, 354]}

LEVEL2 = {'number': 2,
          'enemy': {(255, 200): citizen,
                    (255, 400): citizen,
                    (855, 400): punk},
          'objects': {'manhole_cover': [],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [-1024, -768],
          'pos_player': [512, 354]}

LEVEL3 = {'number': 3,
          'enemy': {(255, 200): citizen,
                    (255, 400): citizen,
                    (855, 200): punk,
                    (855, 400): punk},
          'objects': {'manhole_cover': [],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [-1024, -1536],
          'pos_player': [512, 354]}

LEVEL4 = {'number': 4,
          'enemy': {(255, 200): citizen,
                    (255, 400): citizen,
                    (255, 600): citizen,
                    (855, 200): punk,
                    (855, 400): punk,
                    (855, 600): punk},
          'objects': {'manhole_cover': [],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [0, -1536],
          'pos_player': [512, 354]}

LEVELS_LIST = [LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4]
