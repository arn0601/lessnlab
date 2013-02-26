from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from registration.views import activate
from registration.views import register
from accounts.forms import UserProfileRegistrationForm

urlpatterns = patterns('',
	url(r'^register/$',register,{'backend':'registration.backends.simple.SimpleBackend', 'form_class' : UserProfileRegistrationForm, 'success_url': 'LessonPlanner.views.showTemplateLesson' },name='registration.views.register'),

)
