# Create your views here.
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
import base_methods 

#show the units for a specific course
@csrf_exempt
def showUnits(request):
	base_dict = base_methods.createBaseDict(request)
        action = request.GET.get('action')
	if action == "Edit":
                return EditUnitRequest(request, base_dict['unit'].id)
        elif action == "Delete":
                return DeleteUnitRequest(request, base_dict['unit'].id)
	
	#return from base

	request.session['last_page'] = '/units/?course_id='+str(base_dict['course'].id)
	
	return render_to_response('unit.html', base_dict)

#show the lessons of a unit

def showLesson(request):
	base_dict = base_methods.createBaseDict(request)
        action = request.GET.get('action')
        if action == "Edit":
                return EditLessonRequest(request, base_dict['lesson'].id)
        elif action == "Delete":
                return DeleteLessonRequest(request, base_dict['lesson'].id)

	request.session['last_page'] = '/lessons/?unit_id='+str(base_dict['unit'].id)
	return render_to_response('lesson.html', base_dict)

def showLessonPlanner(request):
	base_dict = base_methods.createBaseDict(request)
	lesson_info = base_methods.getLessonSpecificInfo(base_dict['lesson'])
	return render_to_response('lessonPlanner.html')

def lastPageToView(request):
	if request.session['last_page'] == 'courses':
		return course(request)
	elif request.session['last_page'] == 'units':
                return unit(request)
	return courses(request)
	
def lastPageToRedirect(request):
	if request.session['last_page'] == 'courses':
		return '/courses/'
	elif 'units' in request.session['last_page']:
                return request.session['last_page']
	elif 'lessons' in request.session['last_page']:
                return request.session['last_page']
	return '/courses/'

@csrf_exempt
def courses(request):
	base_dict = base_methods.createBaseDict(request)

	action = request.GET.get('action')
	if action == "Edit":
		return EditCourseRequest(request, base_dict['course'].id)
	elif action == "Delete":
                return DeleteCourseRequest(request, base_dict['course'].id)
	
	request.session['last_page'] = 'courses'
	return render_to_response('course.html', base_dict)

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

