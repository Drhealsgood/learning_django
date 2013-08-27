"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone

import datetime

from polls.models import Poll

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
class PollMethodTests(TestCase):
    
    def test_was_published_recently(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future, or more than a day in the past
        """
        days = [30,0.1,-1.1,-2,-5,-10]
        for d in days: 
            future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=d))
            self.assertFalse(future_poll.was_published_recently(),"Expected False for {0}".format(d))
        days = [-0.1,-0.5,-0.9,-1]
        for d in days:
            future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=d))
            self.assertTrue(future_poll.was_published_recently(),"Expected True for {0}".format(d))