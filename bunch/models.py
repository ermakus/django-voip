import re
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel

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

    def as_node( self ):
        return self.content

    def as_list( self ):
        html = '<ul class="%s">' % self.kind
        for i in self.get_ancestors():
             html += '<li class="%s">%s</lI>' % ( i.kind , i.as_node() )
        return html + "</ul>"

    @classmethod
    def resolve( self, path ):

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
