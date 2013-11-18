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

def json_view(fn):
    def wrapped(*args, **kwargs):
        data, response_code, exclude_fields = fn(*args, **kwargs)
        if not isinstance(data, dict):
            data = [d.to_dict(exclude_fields) for d in data]
        return HttpResponse(json.dumps(data), status = response_code, mimetype = 'application/json')
    return wrapped


@json_view
def repo(request, repo_id):
    try:
        repo = Repo.objects.get(id = repo_id)
        functions = Function.objects.select_related('commit', 'commit__actor')\
            .filter(commit__repo__id = repo_id)\
            .exclude(commit__actor__lat = 0)\
            .exclude(commit__actor__lng = 0)
        return functions, 200, ['commit.repo.id', 'commit.actor.loc', 'id']
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



@json_view
def interactions(request, repo_id):
    try:
        repo = Repo.objects.get(id = repo_id)
        calls = FunctionCall.objects.filter(caller__commit__repo = repo)\
            .exclude(caller__commit__actor__lat = 0)\
            .exclude(callee__commit__actor__lat = 0)

        return calls, 200, []
    except Repo.DoesNotExist:
        return {'message' : 'Invalid id'}, 404, []