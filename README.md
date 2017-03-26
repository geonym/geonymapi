# GeonymAPI

Implémentation minimaliste d'une API de conversion Geonym <-> lat/lon

L'API repose sur le module python Falcon, et un module geonym.py

## À propos des Géonym

Un geonym est une traduction sous forme de chaine de caractère d'une position géographique.
Plus cette chaine est longue, plus le geonym correspond à une petite zone géographique.

P = zone de 234km x 234km
PP = zone de 47km x 47km inclue dans celle de 'P'
PP7 = zone de 9 x 9km inslue dans celle de 'PP'
...
PP7K-RF4V = zone de 3m x 3m correspondant à l'entrée de la Tour Mirabeau à Paris

Voir: http://www.geonym.fr/visu/#19/48.84687/2.27924

L'algorithme utilisé est identique à OpenPostcode (licence LGPL), avec un alphabet différent.

Les caractères utilisés sont limités aux chiffres de 0 à 9 et aux consonnes non ambigües (0/D/O, 1/I, 2/Z, 4/A, 5/S, 6/G, 8/B).

![Alphabet geonym et répartition en spirale](https://raw.githubusercontent.com/geonym/visugeonym/master/img/geonym.svg)


## Installation

`git clone https://github.com/geonym/geonymapi.git`

pour installer les modules pythons nécessaires:

`pip install -r requirements.txt`

L'idéal est de fonctionner dans un virtualenv python3.


## Test / serveur

`gunicorn geonymapi:app -b 0.0.0.0:1405 -w 4`

ou pour fonctionner en daemon avec rechargement automatique lorsque le code est modifié:

`gunicorn geonymapi:app -b 0.0.0.0:1405 -w 4 --reload -D`


## Usage

Conversion geonym > lat/lon:
- http://api.geonym.fr/PP7K-RF4R
- http://api.geonym.fr/?geonym=PP7K-RF4R

Conversion lat/lon > geonym:
- http://api.geonym.fr/?lat=48.8&lon=2.35

Réponse:
```{
    "geometry": {
        "coordinates": [
            2.283656128,
            48.85509449728001
        ],
        "type": "Point"
    },
    "params": {
        "alpha": "456783NPR92MXTC1LWVD0KJHF",
        "max_lat": 51.45,
        "max_lon": 9.8,
        "min_lat": 40.91,
        "min_lon": -5.45
    },
    "properties": {
        "east": 2.2836600320000002,
        "geonym": "PP7K-RF4R",
        "lat": 48.85509449728001,
        "lon": 2.283656128,
        "north": 48.85509719552,
        "south": 48.855091799040004,
        "west": 2.283652224
    },
    "type": "Feature"
}
```

- north/west/south/east sont les limites du geonym
- lat/lon correspond au centre de la bbox du geonym
- params contient les paramètres de la grille (alphabet et limites géographiques)