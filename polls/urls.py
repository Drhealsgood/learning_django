'''
Created on 27/08/2013

@author: luke
'''
from django.conf.urls import patterns, url

from polls import views

# map the view to url
urlpatterns = patterns('',
            url(r'^$',views.index, name='index')
            )
