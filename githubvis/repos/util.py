from git import Repo
from django.conf import settings
from models import Repo as RepoModel, Actor, Commit, Function, FunctionCall, FileChange, CommonFileChange
import ast
import re
from threading import Thread
from django.db import transaction
import subprocess
from django.conf import settings
import json
from django.db import IntegrityError
import os

def repo_from_url(url):
    splits = url.split('/')
    username = splits[-2]
    repo = splits[-1]
    return (username, repo)

def repo_path(username, repo_name):
    path = settings.REPO_ROOT + '%s/%s' % (username, repo_name)
    return path


def get_remote_repo(url):
    username, repo = repo_from_url(url)
    Repo.clone_from(url, repo_path(username, repo))


def func_line_to_path(line):
    sp = line.split(':')
    return sp[0], sp[1]


def files_in_common(r):
    already_common = {}
    def mark(a1, a2):
        already_common['%s_%s' % (a1.id, a2.id)] = True

    def common_exists(a1, a2):
        return already_common.get('%s_%s' %(a1.id, a2.id), False)

    changes = FileChange.objects.select_related('actor')\
                .filter(commit__repo = r)\
            .exclude(actor__lat = 0)\
            .exclude(actor__lng = 0)
    
    with transaction.commit_on_success():
        for c in changes:
            #Get the changes that were not made by this actor, and have a location associated
            common_changes = FileChange.objects.select_related('actor')\
                                .exclude(actor = c.actor)\
                                .exclude(actor__lat = 0)\
                                .exclude(actor__lng = 0)\
                                .filter(path = c.path)
            for cc in common_changes:
                if not common_exists(c.actor, cc.actor):
                    print "%s changed by %s and %s" % (cc.path[-10:], c.actor.full_name, cc.actor.full_name)
                    CommonFileChange(change1 = c, change2 = cc).save()
                    mark(c.actor, cc.actor)


def test():
    return analyze_repo('https://github.com/kennethreitz/requests')

def test_changes():
    r = RepoModel.objects.get(id = 23)
    files_in_common(r)

def analyze_repo(url):
    get_remote_repo(url)
    username, repo_name = repo_from_url(url)

    a = Analyzer(username, repo_name)
    a.walk_commits()

    #Path to the code to analyze
    r_path = repo_path(username, repo_name)
    #Path to sonar
    sonar_path = '%s/libs/pysonar2' % settings.SITE_ROOT_DIR
    #Output directory
    out_path = '%s%s/%s' % (settings.SONAR_ROOT, username, repo_name)
    #Command to run
    command = 'java -jar %s/target/pysonar-2.0-SNAPSHOT.jar %s %s' % (sonar_path, r_path, out_path)
    proc = subprocess.Popen(command, shell = True)
    proc.wait()
    if not proc.returncode == 0:
        print "Failure!"
        return

    #Go open the file, and place it in the repos interaction table
    with open(out_path + '/output.json') as f:
        funcs = json.loads(f.read())
        with transaction.commit_on_success():

            for caller in funcs.keys():
                caller_path, caller_name = func_line_to_path(caller)
                try:
                    caller_model = Function.objects.get(path = caller_path, name = caller_name)

                    callees = funcs[caller]
                    for callee in callees:
                        callee_path, callee_name = func_line_to_path(callee)

                        try:
                            callee_model = Function.objects.get(path = callee_path, name = callee_name)
                            FunctionCall(caller = caller_model, callee = callee_model).save()
                        except Function.DoesNotExist:
                            print "No: %s %s" % (callee_path, callee_name)


                except Function.DoesNotExist:
                    print "NO| %s %s" % (caller_path, caller_name)
    return a.repo_model        


class Analyzer(object):

    def __init__(self, username, repo_name):
        self.repo = Repo(repo_path(username, repo_name))
        self.seen_files = {}
        try:
            print "Repo exists"
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
        for f in funcs:
            funcs = funcs + self.get_all_funcs_from_body(f.body)
        return funcs



    def read_diffs(self, diffs):
        new_funcs = []
        files_changed = []
        for diff in diffs:

            if diff.a_blob and diff.b_blob:
                a_blob_text = diff.a_blob.data_stream.read()
                b_blob_text = diff.b_blob.data_stream.read()

                try:
                    a_syntax_tree = ast.parse(a_blob_text)
                except (ValueError, SyntaxError, TypeError) as e:
                    #Someone has committed some crap that's not valid python, 
                    #carry on...
                    continue                

                a_entities = a_syntax_tree.body
                a_funcs = self.get_all_funcs_from_body(a_entities)
                a_func_names = [f.name for f in a_funcs]
                
                file_name = diff.a_blob.abspath + diff.a_blob.name
                files_changed.append(file_name)
                if not self.seen_files.get(file_name, False):
                    #This is a new file, so ALL functions contained within it are new
                    self.seen_files[file_name] = True
                    new_funcs = new_funcs + [(diff.a_blob.abspath, fname) for fname in a_func_names]

                    print "New file!" 
                    print new_funcs

                else:
                    #Not a new file, get what has changed, so get the next blob, parse it, and get the 
                    #functions from it. 

                    #Get the syntax_tree for the second blob
                    try:
                        b_syntax_tree = ast.parse(b_blob_text)
                    except (ValueError, SyntaxError, TypeError) as e:
                        #Someone has committed some crap that's not valid python, 
                        #carry on...
                        continue                


                    b_entities = b_syntax_tree.body
                    b_funcs = self.get_all_funcs_from_body(b_entities)
                    b_func_names = [f.name for f in b_funcs]

                    #xor the functions
                    new_in_this_diff = list(set(a_func_names) ^ set(b_func_names))
                    new_funcs = new_funcs + [(diff.a_blob.abspath, fname) for fname in new_in_this_diff]


        return new_funcs, files_changed


    def store(self, commit, new_funcs, files_changed):
        name = commit.author.name
        date = commit.committed_date

        self.cached_data[commit.hexsha] = {
            'name' : name,
            'date' : date,
            'funcs' : new_funcs, 
            'files_changed' : files_changed
        }

        if(len(self.cached_data.keys()) > 30):
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

            for path, fun in val['funcs']:
                if not Function.objects.filter(name = fun, path = path).exists():
                    fmodel = Function(name = fun, commit = commit, path = path)
                    fmodel.save()
                    print "Saved  `%s` : `%s`" % (path[-16:], fun)

            for file_name in val['files_changed']:
                FileChange(path = file_name, actor = actor, commit = commit).save()


        self.cached_data.clear()

    def walk_commits(self):
        
        #This uses a lot of memory, but...I don't see another way to go backwards
        #in git python
        commits = []
        for c in self.repo.iter_commits():
            commits.append(c)

        #pop the first commit off, so that all commits in the loop will have a parent
        commits.pop()
        
        while len(commits) > 0:
            commit = commits.pop()
            #Create a list of diffs based on the parent (aka commit before this commit)
            try:
                diffs = commit.diff(commit.parents[0])
                diffs = [d for d in diffs if self.is_python_file(d)]
                new_funcs, files_changed = self.read_diffs(diffs)
                self.store(commit, new_funcs, files_changed)
            except LookupError:
                #This seems to be a bug in PyGit maybe?
                #seems to throw this sometimes, not much we can do here...
                continue

