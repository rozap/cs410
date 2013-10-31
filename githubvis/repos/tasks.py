from celery import task
from util import analyze_repo as seq_analyze_repo
from location import geocode_locations

@task()
def analyze_repo(url):
	print "Starting task!"
	seq_analyze_repo(url)
	geocode_locations()


