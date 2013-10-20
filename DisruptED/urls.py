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
    url(r'^extra/', include('ExtraPages.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^Profile/', include('Profile.urls')),
    (r'^Utils/', include('Utils.urls')),
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^classes/', include('Classes.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^lessonPlanner/', include('LessonPlanner.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^courses/$', 'Courses.views.showCourses', name="myCourses"),
    url(r'^requestEditCourse/$', 'Courses.views.EditCourseRequest', name="requestEditCourse"),
    url(r'^editCourse/$', 'Courses.views.editCourse', name="editCourse"),
    url(r'^deleteCourse/$', 'Courses.views.deleteCourse', name="deleteCourse"),
    url(r'^requestEditUnit/$', 'Units.views.EditUnitRequest', name="requestEditUnit"),
    url(r'^editUnit/$', 'Units.views.editUnit', name="editUnit"),
    url(r'^deleteUnit/$', 'Units.views.deleteUnit', name="deleteUnit"),
    url(r'^requestEditLesson/$', 'Lessons.views.EditLessonRequest', name="requestEditLesson"),
    url(r'^editLesson/$', 'Lessons.views.editLesson', name="editLesson"),
    url(r'^deleteLesson/$', 'Lessons.views.deleteLesson', name="deleteLesson"),
    url(r'^deleteSection/$', 'LessonPlanner.views.deleteSection', name="deleteSection"),
    url(r'^deleteContent/$', 'LessonPlanner.views.deleteContent', name="deleteContent"),
    url(r'^addCourse/$', 'Courses.views.addCourse'),
    url(r'^recommendCourses/$', 'Courses.views.recommendCourses'),
    url(r'^cloneCourse/$', 'Courses.views.cloneCourse', name="cloneCourse"),
    url(r'^addSection/$', 'LessonPlanner.views.addSection'),
    url(r'^addUnit/$', 'Units.views.addUnit'),
    url(r'^addLesson/$', 'Lessons.views.addLesson'),
    url(r'^addContent/$', 'LessonPlanner.views.addContent'),
    url(r'^changeSectionPlacement/$', 'LessonPlanner.views.changeSectionPlacement'),
    url(r'^changeContentPlacement/$', 'LessonPlanner.views.changeContentPlacement',name='changeContentPlacement'),
    url(r'^activitySearch/$', 'LessonPlanner.views.search_activity_ajax_view',name='activitySearch'),
    url(r'^viewActivity/$', 'LessonPlanner.views.activity_ajax_view'),
    url(r'^addActivity/$', 'LessonPlanner.views.activity_add'),
    url(r'^$', 'LessonPlanner.views.landing'),

    url(r'^createCourseFromStandard/$', 'Courses.views.createCourseFromStandard', name='createCourseFromStandard'),

    url(r'team/$', 'LessonPlanner.views.team'),
    (r'^login/$', 'accounts.views.login_user'),
    (r'^profile/$', 'Profile.views.view_profile'),
    (r'^logout/$', 'accounts.views.logout_user'),
    (r'^lessons/$', 'Lessons.views.showLessons'),
    (r'^lessonPlanner/$', 'LessonPlanner.views.showLessonPlanner'),
    url(r'^lessonPresentation/$', 'LessonPlanner.views.lesson_presentation', name="lessonPresentation"),
    url(r'^addUnitStandards/$', 'Units.views.addUnitStandards', name="addUnitStandards"),
    url(r'^addLessonStandards/$', 'Lessons.views.addLessonStandards', name="addLessonStandards"),
    url(r'^addLessonObjectives/$', 'Lessons.views.addLessonObjectives', name="addLessonObjectives"),
    url(r'^getGroupStandards/$', 'Courses.views.getStandardsFromGroup', name="getStandardsFromGroup"),
    (r'^requestLessonStandards/$', 'Lessons.views.requestAddableLessonStandards'),
    (r'^requestUnitStandards/$', 'Units.views.requestAddableUnitStandards'),
    url(r'^getLessonStandards/$', 'Lessons.views.getLessonStandards', name='getLessonStandards'),
    url(r'^standard/$', 'Standards.views.getStandard', name='getStandard'),
    url(r'^createLessonObjectives/$', 'Lessons.views.createLessonObjectives', name='createLessonObjectives'),
    (r'^addStandardAnalysis/$', 'LessonPlanner.views.addStandardAnalysis'),
    url(r'^units/$', 'Units.views.showUnits',name="units"),
    url(r'^unitView/$', 'Units.views.publicUnitView', name='publicUnitView'),
    url(r'^courseView/$', 'Courses.views.publicCourseView', name='publicCourseView'),
    url(r'^standardsSearch/$', 'Standards.views.standardsSearch', name='standardsSearch'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT,
       }),	
    (r'^rateAnalysis/$', 'LessonPlanner.views.rateAnalysis'),
)



