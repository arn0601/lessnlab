from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
import accounts.views
from registration.views import activate
from registration.views import register

urlpatterns = patterns('',
   url(r'^setData/$', 'Utils.views.setData', name="setData"),
   url(r'^getPrivateUrl/$', 'Utils.views.getPrivateUrl', name="getPrivateUrl"),
   url(r'^uploadData/$', 'Utils.views.uploadData', name="uploadData"),
)
