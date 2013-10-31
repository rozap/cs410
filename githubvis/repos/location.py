from agithub import Github
from models import Actor
from django.conf import settings
import requests
import json
from threading import Thread
import time

def geocode_locations():
    l = Locator()
    l.get_locations()
    l.geocode()

class Locator(object):

    GOOGLE = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'

    def __init__(self):
        self.gh = Github(username = settings.GITHUB_USERNAME, password=settings.GITHUB_PASS)


    def geocode(self):
        actors = list(Actor.objects.exclude(loc = '').exclude(loc = 'unknown').filter(lat = 0, lng = 0))

        for a in actors:
            print 'Geocoding %s' % a.full_name
            try:
                url = self.GOOGLE % a.loc
                resp = requests.get(url)
                geocode_data = json.loads(resp.text)
                
                results = geocode_data.get('results', False)
                loc = results[0]['geometry']['location']
                a.lat = loc['lat']
                a.lng = loc['lng']
            except:

                time.sleep(62)
                print geocode_data
            a.save()

    def get_locations(self):
        actors = list(Actor.objects.filter(loc = ''))

        for a in actors:
            a.loc = 'unknown'
            stripped = a.full_name.encode('utf8')
            print "Getting location of %s" % stripped
            res = self.gh.search.users.get(q = stripped)
            if res[0] == 200:
                data = res[1]
                items = data['items']

                if data['total_count'] > 0:
                    best_result = items[0]
                    user_resp = requests.get(best_result['url'])
                    user_data = json.loads(user_resp.text)
                    if user_data.get('location', False):
                        a.loc = user_data['location']
                a.save()
            else:
                print "Sleeping..."
                time.sleep(62)
            print a