# Create your views here.
import json
from django.http import HttpResponse, HttpResponseForbidden
from repos.models import Repo, Actor, Commit, Function
import datetime
from repos.models import BaseModel
from django.db.models.query import QuerySet


def json_view(fn):
    def wrapped(*args, **kwargs):
        data, response_code, exclude_fields = fn(*args, **kwargs)
        data = [d.to_dict(exclude_fields) for d in data]
        return HttpResponse(json.dumps(data), status = response_code, mimetype = 'application/json')
    return wrapped


@json_view
def repo(request, repo_id):
	functions = Function.objects.select_related('commit', 'commit__actor')\
		.filter(commit__repo__id = repo_id)\
		.exclude(commit__actor__lat = 0)\
		.exclude(commit__actor__lng = 0)
	return functions, 200, ['commit.repo.id', 'commit.actor.loc', 'id']