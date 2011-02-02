from django.db import models
from django.contrib.auth.models import User

from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
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
