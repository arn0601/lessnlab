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
    url(r'^courses/$', 'LessonPlanner.views.courses', name="course"),
    url(r'^editCourse/$', 'LessonPlanner.views.editCourse', name="editCourse"),
    url(r'^deleteCourse/$', 'LessonPlanner.views.deleteCourse', name="deleteCourse"),
    url(r'^editUnit/$', 'LessonPlanner.views.editUnit', name="editUnit"),
    url(r'^deleteUnit/$', 'LessonPlanner.views.deleteUnit', name="deleteUnit"),
    url(r'^editLesson/$', 'LessonPlanner.views.editLesson', name="editLesson"),
    url(r'^deleteLesson/$', 'LessonPlanner.views.deleteLesson', name="deleteLesson"),
    url(r'^deleteSection/$', 'LessonPlanner.views.deleteSection', name="deleteSection"),
    url(r'^deleteContent/$', 'LessonPlanner.views.deleteContent', name="deleteContent"),
    url(r'^addCourse/$', 'LessonPlanner.views.addCourse'),
    url(r'^addSection/$', 'LessonPlanner.views.addSection'),
    url(r'^addUnit/$', 'LessonPlanner.views.addUnit'),
    url(r'^addLesson/$', 'LessonPlanner.views.addLesson'),
    url(r'^addContent/$', 'LessonPlanner.views.addContent'),
    url(r'^$', 'LessonPlanner.views.courses'),
    (r'^login/$', 'accounts.views.login_user'),
    (r'^lessons/$', 'LessonPlanner.views.showLesson'),
    (r'^lessonPlanner/$', 'LessonPlanner.views.showLessonPlanner'),
    url(r'^addUnitStandards/$', 'LessonPlanner.views.addUnitStandards', name="addUnitStandards"),
    url(r'^addLessonStandards/$', 'LessonPlanner.views.addLessonStandards', name="addLessonStandards"),
    url(r'^addLessonObjectives/$', 'LessonPlanner.views.addLessonObjectives', name="addLessonObjectives"),
    url(r'^getGroupStandards/$', 'LessonPlanner.views.getStandardsFromGroup', name="getStandardsFromGroup"),
    (r'^requestLessonStandards/$', 'LessonPlanner.views.requestLessonStandards'),
    (r'^requestUnitStandards/$', 'LessonPlanner.views.requestUnitStandards'),
    (r'^requestLessonObjectives/$', 'LessonPlanner.views.requestLessonObjectives'),
    (r'^units/$', 'LessonPlanner.views.showUnits'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT,
       }),	
)



