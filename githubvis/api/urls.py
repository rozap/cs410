from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'repos$', 'repos', name='repos'),
    url(r'repos/(?P<repo_id>\d+)$', 'repo', name='repo'),
    url(r'repos/(?P<repo_id>\d+)/interactions$', 'interactions', name='interactions'),
    url(r'repos/(?P<repo_id>\d+)/common_file_changes$', 'common_file_changes', name='common_file_changes'),

)
