from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    user = models.ForeignKey( User )
    name = models.CharField(max_length=80, primary_key=True)
    nat = models.CharField(max_length=5, help_text="yes or no", default="yes")
    host = models.CharField(max_length=80, help_text="dynamic or domain name", default="dynamic")
    type = models.CharField(max_length=6, help_text="user,peer or friend", default="peer")
    ipaddr = models.CharField(max_length=50, blank=True)
    regseconds = models.CharField(max_length=50, blank=True)
    useragent = models.CharField(max_length=50, blank=True)
    lastms = models.CharField(max_length=50, blank=True)
    fullcontact = models.CharField(max_length=50, blank=True)
    accountcode = models.CharField(max_length=20, blank=True)
    amaflags = models.CharField(max_length=13, help_text="default, omit, billing, documentation", default="default")
    callgroup = models.CharField(max_length=5, blank=True)
    callerid = models.CharField(max_length=80)
    directmedia = models.CharField(max_length=5, default="yes")
    context = models.CharField(max_length=80, default="default")
    dtmfmode = models.CharField(max_length=6, default="info", help_text="info,inband,rfc2833")
    defaultip = models.CharField(max_length=15, blank=True)
    fromuser = models.CharField(max_length=80, blank=True)
    fromdomain = models.CharField(max_length=80, blank=True)
    language = models.CharField(max_length=2, blank=True)
    insecure = models.CharField(max_length=2, blank=True)
    mailbox = models.CharField(max_length=50, blank=True)
    secret = models.CharField(max_length=50, blank=True)
    md5secret = models.CharField(max_length=50, blank=True)
    deny = models.CharField(max_length=95, blank=True, help_text="192.168.1.1/255.255.255.255;0.0.0.0/0.0.0.0")
    permit = models.CharField(max_length=95, blank=True, help_text="192.168.1.0/255.255.255.;1.1.2.3/255.255.255.255")
    pickupgroup = models.CharField(max_length=10, blank=True)
    qualify = models.CharField(max_length=3, help_text="yes,no, number of ms", default="yes")
    disallow = models.CharField(max_length=80, help_text="all or codesc list alaw;ulaw;gsm etc",default="all")
    allow = models.CharField(max_length=80, help_text="set codesc list 'alaw;ulaw;gsmx'",default="speex")
    port = models.CharField(max_length=5, help_text="default blank or 5060", default="5060")
    defaultuser = models.CharField(max_length=80, blank=True)
    fromuser = models.CharField(max_length=80, blank=True)
    subscribecontext = models.CharField(max_length=80, blank=True)
    canreinvite = models.CharField(max_length=3, help_text="yes or no", default="no")


    def is_online(self):
		return self.fullcontact != ""

    class Meta:
        db_table = u"asterisk_channel"
