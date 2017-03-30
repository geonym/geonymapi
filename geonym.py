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
grid_north = 51.45
grid_west  = -5.45
grid_south = 40.91
grid_east = 9.8
grid_alpha = "456783NPR92MXTC1LWVD0KJHF"
grid_h = (grid_north-grid_south)/5
grid_w = (grid_east-grid_west)/5

# paramètres sous-grille FR
grid_sub = [{"name":"Guyane",   "north":5.8,    "south":2,      "west":-55, "east":-50,     "scale":0.5,    "x":0,          "y":0},
            {"name":"Antilles", "north":17,     "south":14,     "west":-62, "east":-60.5,   "scale":1,      "x":grid_h,     "y":0},
            {"name":"Réunion",  "north":-20.6,  "south":-21.6,  "west":55,  "east":56,      "scale":1,      "x":grid_h*4,   "y":0},
            {"name":"Mayotte",  "north":-12.5,  "south":14,     "west":45,  "east":45.5,    "scale":1,      "x":grid_h+1,   "y":0}]

def ll2geonym(lat, lon):
    "Conversion lat/lon -> geonym"
    out = ''

    # sous-grilles
    if (lat<=5.8 and lat>=2 and lon>=-55 and lon<=-50): # guyane > zone '0'
        lat = (lat-2)*0.5 + grid_south
        lon = (lon+55)*0.5 + grid_west
    elif (lat<=-20.6 and lat>=-21.6 and lon>=55 and lon<=56): # réunion > zone '4'
        lat = (lat+21.6)*1 + grid_south + grid_h*4
        lon = (lon-55)*1 + grid_west
    elif (lat<=17 and lat>=14 and lon>=-62 and lon<=-60.5): # martinique/guadeloupe > zone '1'
        lat = (lat-14)*1 + grid_south + grid_h
        lon = (lon+62)*1 + grid_west
    elif (lat<=-12.5 and lat>=-13.5 and lon>=45 and lon<=45.5): # mayotte > zone '4'
        lat = (lat+13.5)*1 + grid_south + grid_h*4 + 1
        lon = (lon-45)*1 + grid_west

    if (lat >= grid_north or lat <= grid_south or lon >= grid_east or lon <= grid_west):
        return None;
    yy = (grid_north - lat) / (grid_north-grid_south) * 5**8
    xx = (lon - grid_west) / (grid_east-grid_west) * 5**8
    y = base5(yy).zfill(8)
    x = base5(xx).zfill(8)
    for d in range(0, 8):
        out += grid_alpha[int(y[d])*5+int(x[d])]
    return(out)

def geonym2ll(geonym):
    "Conversion geonym -> lat/lon"
    x = 0
    y = 0

    geonym = cleanGeonym(geonym)
    for d in range(0,len(geonym)):
        p = grid_alpha.find(geonym[d])
        x = x*5 + p % 5
        y = y*5 + p // 5
    north = grid_north - (grid_north-grid_south) * y / (5**len(geonym))
    # south = grid_north - (grid_north-grid_south) * (y+1) / (5**len(geonym))
    south = north - (grid_north-grid_south) / (5**len(geonym))
    west = grid_west + (grid_east-grid_west) / (5**len(geonym)) * x
    east = west + (grid_east-grid_west) / (5**len(geonym))
    # east = grid_west + (grid_east-grid_west) / (5**len(geonym)) * (x+1)

    # décalage pour les DOM
    if geonym[0]=='0': # guyane
      north = (north-grid_south)/0.5 + 2
      south = (south-grid_south)/0.5 + 2
      west = (west-grid_west)/0.5 - 55
      east = (east-grid_west)/0.5 - 55
    elif north < grid_south+grid_h*2 and east<grid_west+3: # martinique/guadeloupe
      north = (north-grid_south-grid_h)/1 + 14
      south = (south-grid_south-grid_h)/1 + 14
      west = (west-grid_west)/1 -62
      east = (east-grid_west)/1 -62
    elif north > grid_south+grid_h*4+1 and east<grid_west+1: # mayotte
      north = (north-grid_south-grid_h*4-1)/1 -13.5
      south = (south-grid_south-grid_h*4-1)/1 -13.5
      west = (west-grid_west)/1 +45
      east = (east-grid_west)/1 +45
    elif north > grid_south+grid_h*4 and east<grid_west+1: # réunion
      north = (north-grid_south-grid_h*4)/1 - 21.6
      south = (south-grid_south-grid_h*4)/1 - 21.6
      west = (west-grid_west)/1 + 55
      east = (east-grid_west)/1 + 55

    return {'geonym':geonym, 'north':north, 'west':west, 'south':south, 'east':east, 'lat': (north+south)/2, 'lon': (west+east)/2}

def checkGeonym(geonym):
    "Vérifie la validité d'un géonym"
    m = re.match(r'^[456783NPR92MXTC1LWVD0KJHF]*$', cleanGeonym(geonym).upper().replace('-',''))
    return(m!=None)


def cleanGeonym(geonym):
    geonym = geonym.upper().replace('-','')

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
    return {'max_lat': grid_north, 'min_lat':grid_south,'min_lon':grid_west,'max_lon':grid_east,'alpha':grid_alpha}
