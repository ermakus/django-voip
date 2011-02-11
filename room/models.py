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

class Meeting( models.Model ):
    room      = models.ForeignKey( Room )
    comment   = models.TextField( blank=True )
    date_time = models.DateTimeField()
    duration  = models.IntegerField()
    participants = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = 'Meetings'

    def __unicode__(self):
        return "%s" % ( self.room, self.event.place, self.count, self.price )

class Stream( models.Model ):
    uid = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    user = models.ForeignKey( User )

categories.register_m2m(Room, 'cats', )
