import os
import sys
# Environment setup for your Django project files:
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from room.models import Room

try:
    import json
except ImportError:
    import simplejson as json

def handle_send(msg, username, channel_id):
    print "=handle_send= ", msg, username, channel_id
    msg = json.loads(msg)
    msg.update({"from":username})
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
