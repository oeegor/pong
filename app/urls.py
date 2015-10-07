# coding: utf-8

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = staticfiles_urlpatterns()

urlpatterns += [
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'core.views.home', name='home'),
    url(r'^tournament/([0-9]+)/?$', 'core.views.tournament', name='app-tournament'),
    url(r'^tournament/([0-9]+)/join/?$', 'core.views.join_tournament', name='app-join-tournament'),
    url(r'^match/([0-9]+)/?$', 'core.views.match', name='app-match'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^login/?$', 'account.views.login', name='login'),
    url(r'^logout/?$', 'account.views.logout', name='logout'),
]
