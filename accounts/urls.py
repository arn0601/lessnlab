from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
import accounts.views
from registration.views import activate
from registration.views import register
from accounts.forms import *

urlpatterns = patterns('',
	url(r'^registerTeacher/$',accounts.views.registerTeacher,{'backend':'registration.backends.simple.SimpleBackend', 'form_class' : TeacherRegistrationForm, 'success_url': '/courses/', 'template_name': 'registration/registration_teacher.html' },name='accounts.views.registerTeacher'),

	url(r'^registerStudent/$',accounts.views.registerStudent,{'backend':'registration.backends.simple.SimpleBackend', 'form_class' : StudentRegistrationForm, 'success_url': '/classes/classes/', 'template_name': 'registration/registration_student.html' },name='accounts.views.registerStudent'),

    (r'^validateLogin/$', 'accounts.views.validateLogin'),
    (r'^validateRegisterTeacher/$', 'accounts.views.validateRegisterTeacher'),
    (r'^validateRegisterStudent/$', 'accounts.views.validateRegisterStudent'),
)
