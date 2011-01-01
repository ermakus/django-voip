#!/usr/bin/python
# -*- coding: utf8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings

from django.db import models
from video.models import Movie
import sys, datetime

from os.path import dirname, abspath

CURL="wget"
for movie in Movie.objects.all():
#    print "# Movie: %s" % movie.title
    print "# Trailer: %s" % movie.trailer
    print "# Cover: %s" % movie.trailer_image
    print "# Thumb: %s" % movie.image
#    if movie.trailer:
#        basename, ext = os.path.splitext( movie.trailer )
#        print "%s -o ./media/trailers/%s%s %s" % ( CURL, movie.pk, ext, movie.trailer )
    if movie.image:
        basename, ext = os.path.splitext( movie.image )
        print "%s -O ./media/thumbs/%s%s %s" % ( CURL, movie.pk, ext, movie.image )
    if movie.trailer_image:
        basename, ext = os.path.splitext( movie.trailer_image )
        print "%s -O ./media/covers/%s%s %s" % ( CURL, movie.pk, ext, movie.trailer_image )

