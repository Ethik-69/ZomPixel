#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zompixel.title_screen import TitleScreen
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger('root')


if __name__ == "__main__":
    while True:
        LOGGER.info("[*] Game Object Init")
        game = TitleScreen()
        game.start()

    # TODO: zombie alliés traverse les barriere ???
    # TODO: Changer layer zombie/player
    # TODO: ajouter layer objet pour le niveau 4 arbre/barriere
    # TODO: Site web
    # -Page
    # -Accueil (présentation du jeu ajouter text)
    # -Download Ok
    # -Rating Ok
    # -Contact Ok
    # -Sécurisé le site
    # -Hebergement : digital ocean
    # -Install + config srv Ok (Flask Ok Lamp Ok)
    # -acces admin rethinkdb Ok
    # -acces rethinkdb app En cours
    # -Integration site A faire
    # -Responsive Presque
    # TODO: Refacto (2em passage à faire)
    # pygame book example:
    #   homing missiles / targeting (les zombies suivent les citoyens)
    # TODO: Recherche 'IA'

    # RETOUR: - Plus nerveux
    #     - Amélioration collision
    #     - Ajouter des personnages féminin
