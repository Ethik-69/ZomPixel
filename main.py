#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from title_screen import *

try:
    from pygame.locals import *
except ImportError, errmsg:
    print('Requires PyGame')
    print(errmsg)
    sys.exit(1)

__author__ = "The_System69 (Ethan CHAMIK)"

if __name__ == '__main__':
    while True:
        print('[*] Game Object Init')
        game = TitleScreen()
        game.start()

    # TODO: zombie alliés traverse les barriere ???
    # TODO: Changer layer zombie/player
    # TODO: ajouter layer objet pour le niveau 4 arbre/barriere
    # TODO: Site web
        # -Sécurisé le site
        # -Responsive
    # TODO: TP:
        # -readme En cours
        # -Doc Ok
        # -Cahier des charges En cours
        # -Diagramme objets
        # -Remplir ECF.odt
    # TODO: Refacto (2em passage à faire)
    # pygame book example:
    #   homing missiles / targeting (les zombies suivent les citoyens)
    # TODO: Recherche 'IA'

    # RETOUR: - Plus nerveux
        #     - Amélioration collision
        #     - Ajouter des personnages féminin

    # TODO at :
        # campagne : 252
        # character : 220-281-165
