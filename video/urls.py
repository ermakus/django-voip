from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'video.views.index', name='index'),
    url(r'^common.js$', 'video.views.script'),
    url(r'^context$', 'video.views.context', name='context'),
    url(r'^upload$', 'video.views.upload', name='upload'),
    url(r'^content/(?P<content_id>\w+)$', 'video.views.content',name="content"),
    url(r'^buy/(?P<content_id>\w+)$', 'video.views.buy', name="buy"),
)
