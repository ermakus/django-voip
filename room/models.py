from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import permalink
import categories

class Invite( models.Model ):
    from_user = models.ForeignKey( User, related_name='from_user_id' )
    to_user   = models.ForeignKey( User, related_name='to_user_id' )
    status    = models.CharField(max_length=64)
    comment   = models.TextField()
    class Meta:
        verbose_name_plural = 'Actions'

    def __unicode__(self):
        return "%s: %s (%s)" % ( self.command, self.params  )

