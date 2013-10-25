from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'repos/(?P<repo_id>\d+)$', 'repo', name='repo'),
)
