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

__author__ = "Thibault, Romain -> images Ethan -> Code"

if __name__ == '__main__':
    while True:
        print('[*] Game Object Init')
        game = TitleScreen()
        game.start()

    # TODO: Changer layer zombie/player
    # TODO: ajouter layer objet pour le niveau 4 arbre/barriere
    # TODO: Site web
        # -Page
            # -Accueil Ok
            # -Download Ok
            # -Rating Ok
            # -Contact Ok
        # -Sécurisé le site
        # -Responsive Plus ou Moins Ok
        # -Hebergement : digital ocean
            # -Install + config srv Ok (Flask Ok Lamp Ok)
            # -acces admin rethinkdb Ok
            # -acces rethinkdb app Ok
            # -Integration site Ok
    # TODO: DB
        # -db_manager Ok
        # -Integration survival (db Ok img Ok gestion input nom joueur Ok)
        # -Integration page web Ok
    # TODO: TP:
        # -readme En cours
        # -Doc En cours
        # -Cahier des charges En cours
        # -Diagramme objets
        # -Remplir ECF.odt
    # TODO: Refacto
    # pygame book example:
    #   homing missiles / targeting (les zombies suivent les citoyens)
    # TODO: Recherche 'IA'

    # RETOUR: - Plus nerveux
        #     - Amélioration collision
        #     - Ajouter des personnages féminin
