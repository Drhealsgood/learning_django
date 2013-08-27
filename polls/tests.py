"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import random

import datetime

from polls.models import Poll
        
#------------------------------------------------------------------------------ 
# Factories
#------------------------------------------------------------------------------ 
class Factory():
    
    def get_item(self):
        return False
    
class PollFactory(Factory):
    
    def get_item(self,questions,days):
        if len(questions)>0:
            for q,d in (questions,days):
                yield Poll.objects.create(question=questions,
                    pub_date=timezone.now() + datetime.timedelta(days=days))
                
#===============================================================================
# Poll tests
#===============================================================================
class PollViewTests(TestCase):
    _p_factory = PollFactory()
    
    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
        
    def test_index_view_with_a_past_poll(self):
        """
        Polls with a pub_date in the past should be displayed on the index page.
        """
        self._p_factory.get_item(questions=["Past poll."], days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
                                 )
        
    def test_index_view_with_a_future_poll(self):
        """
        Polls with a pub_date in the future should not be displayed on the index page
        """
        self._p_factory.get_item(questions=["Future poll."], days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
        
    def test_index_view_with_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls should
        be displayed
        """
        self._p_factory.get_item(questions=['Past poll.','Future poll.'], 
                                 days=[-30,30])
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], 
                                 ['<Poll: Past poll.>']
        )
    
    def test_index_view_with_mult_past_polls(self):
        y =  dict((["Past poll {0}".format(d) for d in range(-1,-15,-1)],[random.randint(-1,-30) for d in range(-1,-15,-1)]))
        self._p_factory.get_item()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_poll_list'],
                
                                 )
        
        
        
        
class PollMethodTests(TestCase):
    
    def test_was_published_recently(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future, or more than a day in the past
        """
        # any day not in range (0->1.01) shopuld be false
        days = [30,0.1,-1.1,-2,-5,-10]
        for d in days: 
            future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=d))
            self.assertFalse(future_poll.was_published_recently(),"Expected False for {0}".format(d))
        days = [-0.1,-0.5,-0.9,-1]
        for d in days:
            future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=d))
            self.assertTrue(future_poll.was_published_recently(),"Expected True for {0}".format(d))