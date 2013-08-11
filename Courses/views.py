from Courses.models import Course
from Utils.ajax_helpers import direct_block_to_template, direct_json_to_template
from django.template import loader,Context
from django.contrib.auth.models import User
import course_methods
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
import Utils.base_methods as base_methods
from Courses.forms import *
from Lessons.models import Lesson
import simplejson

# Create your views here.

def showCourses(request):
	base_dict = base_methods.createBaseDict(request)
	print base_dict
	if base_dict == None:
		return HttpResponseRedirect('/')
	
	request.session['last_page'] = '/courses/'
	return render(request,'course.html', base_dict)	


def addCourse(request):
	if request.method == 'POST':

		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			logout(request)
			return HttpResponseRedirect('/')
		addCourseForm = AddCourse(data=request.POST, teacher=teacher)
		if addCourseForm.is_valid():
			course = addCourseForm.save()
			groups_added = addCourseStandards(course, teacher)
			standard_list = course_methods.getCourseStandards(course, False)
			context = {'groupStandards': standard_list, 'justSynced': True}
			return direct_json_to_template(request,'course_view_standards.html', 'showGroupStandards', context, {'success':'1'})
		else:
			print addCourseForm.errors
			context = {'courseAddForm':addCourseForm}
			return direct_json_to_template(request,'course_add_modal.html', 'addCourse', context, {'success':'0'})
	return HttpResponseRedirect('/courses/')

def addCourseStandards(course, teacher):
	standards = Standard.objects.filter(subject=course.subject).filter(grade=course.grade)
	groups_to_render = []
        groups_add = {};
	
	for standard in standards:
		good_standard = False
		if standard.standard_type == 'State':
			if (standard.state == teacher.state):
				good_standard=True
		else:
			good_standard=True
		if good_standard:
			for sg in standard.standardgrouping_set.all():
				if sg.prebuilt==True:
					course.standard_grouping.add(sg)
		
	for group in course.standard_grouping.all():
		slist = []
		for standard in group.standard.all():
			slist.append(standard)
		groups_add[group] = slist
	return groups_add

def editCourse(request):
	if request.method == 'POST':
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			logout(request)
			return HttpResponseRedirect('/')
		course_id = request.POST['selectedCourse']
		course = Course.objects.get(id=course_id)
                editCourseForm = EditCourse(request.POST, instance=course)
                if editCourseForm.is_valid():
			editCourseForm.save()
			course.standard_grouping.clear()
			groups_added = addCourseStandards(course,teacher)
			return HttpResponse(simplejson.dumps({'success':'1'}))
		else:
			print editCourseForm.errors
			context = {'editCourseForm':editCourseForm, 'selectedCourse':course_id}
			return direct_json_to_template(request,'course_edit_modal.html', 'editCourse', context, {'success':'0'})
        return HttpResponseRedirect('/courses/')

def deleteCourse(request):
        if request.method == 'POST':
                if deleteCourseData(request.POST.get('course_id', None)):
                        return HttpResponseRedirect(request.session['last_page'])
        return HttpResponseRedirect(request.session['last_page'])

def EditCourseRequest(request):
	if request.method == 'POST':
		course_id = request.POST['course_id']
		course = Course.objects.get(id=course_id)
		editCourseForm = EditCourse(instance=course)	
		context = {'editCourseForm':editCourseForm, 'selectedCourse':course_id}
        	return direct_block_to_template(request,'course_edit_modal.html', 'editCourse', context)
	return HttpResponse('')


def deleteCourseData(course_id):
	if course_id:
       		Course.objects.get(id=course_id).delete()
                return True;
        return False;


def publicCourseView(request):
	base_dict = base_methods.createBaseDict(request)
	course_id = request.GET['course_id']
	course = Course.objects.get(id=course_id)
	base_dict.update(course_methods.getCourseInfo(course))
	return render(request,'public_course_view.html',base_dict)

'''
this will get the add form course given the standard
'''
def createCourseFromStandard(request):
	if request.method == 'POST':
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			return HttpResponse('')
		sid = request.POST.get('standard_id')
		if sid == None:
			return HttpResponse('')
		try:
			standard = Standard.objects.get(id=sid)
		except:
			return HttpResponse('')
		t = standard.standard_type
		s = None
		if (t.value == 'State'):
			s = standard.state
		b = standard.subject
		g = standard.grade
		addCourseForm = AddCourse(grade=g, owner=teacher, subject=b)
		context = {'courseAddForm': addCourseForm}
		return direct_block_to_template(request,'course_add_modal.html', 'addCourse', context)
	return HttpResponse('')

def cloneCourse(request):
	if request.method  == 'POST':
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			return HttpResponse('')
		course_id = request.POST.get('course_id')
		if course_id == None:
			return HttpResponse('')
		try:
			course = Course.objects.get(id=course_id)
		except:
			return HttpResponse('')
		new_course = course_methods.deepcopy_course(course, teacher)
		if new_course:
			return HttpResponse('success')
	return HttpResponse('')

