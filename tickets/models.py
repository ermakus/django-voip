from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import permalink
import categories

RELATION_ROLES = (
    ('BROKER','Broker'),
    ('CUSTOMER','Customer')
)

class Event( models.Model ):
    title     = models.CharField(max_length=256)
    more      = models.TextField()
    date_time = models.DateTimeField()
    city      = models.CharField( max_length=64 )
    place     = models.CharField( max_length=64 )

    def __unicode__(self):
        return "%s (%s)" % ( self.title, self.date_time.strftime("%A, %d %B %Y") )

    @permalink
    def get_absolute_url(self):
        return ('event_view', [str(self.id)])

    def get_ticket_count(self):
        count = 0
        for t in Ticket.objects.filter(event=self):
            count += t.count
        return count

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ('-date_time',)
        get_latest_by = 'date_time'


class Ticket( models.Model ):
    event    = models.ForeignKey( Event )
    count    = models.IntegerField()
    price    = models.DecimalField( decimal_places=2, max_digits=10)
    comment  = models.TextField( blank=True )

    class Meta:
        verbose_name_plural = 'Tickets'

    def __unicode__(self):
        return "%s at %s (%s ticket(s) for $%s)" % ( self.event.title, self.event.place, self.count, self.price )


class Relation( models.Model ):
    user     = models.ForeignKey( User )
    ticket   = models.ForeignKey( Ticket )
    role     = models.CharField( max_length=64, choices=RELATION_ROLES )

    class Meta:
        verbose_name_plural = 'Relations'

    def __unicode__(self):
        return "%s (%s)" % ( self.user, self.role )

categories.register_m2m(Event, 'cats', )
