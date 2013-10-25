from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'repos.views.home', name='home'),
    url(r'^repos/(?P<repo_id>\d+)$', 'repos.views.repo', name='repo'),

    url(r'^api/', include('api.urls')),

)
