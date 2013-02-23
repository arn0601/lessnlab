from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from registration.views import activate
from registration.views import register
from accounts.forms import UserProfileRegistrationForm

urlpatterns = patterns('',
	url(r'^register/$',register,{'backend':'registration.backends.default.DefaultBackend', 'form_class' : UserProfileRegistrationForm},name='registration.views.register'),
#url(r'^/login/$', 'accounts.views.login_user'),

)
