from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/', include('accounts.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^courses/$', 'LessonPlanner.views.courses'),
    url(r'^addCourse/$', 'LessonPlanner.views.addCourse'),
    (r'^login/$', 'accounts.views.login_user'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT,
       }),	
)



