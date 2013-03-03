# Create your views here.
from LessonPlanner.models import Lesson
from LessonPlanner.models import Course,Unit
from LessonPlanner.forms import AddCourse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import UserProfile
import simplejson

#show the units for a specific course
@csrf_exempt
def showUnits(request):
	courseID = request.GET.get('courseID')
	print courseID,"-Course"
	uname = request.user.username
        fullname = uname
        (courseAddForm) = returnBlankForms()
	user = UserProfile.objects.get(user=request.user)
        user_units =  Unit.objects.filter(owner=user)
	course = Course.objects.get(id=courseID)
	return render_to_response('unit.html', {'course': course, 'userUnits': user_units,'username':uname, 'fullname':uname, 'courseAddForm':courseAddForm})

#show the lessons of a unit

def lastPageToView(request):
	if request.session['last_page'] == 'courses':
		return course(request)
	return course(request)
	
def lastPageToRedirect(request):
	if request.session['last_page'] == 'courses':
		return '/courses/'
	return '/courses/'

@csrf_exempt
def courses(request):
	print "Course Page"	
	uname = request.user.username
        fullname = uname
	(addCourseForm) = returnBlankForms()
		
	user = UserProfile.objects.get(user=request.user) 
	user_courses =  Course.objects.filter(owner=user)
	print user_courses,"data"
	request.session['last_page'] = 'courses'
	return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'courseAddForm':addCourseForm})

@csrf_exempt
def addCourse(request):
	if request.method == 'POST':
		addCourseForm = AddCourse(data=request.POST)
		if saveCourse(addCourseForm, request.user):
			return HttpResponseRedirect(lastPageToRedirect(request))
	return lastPageToView(request)

def saveCourse(addCourseForm, request_user):
	if addCourseForm.is_valid():
		course = Course()
		course.owner = UserProfile.objects.get(user=request_user)
		course.subject = addCourseForm.data['name']
		course.department = addCourseForm.data['department']
		course.year = str(addCourseForm.data['year'])
		course.save()
		return True;
	return False;

def returnBlankForms():
	addCourseForm = AddCourse()
	return (addCourseForm)
