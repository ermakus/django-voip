from django.conf.urls.defaults import *

urlpatterns = patterns('room.views',
    url(r'^context$', 'context', name='context'),
    url(r'^profiles/(?P<category>\w+)$', 'profiles',name="profiles"),
)