@csrf_exempt
def addUnit(request):
	if request.method == 'POST':
                addUnitForm = AddUnitForm(data=request.POST)
                if saveUnit(addUnitForm, request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

@csrf_exempt
def editUnit(request):
        if request.method == 'POST':
                unitForm = EditUnit(data=request.POST)
                if saveUnit(unitForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

@csrf_exempt
def deleteUnit(request):
        if request.method == 'POST':
                unitForm = DeleteUnit(data=request.POST)
                if deleteUnitData(unitForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)


@csrf_exempt
def addLesson(request):
        if request.method == 'POST':
                addLessonForm = AddLessonForm(data=request.POST)
                if saveLesson(addLessonForm, request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

@csrf_exempt
def editLesson(request):
        if request.method == 'POST':
                lessonForm = EditLesson(data=request.POST)
                if saveLesson(lessonForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

@csrf_exempt
def deleteLesson(request):
        if request.method == 'POST':
                lessonForm = DeleteLesson(data=request.POST)
                if deleteLessonData(lessonForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return lastPageToView(request)

def DeleteCourseRequest(request, course_id):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        course = Course.objects.get(id=course_id)
        deleteCourseForm = DeleteCourse()
        deleteCourseForm.fields["course_id"].initial = course.id
        return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'deleteCourseForm':deleteCourseForm,'showDeleteCourse': 1}, context_instance=RequestContext(request))


def EditCourseRequest(request, course_id):
	uname = request.user.username
	user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
	course = Course.objects.get(id=course_id)
	editCourseForm = EditCourse()	
	editCourseForm.fields["course_id"].initial = course.id	
	editCourseForm.fields["name"].initial = course.subject
	editCourseForm.fields["department"].initial = course.department
	editCourseForm.fields["year"].initial = course.year
	return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'editCourseForm':editCourseForm,'showEditCourse': 1})

def DeleteUnitRequest(request, unitID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        unit = Unit.objects.get(id=unitID)
        deleteUnitForm = DeleteUnit()
        deleteUnitForm.fields["unitID"].initial = unit.id
	course_units =  Unit.objects.filter(course=unit.course)
        return render_to_response('unit.html', {'course_id':unit.course.id,'userUnits':course_units,'userCourses': user_courses, 'username':uname, 'fullname':uname, 'deleteUnitForm':deleteUnitForm,'showDeleteUnit': 1}, context_instance=RequestContext(request))


def EditUnitRequest(request, unitID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        unit = Unit.objects.get(id=unitID)
        editUnitForm = EditUnit()
        editUnitForm.fields["unitID"].initial = unit.id
	editUnitForm.fields["course_id"].initial = unit.course.id
        editUnitForm.fields["name"].initial = unit.name
        editUnitForm.fields["description"].initial = unit.description
        editUnitForm.fields["week_length"].initial = unit.week_length
	course_units =  Unit.objects.filter(course=unit.course)
        return render_to_response('unit.html', {'course_id':unit.course.id,'userUnits':course_units,'userCourses': user_courses, 'username':uname, 'fullname':uname, 'editUnitForm':editUnitForm,'showEditUnit': 1})

def DeleteLessonRequest(request, lessonID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        lesson = Lesson.objects.get(id=lessonID)
        deleteLessonForm = DeleteLesson()
        deleteLessonForm.fields["lessonID"].initial = lesson.id
	unit_lessons =  Lesson.objects.filter(unit=lesson.unit)
        return render_to_response('lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname, 'fullname':uname,'userLessons':unit_lessons, 'deleteLessonForm':deleteLessonForm,'showDeleteLesson': 1}, context_instance=RequestContext(request))


def EditLessonRequest(request, lessonID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        lesson = Lesson.objects.get(id=lessonID)
        unit = lesson.unit
	unit_lessons =  Lesson.objects.filter(unit=lesson.unit)
	editLessonForm = EditLesson()
	editLessonForm.fields["lessonID"].initial = lesson.id
        editLessonForm.fields["unitID"].initial = unit.id
        editLessonForm.fields["name"].initial = lesson.name
        return render_to_response('lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname,'userLessons':unit_lessons, 'fullname':uname, 'editLessonForm':editLessonForm,'showEditLesson': 1})


def saveCourse(addCourseForm, request_user):
	if addCourseForm.is_valid():
		course = Course()
		if 'course_id' in addCourseForm.data:
			course = Course.objects.get(id=addCourseForm.data['course_id'])
		course.owner = UserProfile.objects.get(user=request_user)
		course.subject = addCourseForm.data['name']
		course.department = addCourseForm.data['department']
		course.year = str(addCourseForm.data['year'])
		course.save()
		return True;
	return False;

def saveUnit(addUnitForm, request_user):
	if addUnitForm.is_valid():
		print "creating unit"
		unit = Unit()
		if 'unitID' in addUnitForm.data:
                        unit = Unit.objects.get(id=addUnitForm.data['unitID'])
		user = UserProfile.objects.get(user=request_user)
		course_id = addUnitForm.data['course_id']
                course = Course.objects.get(id=course_id)
                slist = Standard.objects.filter(department=course.department, owner_type=user.user_school_state)
                s_choices = [(s.id, s.description) for s in slist]
		addUnitForm.fields['standards'].choices = s_choices	
		unit.name = addUnitForm.data['name']
		unit.description = addUnitForm.data['description']
		unit.course = course
		unit.owner = UserProfile.objects.get(user=request_user)
		unit.week_length = addUnitForm.data['week_length']
		tags_ = addUnitForm.data['tags']
		separated_tags = tags_.split(',')
		unit.save()
		for t in separated_tags:
			newTag, created = Tag.objects.get_or_create(tagname=t)
			unit.tags.add(newTag)
		for s in addUnitForm.cleaned_data['standards']:
			standard_id = int(s)
			standard = Standard.objects.get(id=standard_id)
			print standard
			unit.standards.add(standard)
		return True
	print addUnitForm.errors
	return False

def saveLesson(addLessonForm, request_user):
        if addLessonForm.is_valid():
                lesson = Lesson()
                if 'lessonID' in addLessonForm.data:
                        lesson = Lesson.objects.get(id=addLessonForm.data['lessonID'])
                lesson.name = addLessonForm.data['name']
                unitID = addLessonForm.data['unitID']
                unit = Unit.objects.get(id=unitID)
                lesson.owner = UserProfile.objects.get(user=request_user)
		lesson.unit = unit
                lesson.save()
		return True
	print "invalid form - lesson"
        print addLessonForm.errors
        return False


def deleteCourseData(courseForm, request_user):
	if 'course_id' in courseForm.data:
       		Course.objects.get(id=courseForm.data['course_id']).delete()
                return True;
        return False;

def deleteUnitData(unitForm, request_user):
        if 'unitID' in unitForm.data:
                Unit.objects.get(id=unitForm.data['unitID']).delete()
                return True;
        return False;

def deleteLessonData(lessonForm, request_user):
	print lessonForm.data
        if 'lessonID' in lessonForm.data:
                Lesson.objects.get(id=lessonForm.data['lessonID']).delete()
                return True;
        return False;

