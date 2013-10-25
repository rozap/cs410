# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Repo, Actor, Commit, Function
from django.http import Http404

def home(request):
	repos = Repo.objects.all()
	return render_to_response('home.html', {
			'repos' : repos
		}, RequestContext(request))


def repo(request, repo_id):

	try:
		repo = Repo.objects.get(id = repo_id)
	except Repo.DoesNotExist:
		raise Http404
	return render_to_response('vis.html', {
		'repo' : repo
			}, RequestContext(request))