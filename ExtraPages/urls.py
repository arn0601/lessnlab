from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
import Classes.views

urlpatterns = patterns('',
    (r'^ObjectivesPage/$', 'ExtraPages.views.ObjectivesPage'),
    (r'^standardsForObjectives/$', 'ExtraPages.views.StandardsSearch'),
    (r'^QuestionsPage/$', 'ExtraPages.views.createCFU'),
   
)

