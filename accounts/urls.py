from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

import accounts.views
from registration.views import activate
from registration.views import register
from accounts.forms import *

urlpatterns = patterns('',
	url(r'^register/$',accounts.views.register,{'backend':'registration.backends.simple.SimpleBackend', 'form_class' : TeacherRegistrationForm, 'success_url': '/courses/' },name='accounts.views.register'),

)
