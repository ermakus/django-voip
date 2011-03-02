import os
import sys
# Environment setup for your Django project files:
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from bunch.models import Bunch

try:
    import json
except ImportError:
    import simplejson as json

def handle_send(msg, username, channel_id):
    print "=handle_send= ", msg, username, channel_id
    msg = json.loads(msg)
    try:
        if 'path' in msg: bunch = Bunch.resolve( msg.path )
        if 'uid' in msg:  bunch = Bunch.objects.get( uid=msg['uid'] )
        raise Exception("No path nor uid in message")
    except Bunch.DoesNotExist:
        bunch = Bunch( uid=Bunch.uidme( msg["uid"], msg["content"] ), content=msg["content"], kind=msg["kind"] )

    msg["uid"] = bunch.uid

    try:
        parent = Bunch.resolve( msg["parent"] )
    except Bunch.DoesNotExist:
        raise Exception('Parent channel not found: %s' % channel_id )

    bunch.insert_at( parent )
    bunch.save()

    return msg

def handle_subscribe(msg, username, channel_id):
    print "=handle_subscribe= ", msg, username, channel_id
    return msg

def handle_unsubscribe(msg, username, channel_id):
    print "=handle_unsubscribe= ", msg, username, channel_id
    return msg

def handle_connect(msg, username, channel_id):
    print "=handle_connect= ", msg, username, channel_id
    return msg

def handle_disconnect(msg, username, channel_id):
    print "=handle_disconnect= ", msg, username, channel_id
    return msg


MESSAGE_HANDLERS = {
    "send":handle_send,
    "subscribe":handle_subscribe,
    "unsubscribe":handle_unsubscribe,
    "connect":handle_connect,
    "disconnect":handle_disconnect
}
