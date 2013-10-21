
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
import Classes.views

urlpatterns = patterns('',
    (r'^classes/$', 'Classes.views.showClasses'),
    (r'^addClass/$', 'Classes.views.addClass'),
    (r'^requestAddClass/$', 'Classes.views.requestAddClassForm'),
    (r'^class/$', 'Classes.views.showClass'),
    (r'^studentAddClass/$', 'Classes.views.studentAddClass'),
    (r'^studentRequestClass/$', 'Classes.views.studentRequestClass'),
    (r'^editClassStudents/$', 'Classes.views.editClassStudents'),
    (r'^manageStudents/$', 'Classes.views.manageStudents'),  
)
