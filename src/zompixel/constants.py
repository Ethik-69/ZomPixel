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

LAYER_POS = {"front": 1, "back": -1}

character_images = {
    "player": {
        "walking_frames_up": [],
        "walking_frames_down": [],
        "walking_frames_left": [],
        "walking_frames_right": [],
        "stop_frame": [],
    },
    "citizen": {
        "walking_frames_up": [],
        "walking_frames_down": [],
        "walking_frames_left": [],
        "walking_frames_right": [],
        "stop_frame": [],
        "attack": {"by_player": [], "by_citizen": [], "by_punk": []},
    },
    "punk": {
        "walking_frames_up": [],
        "walking_frames_down": [],
        "walking_frames_left": [],
        "walking_frames_right": [],
        "stop_frame": [],
        "attack": {"by_player": [], "by_citizen": [], "by_punk": []},
    },
    "z_citizen": {
        "walking_frames_up": [],
        "walking_frames_down": [],
        "walking_frames_left": [],
        "walking_frames_right": [],
        "stop_frame": [],
        "attack": {"by_player": [], "by_citizen": [], "by_punk": []},
    },
    "z_punk": {
        "walking_frames_up": [],
        "walking_frames_down": [],
        "walking_frames_left": [],
        "walking_frames_right": [],
        "stop_frame": [],
        "attack": {"by_player": [], "by_citizen": [], "by_punk": []},
    },
}

# Position x des frames sur les feuilles de sprites
MOVING_SPRITE_X = [0, 75, 150, 225, 300, 375, 450, 525, 600, 675, 750, 825]
DYING_SPRITE_X = [0, 125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375]


player_img = "character/player/zombie_sprite_sheet.png"


# npc = Non-player character / Personnage non joueur
npc = {
    "citizen": {
        "img": "character/citizen/citizen_sprite_sheet.png",
        "attack_by_player": "character/citizen/citizen_attack_by_player.png",
        "attack_by_citizen": "character/citizen/citizen_attack_by_citizen.png",
        "attack_by_punk": "character/citizen/citizen_attack_by_punk.png",
        "zombie_img": "character/citizen/zombie_citizen_sprite_sheet.png",
    },
    "punk": {
        "img": "character/punk/punk_sprite_sheet.png",
        "attack_by_player": "character/punk/punk_attack_by_player.png",
        "attack_by_citizen": "character/punk/punk_attack_by_citizen.png",
        "attack_by_punk": "character/punk/punk_attack_by_punk.png",
        "zombie_img": "character/punk/zombie_punk_sprite_sheet.png",
    },
}

# Dictionnaire des objets
# [0] = path
# [1] = inflatexy pour modifier la taille du rect
# [2] = .center pour modifier son emplacement dans l'image

OBSTACLES = {
    "manhole": ["data/img/objets/manhole.png", (-5, -5), (28, 28)],
    "bush": ["data/img/objets/bush.png", (-13, -13), (32, 32)],
    "blue_car": ["data/img/objets/blue_car.png", (-10, -10), (113, 57)],
    "police_car": ["data/img/objets/police_car.png", (-10, -10), (113, 57)],
    "yellow_car": ["data/img/objets/yellow_car.png", (-10, -10), (113, 57)],
    "cone": ["data/img/objets/cone.png", (-10, -30), (20, 35)],
    "fence": ["data/img/objets/fence.png", (0, -37), (47, 41)],
    "tree": ["data/img/objets/tree.png", (-120, -147), (69, 156)],
    "working_fence_v": ["data/img/objets/working_fence_v.png", (-3, -4), (13, 47)],
    "working_fence_h": ["data/img/objets/working_fence_h.png", (-3, -4), (47, 13)],
    "bin": ["data/img/objets/bin.png", (-7, -30), (17, 40)],
    "skull": ["data/img/objets/skull.png", (0, 0), (0, 0)],  # 0 car pas de collision
    "bench": ["data/img/objets/bench.png", (-5, -5), (49, 15)],
    "phone_box": ["data/img/objets/phone_box.png", (-5, -75), (30, 90)],
}


LEVEL0 = {
    "number": 0,  # Numéro du niveaux
    "enemy": {(200, 350): "citizen"},  # Dictionnaire des enemis
    "objects": {
        "manhole": [(300, 230)],  # Dictionnaire des objets
        "blue_car": [(660, 220)],
        "yellow_car": [(150, 510)],
        "tree": [(500, 50)],
        "bin": [(800, 650)],
        "bench": [(100, 200)],
    },
    "pos_level": [0, -1536],  # Position du niveaux sur la carte
    "pos_player": [512, 354],
}  # Position de départ du joueur


LEVEL1 = {
    "number": 1,
    "enemy": {(255, 568): "citizen", (800, 468): "citizen"},
    "objects": {
        "manhole": [(300, 300)],
        "blue_car": [(140, 520)],
        "yellow_car": [(659, 220)],
        "bench": [(250, 150)],
        "cone": [(250, 290), (365, 290)],
        "bin": [(850, 650)],
    },
    "pos_level": [0, -1534],
    "pos_player": [512, 354],
}


