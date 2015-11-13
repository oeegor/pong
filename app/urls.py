# coding: utf-8

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import account.views
import core.views
import rating.views


urlpatterns = staticfiles_urlpatterns()

urlpatterns += [
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', core.views.home, name='home'),

    url(r'^tournament/([0-9]+)/?$', core.views.tournament, name='app-tournament'),
    url(r'^tournament/([0-9]+)/join/?$', core.views.join_tournament, name='app-join-tournament'),

    url(r'^rating-list$', rating.views.rating_list, name='rating-list'),
    url(r'^rating-history/([0-9]+)$', rating.views.rating_history, name='rating-history'),
    url(r'^rating-match$', rating.views.rated_game_save, name='rating-match'),

    url(r'^group/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/add-result/?$', core.views.add_set_result, name='app-add-set-result'),
    url(r'^set-result/([0-9]+)/approve/?$', core.views.approve_set_result, name='app-approve-set-result'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    url(r'^login/?$', account.views.login, name='login'),
    url(r'^logout/?$', account.views.logout, name='logout'),
]
