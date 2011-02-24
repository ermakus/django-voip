#coding:UTF-8

import datetime
import os

from django.test import TestCase
from django.core.urlresolvers import reverse

from schedule.models import Event, Rule, Occurrence, Calendar
from schedule.periods import Period, Month, Day
from schedule.utils import EventListManager

class TestRule(TestCase):
    """
    test some more sophisticated rule settings
    """

    def setUp(self):
        cal, created = Calendar.objects.get_or_create(name="MyCal")
        cal.save()

    def test_daily(self):
        kw = {'frequency':'DAILY'}
        exp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        self._test_rule(kw, exp)

    def test_daily_limit(self):
        kw = {'frequency':'DAILY', 'params':'count:5'}
        exp = [1, 2, 3, 4, 5]
        self._test_rule(kw, exp)

    def test_monday(self):
        kw = {'frequency':'WEEKLY', 'params':'byweekday:MO'}
        exp = [4, 11, 18, 25]
        self._test_rule(kw, exp)

    def test_monday_thursday(self):
        kw = {'frequency':'WEEKLY', 'params':'byweekday:MO,TH'}
        exp = [4, 7, 11, 14, 18, 21, 25, 28]
        self._test_rule(kw, exp)

    def test_every_other_day(self):
        kw = {'frequency':'DAILY', 'params':'interval:2'}
        exp = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
        self._test_rule(kw, exp)

    def test_every_other_monday(self):
        kw = {'frequency':'WEEKLY', 'params':'byweekday:MO;interval:2'}
        exp = [11, 25]
        self._test_rule(kw, exp)

    def test_first_thursday_of_month(self):
        kw = {'frequency':'MONTHLY', 'params':'byweekday:TH(1)'}
        exp = [7]
        self._test_rule(kw, exp)

    def _test_rule(self, kw, exp):
        print
        print "Rule", kw
        print exp
        print
        rule = Rule(**kw)
        ocs = self.make_occurrences(rule)
        self.assertEqual(ocs, exp)

    def make_occurrences(self, rule):
        cal = Calendar.objects.get(name="MyCal")
        recurring_data = {
                'title': 'Recent Event',
                'start': datetime.datetime(2010, 1, 1, 8, 0),
                'end': datetime.datetime(2010, 1, 1, 9, 0),
                'end_recurring_period' : datetime.datetime(2010, 2, 1, 0, 0),
                'rule': rule,
                'calendar': cal
               }
        recurring_event = Event(**recurring_data)
        occurrences = recurring_event.get_occurrences(start=datetime.datetime(2010, 1, 1, 0, 0),
                                    end=datetime.datetime(2010, 2, 1, 0, 0))
        return [o.start.day for o in occurrences]