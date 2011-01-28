from django.conf.urls.defaults import *

urlpatterns = patterns('content.views',
    url(r'^$', 'index', name='index'),
    url(r'^context$', 'context', name='context'),
    url(r'^upload$', 'upload', name='upload'),
    url(r'^view/(?P<content_id>\w+)$', 'content',name="content"),
    url(r'^buy/(?P<content_id>\w+)$', 'buy', name="buy"),
)
