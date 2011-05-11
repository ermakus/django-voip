from django.db import models
from django.contrib.auth.models import User

from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
from asterisk.models import Channel
import datetime

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class Profile(BaseProfile):
    provider  = models.CharField(max_length = 200)
    uid  = models.CharField(max_length=255, unique=True,db_index=True)
    token = models.CharField(max_length=200,blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(default=datetime.date.today(), blank=True)
    site = models.URLField(blank=True)
    about = models.TextField(blank=True)


    def channel(self):
        return Channel.objects.get(user=self.user)

    def display_name(self):
        name = (' '.join([ self.first_name, self.last_name ])).strip()
        if not name: name = self.user.username
        return name

    def __unicode__(self):
        return self.display_name()


import categories
categories.register_m2m(Profile, 'categories', )
