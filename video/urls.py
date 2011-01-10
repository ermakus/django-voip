from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'video.views.index'),
    url(r'^common.js$', 'video.views.script'),
    url(r'^context$', 'video.views.context'),
    url(r'^feed/(?P<type>\w+)/(?P<page>\w+)$', 'video.views.feed'),
    url(r'^upload$', 'video.views.upload'),
    url(r'^movie/(?P<movie_id>\w+)$', 'video.views.movie'),
    url(r'^gallery/(?P<type>\w+)/(?P<page>\w+)$', 'video.views.gallery'),
    url(r'^buy/(?P<movie_id>\w+)$', 'video.views.buy'),
    url(r'^bag_view/(?P<page>\w+)$', 'video.views.bag_view'),
    url(r'^bag/(?P<movie_id>\w+)$', 'video.views.bag'),
    url(r'^bag_drop/(?P<movie_id>\w+)$', 'video.views.bag_drop'),
)
