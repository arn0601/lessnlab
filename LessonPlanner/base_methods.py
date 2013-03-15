from django.template import RequestContext
from LessonPlanner.models import Lesson
from LessonPlanner.models import Course,Unit,Tag
from LessonPlanner.forms import AddCourse,AddUnitForm,AddLessonForm
from LessonPlanner.forms import EditCourse,EditUnit,EditLesson
from LessonPlanner.forms import DeleteCourse,DeleteUnit,DeleteLesson
from Standards.models import Standard
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import UserProfile
import simplejson

def getStandardsList(course, user):
	print course.department, user.user_school_state
	slist = Standard.objects.filter(department=course.department, owner_type=user.user_school_state)
	s_choices = [(s.id, s.description) for s in slist]
	return s_choices	

def createBaseDict(request):
	(courseAddForm, unitAddForm,lessonAddForm) = returnBlankForms()
	user = UserProfile.objects.get(user=request.user)

	user_courses =  Course.objects.filter(owner=user)
	
	course_id = request.GET.get('course_id')
	if ( not course_id == None ):
		course = Course.objects.get(id=course_id)
        	user_units =  Unit.objects.filter(course=course)
		unitAddForm.fields['course_id'].initial = course_id
	
		standards_list = getStandardsList(course, user)
	else:
		course = None
		user_units = None
		standards_list = []
	
	unit_id = request.GET.get('unitID')
	if ( not unit_id == None ):
		unit = Unit.objects.get(id=unit_id)
		course = unit.course
		user_lessons = Lesson.objects.filter(unit=unit)
		lessonAddForm.fields['unitID'].initial = unit_id
	else:
		unit = None
		user_lessons = None

	lessonID = request.GET.get('lessonID')
	if ( not lessonID == None ):
		lesson = Lesson.objects.get(id=lessonID)
	else:
		lesson = None	

	uname = request.user.username

	unitAddForm.fields['standards'].choices = standards_list
	
	#return (stuff for function, stuff to render)
	return {'course': course, 'unit': unit, 'lesson': lesson, 'userCourses': user_courses, 'userUnits':user_units, 'userLessons': user_lessons, 'username': uname, 'fullname': uname, 'courseAddForm':courseAddForm, 'unitAddForm':unitAddForm, 'lessonAddForm':lessonAddForm, 'standardlist':standards_list}

def returnBlankForms():
	addCourseForm = AddCourse()
	addUnitForm = AddUnitForm()
	addLessonForm = AddLessonForm()
	return (addCourseForm, addUnitForm , addLessonForm)