LEVEL2 = {
    "number": 2,
    "enemy": {(255, 568): "citizen", (800, 468): "citizen", (750, 690): "punk"},
    "objects": {
        "manhole": [(151, 463)],
        "bush": [],
        "blue_car": [(660, 220)],
        "phone_box": [(250, 120)],
        "bin": [(450, 640), (490, 640)],
    },
    "pos_level": [0, -1534],
    "pos_player": [512, 354],
}


LEVEL3 = {
    "number": 3,
    "enemy": {
        (255, 528): "citizen",
        (800, 168): "citizen",
        (750, 650): "punk",
        (150, 630): "punk",
    },
    "objects": {
        "manhole": [(351, 300)],
        "yellow_car": [(-75, 100)],
        "bush": [(100, 620), (900, 620)],
        "tree": [(150, 350), (750, 350)],
        "fence": [
            (-1, 525),
            (91, 525),
            (182, 525),
            (274, 525),
            (546, 525),
            (637, 525),
            (728, 525),
            (819, 525),
            (910, 525),
            (1001, 525),
        ],
    },
    "pos_level": [0, -200],
    "pos_player": [512, 354],
}


LEVEL4 = {
    "number": 4,
    "enemy": {
        (255, 528): "citizen",
        (800, 468): "citizen",
        (750, 650): "punk",
        (150, 630): "punk",
    },
    "objects": {
        "yellow_car": [(660, 550)],
        "bush": [(600, 150)],
        "tree": [(100, 200), (700, 200)],
        "manhole": [(200, 460)],
        "fence": [
            (-1, 295),
            (91, 295),
            (182, 295),
            (274, 295),
            (546, 295),
            (637, 295),
            (728, 295),
            (819, 295),
            (910, 295),
            (1001, 295),
        ],
    },
    "pos_level": [0, -1200],
    "pos_player": [512, 354],
}


LEVEL5 = {
    "number": 5,
    "enemy": {
        (255, 528): "citizen",
        (800, 468): "citizen",
        (750, 650): "punk",
        (150, 630): "punk",
    },
    "objects": {
        "bush": [(500, 350), (480, 450), (480, 550), (50, 700)],
        "tree": [(150, 300), (480, 140), (850, 650)],
        "bench": [(750, 320)],
    },
    "pos_level": [0, -768],
    "pos_player": [350, 150],
}


LEVEL6 = {
    "number": 6,
    "enemy": {
        (255, 328): "citizen",
        (800, 468): "citizen",
        (750, 650): "punk",
        (850, 130): "punk",
        (150, 130): "punk",
    },
    "objects": {
        "manhole": [(300, 100), (800, 500)],
        "bush": [],
        "blue_car": [],
        "police_car": [],
        "yellow_car": [(-80, 330)],
        "cone": [(500, 260), (500, 490), (400, 350), (580, 350)],
        "tree": [(445, 315)],
        "bin": [(100, 100)],
        "phone_box": [(880, 100)],
        "working_fence_h": [],
        "fence": [],
    },
    "pos_level": [-1024, 0],
    "pos_player": [200, 600],
}


TEST_LEVEL = {
    "number": "T",
    "enemy": {
        (255, 328): "citizen",
        (800, 468): "citizen",
        (750, 650): "punk",
        (850, 130): "punk",
        (150, 130): "punk",
    },
    "objects": {
        "manhole": [(50, 50)],
        "bush": [(50, 150)],
        "bench": [(50, 250)],
        "blue_car": [(200, 50)],
        "police_car": [],
        "yellow_car": [],
        "cone": [(50, 400)],
        "tree": [(200, 200)],
        "bin": [(800, 600)],
        "phone_box": [(700, 500)],
        "working_fence_h": [(900, 50)],
        "working_fence_v": [(900, 150)],
        "fence": [(900, 300)],
    },
    "pos_level": [-1024, 0],
    "pos_player": [512, 354],
}


# LEVELS_LIST = [LEVEL2]
LEVELS_LIST = [LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5, LEVEL6]


SURVIVAL = {
    "park": {
        "enemy": {
            (150, 120): "citizen",
            (800, 468): "citizen",
            (750, 650): "citizen",
            (150, 630): "citizen",
        },
        "objects": {
            "bush": [(500, 350), (480, 450), (480, 550), (5, 700), (75, 700), (5, 630)],
            "tree": [(150, 300), (480, 140), (850, 650)],
            "bench": [(750, 320)],
            "manhole": [(85, 630), (580, 300), (430, 350)],
        },
        "pos_map": [0, -768],
        "pos_player": [150, 120],
    },
    "street": {
        "enemy": {
            (150, 120): "citizen",
            (800, 468): "citizen",
            (750, 650): "citizen",
            (350, 630): "citizen",
        },
        "objects": {
            "police_car": [(-50, 700), (350, 200), (350, 500)],
            "working_fence_v": [(320, 200), (320, 300), (320, 400), (320, 500)],
            "manhole": [(200, 700), (600, 250), (750, 550)],
        },
        "pos_map": [0, -1534],
        "pos_player": [800, 100],
    },
}
