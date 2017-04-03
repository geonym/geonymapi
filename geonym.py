#!/usr/bin/python3
import re

def base5(decimal) :
    "Conversion decimal > base 5"
    list = "01234"
    answer = ""
    decimal=int(decimal)
    while decimal != 0 :
        answer  = list[decimal % 5]+answer
        decimal = (decimal-(decimal%5)) // 5
    return answer.zfill(8)


# paramètres de grille FR
grid_fr = {"north": 51.45,
           "south": 40.91,
           "west": -5.45,
           "east": 9.8,
           "alphabet":"456783NPR92MXTC1LWVD0KJHF",
           "checksum":"0123456789ACDEFGHJKLMNPQRTUVWXY"}
grid_h = (grid_fr['north']-grid_fr['south'])/5
grid_w = (grid_fr['east']-grid_fr['west'])/5
# paramètres sous-grille FR
grid_fr_sub = [ {"name":"Guyane",   "north":  5.8,  "south":  2,    "west":-55, "east":-50,    "scale":0.5,  "x":0,          "y":0},
                {"name":"Antilles", "north": 17,    "south": 14,    "west":-62, "east":-60.5,  "scale":1,    "x":grid_h,     "y":0},
                {"name":"Réunion",  "north":-20.6,  "south":-21.6,  "west": 55, "east": 56,    "scale":1,    "x":grid_h*4,   "y":0},
                {"name":"Mayotte",  "north":-12.5,  "south":-14,    "west": 45, "east": 45.5,  "scale":1,    "x":grid_h*4+1, "y":0}]

def ll2geonym(lat, lon):
    "Conversion lat/lon -> geonym"
    out = ''
    grid = grid_fr

    # sous-grilles
    for sub in grid_fr_sub:
        if (lat <= sub['north'] and lat >= sub['south'] and lon >= sub['west'] and lon <= sub['east']):
            print(sub['name'])
            lat = (lat - sub['south'])*sub['scale'] + grid['south'] + sub['x']
            lon = (lon - sub['west'])*sub['scale'] + grid['west'] + sub['y']
            break

    if (lat >= grid['north'] or lat <= grid['south'] or lon >= grid['east'] or lon <= grid['west']):
        return None;
    yy = (grid['north'] - lat) / (grid['north']-grid['south']) * 5**8
    xx = (lon - grid['west']) / (grid['east']-grid['west']) * 5**8
    y = base5(yy).zfill(8)
    x = base5(xx).zfill(8)
    for d in range(0, 8):
        out += grid['alphabet'][int(y[d])*5+int(x[d])]
    return(out)

def geonym2ll(geonym):
    "Conversion geonym -> lat/lon"
    x = 0
    y = 0
    grid = grid_fr
    geonym = cleanGeonym(geonym)
    for d in range(0,len(geonym)):
        p = grid['alphabet'].find(geonym[d])
        x = x*5 + p % 5
        y = y*5 + p // 5
    north = grid['north'] - (grid['north']-grid['south']) * y / (5**len(geonym))
    # south = grid['north'] - (grid['north']-grid['south']) * (y+1) / (5**len(geonym))
    south = north - (grid['north']-grid['south']) / (5**len(geonym))
    west = grid['west'] + (grid['east']-grid['west']) / (5**len(geonym)) * x
    east = west + (grid['east']-grid['west']) / (5**len(geonym))
    # east = grid['west'] + (grid['east']-grid['west']) / (5**len(geonym)) * (x+1)

    # recalage pour les DOM
    for sub in grid_fr_sub:
        if north < grid['south'] + sub['x'] + (sub['north']-sub['south'])*sub['scale'] and south > grid['south'] + sub['x'] and west > grid['west'] + sub['y'] and east < grid['west'] + sub['y'] + (sub['east']-sub['west'])*sub['scale']:
          north = (north-grid['south']-sub['x'])/sub['scale'] + sub['south']
          south = (south-grid['south']-sub['x'])/sub['scale'] + sub['south']
          west = (west-grid['west']-sub['y'])/sub['scale'] + sub['west']
          east = (east-grid['west']-sub['y'])/sub['scale'] + sub['west']
          break

    return {'geonym':geonym, 'north':north, 'west':west, 'south':south, 'east':east, 'lat': (north+south)/2, 'lon': (west+east)/2}

def checkGeonym(geonym):
    "Vérifie la validité d'un géonym"
    m = re.match(r'^[456783NPR92MXTC1LWVD0KJHF]*(|/[0123456789ACDEFGHJKLMNPQRTUVWXY])$', geonym.upper().replace('-',''))
    return(m!=None)


def cleanGeonym(geonym):
    geonym = geonym.upper().replace('-','')
    # strip checksum
    if geonym.find('/')>0:
        geonym = geonym[:geonym.find('/')]

    # remplacement erreurs alphabet
    geonym = geonym.replace('A','4')
    geonym = geonym.replace('B','8')
    geonym = geonym.replace('E','F')
    geonym = geonym.replace('G','6')
    geonym = geonym.replace('I','1')
    geonym = geonym.replace('O','0')
    geonym = geonym.replace('Q','0')
    geonym = geonym.replace('S','5')
    geonym = geonym.replace('U','V')
    geonym = geonym.replace('Y','V')
    geonym = geonym.replace('Z','2')
    return geonym


def getParams():
    "Paramètres de grille / alphabet"
    return {'max_lat': grid_fr['north'], 'min_lat':grid_fr['south'],'min_lon':grid_fr['west'],'max_lon':grid_fr['east'],'alpha':grid_fr['alphabet']}

def checksum(geonym):
    "Calcule de checksum d'un géonym"
    geonym = cleanGeonym(geonym)
    if len(geonym)!=8:
        return None
    grid = grid_fr
    c = 0
    for p in range(0,len(geonym)):
        c += grid['alphabet'].find(geonym[p])*(p+1)
    return(grid['checksum'][c % 31])
