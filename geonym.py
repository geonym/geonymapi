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

def ll2geonym(lat, lon):
    "Conversion lat/lon -> geonym"
    out = ''
    if (lat>grid_north or lat < grid_south or lon > grid_east or lon < grid_west):
        return None;
    yy = (grid_north - lat) / (grid_north-grid_south) * 5**8
    xx = (lon - grid_west) / (grid_east-grid_west) * 5**8
    y = base5(yy).zfill(8)
    x = base5(xx).zfill(8)
    print(xx,yy,x,y)
    for d in range(0, 8):
        out += grid_alpha[int(y[d])*5+int(x[d])]
    return(out)

def geonym2ll(geonym):
    "Conversion geonym -> lat/lon"
    x = 0
    y = 0
    for d in range(0,len(geonym)):
        p = grid_alpha.find(geonym[d])
        x = x*5 + p % 5
        y = y*5 + p // 5
    north = grid_north - (grid_north-grid_south) * y / (5**len(geonym))
    south = grid_north - (grid_north-grid_south) * (y+1) / (5**len(geonym))
    west = grid_west + (grid_east-grid_west) / (5**len(geonym)) * x
    east = grid_west + (grid_east-grid_west) / (5**len(geonym)) * (x+1)
    return {'geonym':geonym, 'north':north, 'west':west, 'south':south, 'east':east, 'lat': (north+south)/2, 'lon': (west+east)/2}

def checkGeonym(geonym):
    "Vérifie la validité d'un géonym"
    m = re.match(r'^[45673NPR92MXTCLWVDKJHF][456783NPR92MXTC1LWVD0KJHF]*$', geonym.replace('-',''))
    return(m!=None)

def getParams():
    "Paramètres de grille / alphabet"
    return {'max_lat': grid_north, 'min_lat':grid_south,'min_lon':grid_west,'max_lon':grid_east,'alpha':grid_alpha}
