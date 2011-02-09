from django.conf.urls.defaults import *

urlpatterns = patterns('tickets.views',
    url(r'^$', 'index', name='index'),
    url(r'^context$', 'context', name='context'),
    url(r'^my$', 'my', name='ticket_my'),
    url(r'^ticket/(?P<id>\w+)$', 'ticket',name="ticket_view"),
    url(r'^event/(?P<id>\w+)$', 'event',name="ticket_event_view"),
    url(r'^manage/(?P<id>\w+)$', 'manage', name="ticket_manage"),
)
