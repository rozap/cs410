from agithub import Github
from models import Actor
from django.conf import settings
import requests
import json
from threading import Thread

def test():
    l = Locator()
    return l.get_locations()

class Locator(object):

    def __init__(self):
        self.gh = Github(username = settings.GITHUB_USERNAME, password=settings.GITHUB_PASS)


    def get_locations(self):
        actors = list(Actor.objects.filter(loc = '').exclude(loc = 'unknown'))




        for a in actors:
            # stripped = unicode(a.full_name, errors = 'replace')
            stripped = a.full_name.encode('utf8')
            res = self.gh.search.users.get(q = stripped)
            if res[0] == 200:
                data = res[1]
                items = data['items']

                if data['total_count'] > 0:
                    best_result = items[0]
                    user_resp = requests.get(best_result['url'])
                    user_data = json.loads(user_resp.text)
                    print user_resp.text
                    if user_data.get('location', False):
                        a.loc = user_data['location']
                        a.save()
            print a