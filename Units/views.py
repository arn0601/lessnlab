from Units.models import Unit
from Units.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from Utils import base_methods
from Courses import course_methods
import unit_methods
from Lessons.models import Lesson
from Utils.ajax_helpers import direct_block_to_template, direct_json_to_template
from django.template import loader,Context
from django.contrib.auth.models import User
import simplejson

# Create your views here.
def showUnits(request):
	if base_methods.checkUserIsTeacher(request.user):
		base_dict = base_methods.createBaseDict(request)
		#return from base
		request.session['last_page'] = '/units/?course_id='+str(base_dict['course'].id)
		return render(request,"unit.html", base_dict)
	if base_methods.checkUserIsStudent(request):
		student_dict = base_methods.createStudentDict(request)
		return render(request,"student_unit.html", student_dict)
	else:
		return HttpResponseRedirect('/')
#show the lessons of a unit

def addUnit(request):
	if request.method == 'POST':
                addUnitForm = AddUnitForm(request.POST)
                if addUnitForm.is_valid():
			addUnitForm.save()
			return HttpResponse(simplejson.dumps({'success': '1'}))
		else:
			print addUnitForm.errors
			context = {'unitAddForm':addUnitForm}
			return direct_json_to_template(request,'unit_add_modal.html', 'addUnit', context, {'success':'0'})
			
        return HttpResponseRedirect('')

def editUnit(request):
        if request.method == 'POST':
		unit_id = request.POST['selectedUnit']
		unit = Unit.objects.get(id=unit_id)
                unitForm = EditUnit(request.POST, instance=unit)
                if unitForm.is_valid():
			unitForm.save()
			return HttpResponse(simplejson.dumps({'success': '1'}))
		else:
			print unitForm.errors
			context = {'editUnitForm':unitForm, 'selectedUnit':unit_id}
			return direct_json_to_template(request,'unit_edit_modal.html', 'editUnit', context, {'success':'0'})
        return HttpResponseRedirect(request.session['last_page'])

def addUnitStandards(request):
	if request.method == 'POST':
		form = UnitStandardsForm(data=request.POST)
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			logout(request)
			return HttpResponseRedirect('/')
		try:
			unit = Unit.objects.get(id=int(form.data['unit_id']))
		except:
			return HttpResponseRedirect(request.session['last_page'])
		
		course = unit.course
		standard_list = course_methods.getCourseStandards(course, True)
		form.fields['standards'].choices = standard_list
		if form.is_valid():
			
			for sid in form.cleaned_data['standards']:
				s = Standard.objects.get(id=sid)
				unit.standards.add(s)
		else:
			print form.errors
		return HttpResponseRedirect(request.session['last_page'])				
	return HttpResponseRedirect(request.session['last_page'])


def requestAddableUnitStandards(request):
	if request.method == 'POST':
		unit_id = request.POST['unit_id']
		try:
			unit = Unit.objects.get(id=unit_id)
		except:
			return HttpResponseRedirect(request.session['last_page'])
		course = unit.course
		standard_list = course_methods.getCourseStandards(course, True)
		form = UnitStandardsForm(unit_id=unit_id)
		unit_list = unit_methods.getUnitStandards(unit, True)
		unit_standards_choices = [x for (x,y) in unit_list]
		form.fields['standards'].choices = standard_list
		form.fields['standards'].initial = unit_standards_choices
		context = {'unitStandardsForm': form}
		return direct_block_to_template(request,'unit_standards_modal.html', 'addStandards', context)


def deleteUnit(request):
        if request.method == 'POST':
                if deleteUnitData(request.POST.get('unit_id', None)):
                        return HttpResponseRedirect(request.session['last_page'])
        return HttpResponseRedirect(request.session['last_page'])



def EditUnitRequest(request):
	if request.method == 'POST':
		print "change this"
		unitID = request.POST['unit_id']
	        unit = Unit.objects.get(id=unitID)
        	editUnitForm = EditUnit(instance=unit)
		context = {'editUnitForm':editUnitForm, 'selectedUnit':unitID}
        	return direct_block_to_template(request,'unit_edit_modal.html', 'editUnit', context)
	return HttpResponse('')


def deleteUnitData(unit_id):
	if unit_id:
		Unit.objects.get(id=unit_id).delete()
		return True
	return False

def publicUnitView(request):
	base_dict = base_methods.createBaseDict(request)
	unit_id = request.GET['unit_id']
	unit = Unit.objects.get(id=unit_id)
	unit_delta = (unit.end_date - unit.start_date)
	base_dict['unit_length']=(unit_delta.days/7, unit_delta.days%7)
	unit_lessons = Lesson.objects.filter(unit=unit)
	unit_lesson_list = []
	for lesson in unit_lessons:
		ratings = LessonRating.objects.filter(lesson=lesson)
		rating_list = [rating.rating for rating in ratings]
		rating = 0
		if ( len(rating_list) > 0):
			rating = reduce(lambda x, y: x+y, rating_list)/float(len(rating_list))
		unit_lesson_list.append((lesson, rating))
	unit_standards = unit_methods.getUnitStandards(unit, False)
	base_dict['unitStandards'] = unit_standards
	base_dict['unitLessons'] = unit_lesson_list
	return render(request,'public_unit_view.html',base_dict)

def publicUnitView(request):
	base_dict = base_methods.createBaseDict(request)
	unit_id = request.GET['unit_id']
	unit = Unit.objects.get(id=unit_id)
	unit_delta = (unit.end_date - unit.start_date)
	base_dict['unit_length']=(unit_delta.days/7, unit_delta.days%7)
	unit_lessons = Lesson.objects.filter(unit=unit)
	unit_lesson_list = []
	for lesson in unit_lessons:
		ratings = LessonRating.objects.filter(lesson=lesson)
		rating_list = [rating.rating for rating in ratings]
		rating = 0
		if ( len(rating_list) > 0):
			rating = reduce(lambda x, y: x+y, rating_list)/float(len(rating_list))
		unit_lesson_list.append((lesson, rating))
	unit_standards = unit_methods.getUnitStandards(unit, False)
	base_dict['unitStandards'] = unit_standards
	base_dict['unitLessons'] = unit_lesson_list
	return render(request,'public_unit_view.html',base_dict)

###############################################

def showStudentUnits(request):
	if request.method == 'GET':
		student_dict = base_methods.createStudentDict(request)
		render(request, "student_units.html", student_dict)
