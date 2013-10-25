from git import Repo
from django.conf import settings
from models import Repo as RepoModel, Actor, Commit, Function
import ast
import re
from threading import Thread
from django.db import transaction
from github3 import login


def repo_from_url(url):
    splits = url.split('/')
    username = splits[-2]
    repo = splits[-1]
    return (username, repo)

def repo_path(username, repo_name):
    return settings.REPO_ROOT + '%s/%s' % (username, repo_name)



def get_remote_repo(url):
    username, repo = repo_from_url(url)
    Repo.clone_from(url, repo_path(username, repo))


def examine_repo(url):
    get_remote_repo(url)
    username, repo_name = repo_from_url(url)
    a = Analyzer(username, repo_name)
    a.walk_commits()


# def dj():
#     analyzer = Analyzer('django', 'django.git')
#     return analyzer.walk_commits()




class Analyzer(object):

    def __init__(self, username, repo_name):
        self.repo = Repo(repo_path(username, repo_name))

        try:
            self.repo_model = RepoModel.objects.get(username = username, name = repo_name)
        except RepoModel.DoesNotExist:
            self.repo_model = RepoModel(username = username, name = repo_name)
            self.repo_model.save()

        self.cached_data = {}



    def is_python_file(self, diff):
        if diff.a_blob and re.search('.*\.py$', diff.a_blob.name):
            return True
        return False


    def get_classes(self, entities):
        return [e for e in entities if type(e) == ast.ClassDef]


    def get_functions(self, entities):
        return [e for e in entities if type(e) == ast.FunctionDef]


    def get_all_funcs_from_body(self, body):
        funcs = self.get_functions(body)
        classes = self.get_classes(body)
        for c in classes:
            funcs = funcs + self.get_all_funcs_from_body(c.body)
        return funcs





    def read_diffs(self, diffs):
        new_funcs = []
        for diff in diffs:
            if diff.a_blob and diff.b_blob:
                a_blob_text = diff.a_blob.data_stream.read()
                b_blob_text = diff.b_blob.data_stream.read()

                try:
                    a_syntax_tree = ast.parse(a_blob_text)
                    b_syntax_tree = ast.parse(b_blob_text)
                except (ValueError, SyntaxError) as e:
                    #Someone has committed some crap that's not valid python, 
                    #carry on...
                    continue                

                a_entities = a_syntax_tree.body
                a_funcs = self.get_all_funcs_from_body(a_entities)
                
                b_entities = b_syntax_tree.body
                b_funcs = self.get_all_funcs_from_body(b_entities)

                a_func_names = [f.name for f in a_funcs]
                b_func_names = [f.name for f in b_funcs]

                new_funcs = new_funcs + list(set(a_func_names) - set(b_func_names))
                print new_funcs
        return new_funcs


    def store(self, commit, new_funcs):
        name = commit.author.name
        date = commit.committed_date

        self.cached_data[commit.hexsha] = {
            'name' : name,
            'date' : date,
            'funcs' : new_funcs
        }

        if(len(self.cached_data.keys()) > 20):
            with transaction.commit_on_success():
                self.do_save()


    def do_save(self):
        for hexsha in self.cached_data:

            val = self.cached_data[hexsha]

            try:
                actor = Actor.objects.get(full_name = val['name'])
            except Actor.DoesNotExist:
                actor = Actor(full_name = val['name'])
                actor.save()
                #Create the actor

            try:
                commit = Commit.objects.get(hexsha = hexsha)
            except Commit.DoesNotExist:
                commit = Commit(hexsha = hexsha, repo = self.repo_model, actor = actor)
                commit.save()

            for fun in val['funcs']:
                fmodel = Function(name = fun, commit = commit)
                fmodel.save()

        self.cached_data.clear()

    def walk_commits(self):
        for commit in self.repo.iter_commits():
            #Create a list of diffs based on the parent (aka commit before this commit)
            try:
                diffs = commit.diff(commit.parents[0])
                diffs = [d for d in diffs if self.is_python_file(d)]
                new_funcs = self.read_diffs(diffs)
                if new_funcs:
                    self.store(commit, new_funcs)
            except LookupError:
                #This seems to be a bug in PyGit maybe?
                #seems to throw this sometimes, not much we can do here...
                continue

