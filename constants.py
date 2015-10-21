#!/usr/bin/env python
# -*- coding:utf-8 -*-


MOVING_SPRITE_X = [0, 75, 150, 225, 300, 375, 450, 525, 600, 675, 750, 825]
DYING_SPRITE_X = [0, 125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375]


citizen0 = {'nom': 'citizen0',
            'pos_x': 255,
            'pos_y': 200,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}

citizen1 = {'nom': 'citizen1',
            'pos_x': 255,
            'pos_y': 400,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}

citizen2 = {'nom': 'citizen2',
            'pos_x': 655,
            'pos_y': 200,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}

citizen3 = {'nom': 'citizen3',
            'pos_x': 655,
            'pos_y': 400,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}

citizen4 = {'nom': 'citizen4',
            'pos_x': 500,
            'pos_y': 640,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}

citizen5 = {'nom': 'citizen5',
            'pos_x': 500,
            'pos_y': 250,
            'img': 'character/citizen_sprite_sheet.png',
            'attack_img': 'actions/citizen_attack_by_player.png'}


punk0 = {'nom': 'punk0',
         'pos_x': 255,
         'pos_y': 200,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

punk1 = {'nom': 'punk1',
         'pos_x': 255,
         'pos_y': 400,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

punk2 = {'nom': 'punk2',
         'pos_x': 655,
         'pos_y': 200,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

punk3 = {'nom': 'punk3',
         'pos_x': 655,
         'pos_y': 400,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

punk4 = {'nom': 'punk4',
         'pos_x': 500,
         'pos_y': 640,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

punk5 = {'nom': 'punk5',
         'pos_x': 500,
         'pos_y': 250,
         'img': 'character/punk_sprite_sheet.png',
         'attack_img': 'actions/punk_attack_by_player.png'}

OBJECTS = {'manhole_cover': [0, 100, 50, 50],
           'hydrant': [50, 100, 50, 50],  # bouche d'incendie
           'bush': [100, 100, 50, 50],  # buisson
           'blue_car': [0, 0, 200, 100],
           'police_car': [200, 0, 200, 100],
           'yellow_car': [400, 0, 200, 100],
           'cone': [450, 100, 50, 50],
           'working_fence': [0, 150, 100, 50],
           'fence': [550, 100, 50, 50],
           'skull': [500, 100, 50, 50]}


LEVEL0 = {'number': 0,
          'enemy': [citizen0, citizen1],
          'objects': {'manhole_cover': [],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [(550, 500)],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [(300, 350)],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [0, -1534],
          'pos_player': [512, 354]}

LEVEL1 = {'number': 1,
          'enemy': [citizen0, citizen1, punk2],
          'objects': {'manhole_cover': [(350, 350)],
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
          'enemy': [citizen0, citizen1, punk2, punk3],
          'objects': {'manhole_cover': [(350, 350)],
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
          'enemy': [citizen0, citizen1, citizen2, punk3, punk4],
          'objects': {'manhole_cover': [(350, 350)],
                      'hydrant': [],
                      'bush': [],
                      'blue_car': [],
                      'police_car': [],
                      'yellow_car': [],
                      'cone': [(300,350)],
                      'working_fence': [],
                      'fence': []},
          'pos_level': [-1024, -1536],
          'pos_player': [512, 354]}

LEVEL4 = {'number': 4,
          'enemy': [citizen0, citizen1, citizen2, punk3, punk4, punk5],
          'objects': {'manhole_cover': [(350, 350)],
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

# LEVELS_LIST = [LEVEL0]
LEVELS_LIST = [LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4]
