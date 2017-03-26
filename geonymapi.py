#!/usr/bin/python3

import falcon
import json
import requests

import geonym

class HeaderMiddleware:

    def process_response(self, req, resp, resource):
        resp.set_header('X-Powered-By', 'GeonymAPI')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        resp.set_header('Access-Control-Allow-Methods','GET')

class GeonymResource(object):
    def getGeonym(self, req, resp, query=None):
        resp.status = falcon.HTTP_200
        geo = None
        if 'lat' in req.params and 'lon' in req.params:
            query = geonym.ll2geonym(float(req.params['lat']), float(req.params['lon']))
        elif 'geonym' in req.params:
            query = req.params['geonym']
        elif 'adresse' in req.params:
            r = requests.get('http://api-adresse.data.gouv.fr/search', params={"q":req.params['adresse'], "autocomplete":0, "limit":1})
            geo = json.loads(r.text)
            geo['source']='http://api-adresse.data.gouv.fr/search'
            query = geonym.ll2geonym(geo['features'][0]['geometry']['coordinates'][1], geo['features'][0]['geometry']['coordinates'][0])

        if query is not None and geonym.checkGeonym(query):
            data = geonym.geonym2ll(query)
            geojson = {"type":"Feature",
                "properties":data,
                "params":geonym.getParams(),
                "geocode":geo,
                "geometry":{"type":"Point","coordinates":[data['lon'],data['lat']]}}
            resp.body = json.dumps(geojson, sort_keys=True)
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
app.add_route('/geonym', g)
app.add_route('/{query}', g)
