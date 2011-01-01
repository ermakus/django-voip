from django.db import models
from django.contrib.auth.models import User
# Create your models here.

MOVIE_TYPE = (
    ('movie', 'movie'),
    ('series', 'series'),
    ('episode', 'episode'),
)

class Movie(models.Model):
    typeid = models.CharField( choices = MOVIE_TYPE, max_length=32 )
    title = models.CharField( max_length=100 )
    year = models.IntegerField()
    owner = models.ForeignKey(User)
    publish = models.DateTimeField()
    unpublish = models.DateTimeField()
    description = models.TextField()
    image = models.URLField()
    trailer = models.URLField()
    trailer_image = models.URLField()
    price = models.FloatField( default=0.0 )
    rating = models.FloatField( default=0.0 )
    views = models.IntegerField( default=0 )

    def add_relation( self, typeid, user, more ):
        exists = MovieRelation.objects.filter( movie=self,typeid=typeid, user=user )
        rel = None
        if exists.count() > 0:
           rel = exists[0]
        else:
           rel = MovieRelation( typeid=typeid, user=user, movie=self )
        rel.more = more
        rel.save()
        return rel

    def del_relation( self, typeid, user ):
        exists = MovieRelation.objects.filter( movie=self, typeid=typeid, user=user )
        for rel in exists:
            rel.delete()
        
    def __unicode__(self):
        return self.title

    # If using the get_absolute_url method, put the following line at the top of this file:
    from django.db.models import permalink
    
    @permalink
    def get_absolute_url(self):
        return ('movie_view', [str(self.id)])

import categories

categories.register_m2m( Movie )

RELATION_TYPE = (
   ('bag','bag'),
   ('buy','buy'),
   ('comment','comment'),
)

class MovieRelation(models.Model):
    typeid = models.CharField( choices = RELATION_TYPE, max_length=32 )
    movie = models.ForeignKey( Movie )
    user = models.ForeignKey( User )
    more = models.TextField()

    def __unicode__(self):
        return "[" + self.typeid + "] " + self.user.username + " : " + self.movie.title

ATTR_TYPE = (
   ('Genre','Genre'),
   ('Director','Director'),
   ('Cast','Cast'),
   ('Studio','Studio'),
)

class MovieAttribute(models.Model):
    typeid = models.CharField( choices = ATTR_TYPE, max_length=32 )
    movie = models.ForeignKey( Movie )
    title = models.CharField( max_length=100 )

class FriendRelation(models.Model):
    user = models.ForeignKey( User, related_name="user" )
    friend = models.ForeignKey( User, related_name="friend" )
