#!/usr/bin/python3

import falcon
import json
import requests
from pyproj import Proj, transform

import geonym

class HeaderMiddleware:

    def process_response(self, req, resp, resource):
        resp.set_header('X-Powered-By', 'GeonymAPI')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        resp.set_header('Access-Control-Allow-Methods','GET')

URL_GEOCODER = 'http://api-adresse.data.gouv.fr'

class GeonymResource(object):
    def getGeonym(self, req, resp, query=None):
        resp.status = falcon.HTTP_200
        geo = None

        # projections utilisées pour transformation en WGS84/Lambert93
        s_srs = Proj(init='EPSG:2154')
        t_srs = Proj(init='EPSG:4326')

        if 'x' in req.params and 'y' in req.params:
            lon,lat = transform(s_srs,t_srs,req.params['x'],req.params['y'])
            query = geonym.ll2geonym(lat, lon)
        elif 'lat' in req.params and 'lon' in req.params:
            query = geonym.ll2geonym(float(req.params['lat']), float(req.params['lon']))
        elif 'geonym' in req.params:
            query = req.params['geonym']
        elif 'adresse' in req.params:
            r = requests.get(URL_GEOCODER+'/search', params={"q":req.params['adresse'], "autocomplete":0, "limit":1}, timeout=1)
            geo = json.loads(r.text)
            geo['source']=URL_GEOCODER
            query = geonym.ll2geonym(geo['features'][0]['geometry']['coordinates'][1], geo['features'][0]['geometry']['coordinates'][0])

        if query is not None and geonym.checkGeonym(query):
            rev = None
            data = geonym.geonym2ll(query)
            if 'reverse' in req.params and req.params['reverse']=='yes':
                r = requests.get(URL_GEOCODER+'/reverse', params={"lat":data['lat'],"lon":data['lon'],"limit":1}, timeout=1)
                if r.status_code == 200:
                    rev = json.loads(r.text)
                    rev['source']=URL_GEOCODER

            x,y = transform(t_srs,s_srs,data['lon'],data['lat'])
            # on ne retourne les coordonnées Lambert que si on est en zone Lambert93
            if y > -357823.2365 and x > 6037008.6939 and y < 1313632.3628 and x< 7230727.3772:
                data['x'] = int(x)
                data['y'] = int(y)

            geojson = {"type":"Feature",
                "properties":data,
                "link": "http://www.geonym.fr/visu/?g=%s" % (query.upper(),)),
                "params":geonym.getParams(),
                "geometry":{"type":"Polygon","coordinates":[[[data['west'],data['south']],[data['east'],data['south']],[data['east'],data['north']],[data['west'],data['north']],[data['west'],data['south']]]]}}
            if rev is not None:
                geojson['reverse'] = rev
            if geo is not None:
                geojson['geocode'] = geo
            resp.body = json.dumps(geojson, sort_keys=True, indent=4, separators=(',', ': '))
            resp.set_header('Content-type','application/json')
        else:
            resp.status = falcon.HTTP_400
            resp.set_header('Content-type','text/html')
            resp.body = "README dispo sur <a href='https://github.com/geonym/geonymapi'>https://github.com/geonym/geonymapi</a>"

    def on_get(self, req, resp, query=None):
        self.getGeonym(req, resp, query);


# Falcon.API instances are callable WSGI apps.
app = falcon.API(middleware=[HeaderMiddleware()])

# Resources are represented by long-lived class instances
g = GeonymResource()

# things will handle all requests to the matching URL path
app.add_route('/{query}', g)
