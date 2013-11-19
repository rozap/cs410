from celery import task
from util import analyze_repo as seq_analyze_repo, files_in_common
from location import geocode_locations

@task()
def analyze_repo(url):
	print "Starting task!"
	r = seq_analyze_repo(url)
	geocode_locations()
	print "Finding common file changes"
	files_in_common(r)

