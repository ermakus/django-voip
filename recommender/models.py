from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from recommender.managers import RecommenderManager

# Main recommender class. Add here whatever you need to be parametrizable: min values, weigths...
class Recommender(models.Model):

    objects = RecommenderManager()

#Test class only for testing. Delete for real projects.
class TestItem(models.Model):

    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return '%s' % self.name
