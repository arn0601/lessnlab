# Create your views here.
from django.template import RequestContext
from LessonPlanner.models import Lesson
from LessonPlanner.models import Course
from LessonPlanner.forms import AddCourse
from LessonPlanner.forms import EditCourse
from LessonPlanner.forms import DeleteCourse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import UserProfile
import simplejson

@csrf_exempt
def showUnits(request):
	courseID = request.GET.get('courseID')
	uname = request.user.username
        fullname = uname
        form = AddCourse()
	user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
	return render_to_response('unit.html', {'userCourses': user_courses,'username':uname, 'fullname':uname, 'courseAddForm':form})

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
	courseID = request.GET.get('courseID')
	action = request.GET.get('action')
	if action == "Edit":
		return EditCourseRequest(request, courseID)
	elif action == "Delete":
                return DeleteCourseRequest(request, courseID)
	else:	
		uname = request.user.username
        	fullname = uname
		(addCourseForm) = returnBlankForms()
		user = UserProfile.objects.get(user=request.user) 
		user_courses =  Course.objects.filter(owner=user)
		request.session['last_page'] = 'courses'
		return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'courseAddForm':addCourseForm})

@csrf_exempt
def addCourse(request):
	if request.method == 'POST':
		addCourseForm = AddCourse(data=request.POST)
		if saveCourse(addCourseForm, request.user):
			return HttpResponseRedirect(lastPageToRedirect(request))
	return lastPageToView(request)

@csrf_exempt
def editCourse(request):
	if request.method == 'POST':
                addCourseForm = EditCourse(data=request.POST)
                if saveCourse(addCourseForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

@csrf_exempt
def deleteCourse(request):
        if request.method == 'POST':
                addCourseForm = DeleteCourse(data=request.POST)
                if deleteCourseData(addCourseForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)


def DeleteCourseRequest(request, courseID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        course = Course.objects.get(id=courseID)
        deleteCourseForm = DeleteCourse()
        deleteCourseForm.fields["courseID"].initial = course.id
        return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'deleteCourseForm':deleteCourseForm,'showDeleteCourse': 1}, context_instance=RequestContext(request))


def EditCourseRequest(request, courseID):
	uname = request.user.username
	user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
	course = Course.objects.get(id=courseID)
	editCourseForm = EditCourse()	
	editCourseForm.fields["courseID"].initial = course.id	
	editCourseForm.fields["name"].initial = course.subject
	editCourseForm.fields["department"].initial = course.department
	editCourseForm.fields["year"].initial = course.year
	return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'editCourseForm':editCourseForm,'showEditCourse': 1})



def saveCourse(addCourseForm, request_user):
	if addCourseForm.is_valid():
		course = Course()
		if 'courseID' in addCourseForm.data:
			course = Course.objects.get(id=addCourseForm.data['courseID'])
		course.owner = UserProfile.objects.get(user=request_user)
		course.subject = addCourseForm.data['name']
		course.department = addCourseForm.data['department']
		course.year = str(addCourseForm.data['year'])
		course.save()
		return True;
	return False;

def deleteCourseData(courseForm, request_user):
	if 'courseID' in courseForm.data:
       		course = Course.objects.get(id=courseForm.data['courseID']).delete()
                return True;
        return False;


def returnBlankForms():
	addCourseForm = AddCourse()
	return (addCourseForm)
