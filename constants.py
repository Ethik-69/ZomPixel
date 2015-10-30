#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Les constants utilisées pour le jeu:
- Personnages
- Objets
- Niveaux
- Liste des niveaux
"""

GAME_WIDTH = 1024
GAME_HEIGHT = 768

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


OBJECTS = {'manhole': "data/img/objets/manhole.png",
           'bush': "data/img/objets/bush.png",
           'blue_car': "data/img/objets/blue_car.png",
           'police_car': "data/img/objets/police_car.png",
           'yellow_car': "data/img/objets/yellow_car.png",
           'cone': "data/img/objets/cone.png",
           'tree': "data/img/objets/tree.png",
           'working_fence_v': "data/img/objets/working_fence_v.png",
           'working_fence_h': "data/img/objets/working_fence_h.png",
           'fence': "data/img/objets/fence.png",
           'bin': "data/img/objets/bin.png",
           'skull': "data/img/objets/skull.png",
           'bench': "data/img/objets/bench.png",
           'phone_box': "data/img/objets/phone_box.png"}


LEVEL0 = {'number': 0,
          'enemy': {(200, 350): citizen},
          'objects': {'manhole': [(300, 230)],
                      'blue_car': [(660, 220)],
                      'yellow_car': [(150, 510)],
                      'tree': [(550, 50)],
                      'bin': [(800, 650)]},
          'pos_level': [0, -1536],
          'pos_player': [512, 354]}

LEVEL1 = {'number': 1,
          'enemy': {(255, 568): citizen,
                    (800, 468): citizen},
          'objects': {'manhole': [(300, 300)],
                      'blue_car': [(140, 520)],
                      'yellow_car': [(659, 220)],
                      'bench': [(250, 150)],
                      'cone': [(250, 290), (365, 290)],
                      'bin': [(850, 650)]},
          'pos_level': [0, -1534],
          'pos_player': [512, 354]}

LEVEL2 = {'number': 2,
          'enemy': {(255, 568): citizen,
                    (800, 468): citizen,
                    (750, 690): punk},
          'objects': {'manhole': [(151, 463)],
                      'bush': [],
                      'blue_car': [(660, 220)],
                      'phone_box': [(250, 120)],
                      'bin': [(450, 640), (490, 640)]},
          'pos_level': [0, -1534],
          'pos_player': [512, 354]}

LEVEL3 = {'number': 3,
          'enemy': {(255, 528): citizen,
                    (800, 168): citizen,
                    (750, 650): punk,
                    (150, 630): punk},
          'objects': {'manhole': [(351, 300)],
                      'yellow_car': [(-75, 100)],
                      'bush': [(100, 620), (900, 620)],
                      'tree': [(150, 350), (750, 350)],
                      'fence': [(-1, 525), (91, 525),
                                (182, 525), (274, 525),
                                (546, 525), (637, 525),
                                (728, 525), (819, 525),
                                (910, 525), (1001, 525)]},
          'pos_level': [0, -200],
          'pos_player': [512, 354]}

LEVEL4 = {'number': 4,
          'enemy': {(255, 528): citizen,
                    (800, 468): citizen,
                    (750, 650): punk,
                    (150, 630): punk},
          'objects': {'manhole': [(300, 650)],
                      'bush': [(600, 150)],
                      'yellow_car': [(660, 550)],
                      'tree': [(100, 200), (700, 200)],
                      'fence': [(-1, 295), (91, 295),
                                (182, 295), (274, 295),
                                (546, 295), (637, 295),
                                (728, 295), (819, 295),
                                (910, 295), (1001, 295)]},
          'pos_level': [0, -1200],
          'pos_player': [512, 354]}

LEVEL5 = {'number': 5,
          'enemy': {(255, 528): citizen,
                    (800, 468): citizen,
                    (750, 650): punk,
                    (150, 630): punk},
          'objects': {'bush': [(500, 350), (480, 450), (480, 550), (50, 700)],
                      'tree': [(150, 300), (480, 140), (850, 650)],
                      'bench': [(750, 320)]},
          'pos_level': [0, -768],
          'pos_player': [350, 150]}

LEVEL6 = {'number': 6,
          'enemy': {(255, 328): citizen,
                    (800, 468): citizen,
                    (750, 650): punk,
                    (850, 130): punk,
                    (150, 130): punk},
          'objects': {'manhole': [(300, 100), (800, 500)],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [(-80, 330)],
                      'cone': [(500, 260), (500, 490),
                               (400, 350), (580, 350)],
                      'tree': [(445, 315)],
                      'bin': [(100, 100)],
                      'phone_box': [(880, 100)],
                      'working_fence_h': [],
                      'fence': []},
          'pos_level': [-1024, 0],
          'pos_player': [200, 600]}

LEVELS_LIST = [LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6]
