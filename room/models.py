from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import permalink
import categories

RELATION_ROLES = (
    ('BROKER','Broker'),
    ('CUSTOMER','Customer')
)

class Room( models.Model ):
    moderator = models.ForeignKey( User )
    title     = models.CharField(max_length=256)
    more      = models.TextField()
    rating    = models.IntegerField()

    def __unicode__(self):
        return "%s (Moderator: %s)" % ( self.title, self.moderator.username )

    @permalink
    def get_absolute_url(self):
        return ('room_view', [str(self.id)])

    class Meta:
        verbose_name_plural = 'Rooms'
        ordering = ('rating',)
        get_latest_by = 'rating'

class Snippet( models.Model ):
    author = models.ForeignKey( User, related_name='author_id' )
    target = models.ForeignKey( User, related_name='target_id' )
    room   = models.ForeignKey( Room )
    content_type = models.CharField(max_length=64)
    url = models.CharField(max_length=2048)
    message = models.TextField()
    class Meta:
        verbose_name_plural = 'Snippets'

    def __unicode__(self):
        return "%s: %s" % ( self.content_type, self.message )

class Action( models.Model ):
    snippet = models.ForeignKey( Snippet )
    issuer  = models.ForeignKey( User )
    command = models.CharField(max_length=64)
    params  = models.TextField()
    class Meta:
        verbose_name_plural = 'Actions'

    def __unicode__(self):
        return "%s: %s (%s)" % ( self.command, self.params  )

class Invite( models.Model ):
    from_user = models.ForeignKey( User, related_name='from_user_id' )
    to_user   = models.ForeignKey( User, related_name='to_user_id' )
    room      = models.ForeignKey( Room )
    status    = models.CharField(max_length=64)
    comment   = models.TextField()
    class Meta:
        verbose_name_plural = 'Actions'

    def __unicode__(self):
        return "%s: %s (%s)" % ( self.command, self.params  )

categories.register_m2m(Room, 'cats', )
