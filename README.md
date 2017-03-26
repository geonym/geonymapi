# GeonymAPI

Implémentation minimaliste d'une API de conversion Geonym <-> lat/lon

L'API repose sur le module python Falcon, et un module geonym.py


## Installation

`git clone https://github.com/geonym/geonymapi.git`

pour installer les modules pythons nécessaires:

`pip install -r requirements.txt`

L'idéal est de fonctionner dans un virtualenv python3.


## Test / serveur

`gunicorn geonymapi:app -b 0.0.0.0:1405 -w 4`

## Usage

Conversion geonym > lat/lon:
- http://localhost:1405/PP7K-RF4R
- http://localhost:1405/?geonym=PP7K-RF4R

Conversion lat/lon > geonym:
- http://localhost:1405/?lat=48.8&lon=2.35

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

L'algorithme utilisé est identique à OpenPostcode (licence LGPL), avec un alphabet différent destiné à minimiser les ambiguités (8/B, 0/D). Voir: http://www.openpostcode.org/
