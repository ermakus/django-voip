from django.conf.urls.defaults import *

urlpatterns = patterns('room.views',
    url(r'^$', 'index', name='index'),
    url(r'^context$', 'context', name='context'),
    url(r'^my$', 'rooms_view', name='rooms_view'),
    url(r'^room/(?P<id>\w+)$', 'room_view',name="room_view"),
    url(r'^chat/(?P<id>\w+)$', 'chat_view',name="chat_view"),
    url(r'^call$', 'call_view',name="call_view"),
    url(r'^snippet/(?P<id>\w+):(?P<action>\w+)$', 'snippet',name="snippet"),
)
