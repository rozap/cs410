# Create your views here.
import json
from django.http import HttpResponse, HttpResponseForbidden
from repos.models import Repo, Actor, Commit, Function, FunctionCall
import datetime
from repos.models import BaseModel
from django.db.models.query import QuerySet
from repos.tasks import analyze_repo
from repos.util import repo_from_url
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

def json_view(fn):
    def wrapped(*args, **kwargs):
        print "JSON VIEW"
        data, response_code, exclude_fields = fn(*args, **kwargs)
        if not isinstance(data, dict):
            data = [d.to_dict(exclude_fields) for d in data]
        return HttpResponse(json.dumps(data), status = response_code, mimetype = 'application/json')
    return wrapped


def cacheable(fn):
    def wrapped(*args, **kwargs):
        request = args[0]
        querystring = ''.join(['%s=%s' % (k, request.GET[k]) for k in request.GET.keys()])
        cache_key = 'api-%s-%s' % (request.path, querystring)
        response = cache.get(cache_key)
        if not response:
            print "Cache miss on %s" % request.path
            response = fn(*args, **kwargs)
            cache.set(cache_key, response, 100000000)
        return response
    return wrapped



@cacheable
@json_view
def repo(request, repo_id):
    try:
        repo = Repo.objects.get(id = repo_id)
        functions = Function.objects.select_related('commit', 'commit__actor')\
            .filter(commit__repo__id = repo_id)\
            .exclude(commit__actor__lat = 0)\
            .exclude(commit__actor__lng = 0)
        return functions, 200, ['commit.repo.id', 'commit.actor.loc', 'id',
                                'commit.hexsha', 'commit.repo', 'commit.id']
    except Repo.DoesNotExist:
        return {'message' : 'repo not found'}, 404, []

@csrf_exempt
@json_view
def repos(request):
    if request.method == 'GET':
        repos = Repo.objects.all()
        return repos, 200, []
    elif request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        try:
            username, repname = repo_from_url(url)
            if Repo.objects.filter(name = repname, username = username).count() > 0:
                return {
                    'message' : 'That repo already exists! Check it out to the left.'
                }, 400, []
        except IndexError:
            return {
            'message' : 'Bad url',
            }, 400, []

        analyze_repo.delay(url)
        return {
            'message' : 'The submission is being processed. It takes a while, so go grab lunch or something.'
        }, 200, []


@cacheable
@json_view
def interactions(request, repo_id):
    try:
        repo = Repo.objects.get(id = repo_id)
        calls = FunctionCall.objects.select_related('commit', 'commit__actor')\
                .filter(caller__commit__repo = repo)\
            .exclude(caller__commit__actor__lat = 0)\
            .exclude(callee__commit__actor__lat = 0)

        return calls, 200, ['caller.commit.repo', 'callee.commit.repo', 'id',
                             'caller.commit.hexsha', 'caller.commit.id', 'caller.commit.actor.id',
                            'callee.commit.hexsha', 'callee.commit.id', 'callee.commit.actor.id']
    except Repo.DoesNotExist:
        return {'message' : 'Invalid id'}, 404, []