# ZompiGame

Le jeu dans lequel VOUS etes le zombie (Pour une fois...)


## Installation

1. Installer [Python (2.7)](https://www.python.org/)
2. Installer [Pygame](http://www.pygame.org/download.shtml)
3. Installer [Rethinkdb](https://www.rethinkdb.com/)


## Lancement

1. Aller dans le dossier du jeu et avec le terminal lancer rethinkdb (commande: rethinkdb)
2. Lancer main.py (commande: python main.py)

Le jeu ne fonctionnera pas simplement avec les sources, ils vous faudra les images qui vont avec, 
que vous trouverez sur le site dans le zip contenant le jeu en .exe (lien plus bas))


## Implementation

- `main.py`:  Gère l'import de pygame et lance le jeu.

- `constants.py`: Les constantes du jeu.

- `title_screen.py`: Gère l'affichage du menu principal.

- `campagne.py`: Gère l'affichage de la campagne.

- `survival.py`: Gère l'affichage du survival.

- `levels.py`: Gère les niveaux, création, update, changement... (campagne et survival)

- `manager.py`: Gère la création, suppression, update des PNJ (Personnage Non Joueur)
   ainsi que la création des obstacles.

- `character.py`: Coeur des PNJ (IA... Si on peu appeler ça une IA...)

- `player.py`: Pareil que `character.py` mais exclusivement pour le joueur.

- `sprites.py`: Charge et découpe les images du jeu (sprite sheet)

- `time_made_home.py`: Gestion du temp "fait maison" (pas la mienne, si je retrouve les sources je les mettrait)

- `db_setup.py`: Configuration de la base de donnée (rethinkdb)

- `db_manager.py`: Gestion de la base de donnée (Insert, delete, modif...)

## Site web

[ZompiGame](http://zompigame.net)
