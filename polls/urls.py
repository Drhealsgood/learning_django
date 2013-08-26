'''
Created on 27/08/2013

@author: luke
'''
from django.conf.urls import patterns, url

from polls import views

# map the view to url
urlpatterns = patterns('',
            url(r'^$',views.index, name='index'),
            url(r'^(?P<poll_id>\d+)/$',views.detail,name='detail'),
            url(r'^(?P<poll_id>\d+)/results/$',views.results,name="results"),
            url(r'^(?P<poll_id>\d+)/vote/$',views.vote,name='vote'),
            
            )
