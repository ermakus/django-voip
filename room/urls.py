from django.conf.urls.defaults import *

urlpatterns = patterns('room.views',
    url(r'^$', 'index', name='index'),
    url(r'^context$', 'context', name='context'),
    url(r'^my$', 'rooms_view', name='rooms_view'),
    url(r'^room/(?P<id>\w+)$', 'room_view',name="room_view"),
    url(r'^chat/(?P<id>\w+)$', 'chat_view',name="chat_view"),
    url(r'^call/(?P<id>\w+)$', 'call_view',name="call_view"),
    url(r'^meeting/(?P<id>\w+)$', 'meeting_view',name="meeting_view"),
    url(r'^stream/(?P<uid>\w+):(?P<action>\w+)$', 'stream',name="stream"),
)
