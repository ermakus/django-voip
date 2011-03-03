import re
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel
import random

class Bunch(MPTTModel):
    parent = models.ForeignKey('self', 
        blank=True, 
        null=True, 
        related_name="children", 
        help_text="Parent", 
        verbose_name='Parent')
    uid = models.CharField(max_length=128)
    kind = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)

    def html( self, level=2 ):
        if level > 0:
            children = ''.join( child.html(level-1) for child in self.get_children())
            return "<li id='%s' class='%s'><p>%s</p><ul id='%s-children'>%s</ul></li>" % ( self.uid, self.kind, self.content, self.uid, children )
        else:
            return ""

    @classmethod
    def uidme( self, uid, content=None ):
        uid = ''.join([random.choice('0123456789') for i in xrange(8)])
        while True:
            try:
                Bunch.objects.get( uid = uid )
            except Bunch.DoesNotExist:
                return uid

    @classmethod
    def resolve( self, path ):

        if( path == "/"):
            return Bunch.objects.get( uid="root" )

        path_items = path.strip('/').split('/')

        if len(path_items) >= 2:
            bunch = Bunch.objects.filter(uid__iexact = path_items[-1],level = len(path_items)-1,parent__uid__iexact=path_items[-2])
        else:
            bunch = Bunch.objects.filter(uid__iexact = path_items[-1],level = len(path_items)-1)

        if len(bunch) != 1: raise Bunch.DoesNotExist()
        return bunch[0]
    
    def path(self):
        """Return a path"""
        ancestors = list(self.get_ancestors()) + [self,]
        return  '/' + '/'.join([force_unicode(i.uid) for i in ancestors])
        
    class MPTTMeta:
        verbose_name_plural = 'Bunches'
        unique_together = ('parent', 'uid')
        ordering = ('tree_id', 'lft')
        order_insertion_by = 'uid'

    def __unicode__(self):
        return ' > '.join([force_unicode(i.uid) for i in self.get_ancestors()]+[self.uid,])
