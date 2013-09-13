from Units.models import Unit
from Utils.ajax_helpers import direct_block_to_template, direct_json_to_template, render_block_to_string
from django.template import RequestContext, Context
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from Courses.models import Course
from Lessons.models import  Lesson
from Lessons.forms import *
import lesson_methods
import simplejson
from Utils import base_methods
from Units import unit_methods
from datetime import datetime
from Objectives.models import Objective
# Create your views here.
def showLessons(request):
	if base_methods.checkUserIsTeacher(request):
		base_dict = base_methods.createBaseDict(request)
		request.session['last_page'] = '/lessons/?unit_id='+str(base_dict['unit'].id)
		return render(request,"lesson.html", base_dict)
	elif base_methods.checkUserIsStudent(request):
		student_dict = base_methods.createStudentDict(request)
		return render(request,"student_lesson.html", student_dict)
	else:
		return HttpResponseRedirect('/')
	
#this function is used when creating objectives to select the initial standard
def getLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponse("")
		standard_list = lesson_methods.getLessonStandards(lesson, True)
		form = SelectStandardsForm(lesson_id=lesson_id)
		form.fields['standard'].choices = standard_list
		print "here getting stnadards"
		context = {'selectStandardsForm':form, 'standardsExist':(len(standard_list) > 0)}
		
		return direct_block_to_template(request,"lesson_objectives_modal.html", "selectingStandard", context)

def requestAddableLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponseRedirect(request.session['last_page'])
		
		unit = lesson.unit
		standard_list = unit_methods.getUnitStandards(unit, True)
		form = LessonStandardsForm(lesson_id=lesson_id)
		form.fields['standards'].choices = standard_list
		context = { 'lessonStandardsForm':form}
		return direct_block_to_template(request,'lesson_standards_modal.html', 'addLessonStandards', context)

#this returns the form to add objectives
def createLessonObjectives(request):
	if request.method == 'POST':
		standards_form = SelectStandardsForm(data=request.POST)
		try:
			lesson_id = standards_form.data.get('lesson_id')
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponse("")
		standard_list = lesson_methods.getLessonStandards(lesson, True)
		standards_form.fields['standard'].choices = standard_list	
		if standards_form.is_valid():
			try:
				s = Standard.objects.get(id=standards_form.cleaned_data['standard'])
			except:
				print "standard not found"
				return HttpResponseRedirect(request.session['last_page'])
			best_objectives = Objective.objects.filter(standard=s)[:5]
			obj_list = []
			for obj in best_objectives:
				obj_list.append((obj.id, obj.description))
			next_form = CreateObjectivesForm(standard_id=standards_form.cleaned_data['standard'], lesson_id=standards_form.cleaned_data['lesson_id'])
			next_form.fields['created'].choices = obj_list
			context = {'createObjectivesForm':next_form}
			return direct_block_to_template(request,"lesson_objectives_modal.html","addingLessonObjectives",context)
		else:
			print standards_form.errors
	return HttpResponse("")


def addLessonObjectives(request):
	if request.method == 'POST':
		form = CreateObjectivesForm(data=request.POST)
		
		teacher = base_methods.checkUserIsTeacher(request)
		if not teacher:
			logout(request)
			return HttpResponseRedirect('/')
		try:
			lesson = Lesson.objects.get(id=int(form.data['lesson_id']))
			standard = Standard.objects.get(id=int(form.data['standard_id']))
		except:
			return HttpResponseRedirect(request.session['last_page'])
		
		objectives_list = [(o.id,o.description) for o in Objective.objects.filter(standard=standard)]
		form.fields['created'].choices = objectives_list
		if form.is_valid():
			already_created = form.cleaned_data['created']
			for obj_id in already_created:
				old_o = Objective.objects.get(id=obj_id)
				new_o = Objective()
				new_o.description = old_o.description
				new_o.standard = old_o.standard
				new_o.owner = teacher
				new_o.creation_date = datetime.today()
				new_o.lesson = lesson
				new_o.save()
			new_count = form.cleaned_data['new_objectives_count']
			for index in range(0,int(new_count)):
				new_o = Objective()
				new_o.description = form.data['new_objective_{index}'.format(index=index)]
				new_o.standard = standard
				new_o.owner = teacher
				new_o.creation_date = datetime.today()
				new_o.lesson = lesson
				new_o.save()
		else:
			print form.errors
		return HttpResponseRedirect(request.session['last_page'])				
	return HttpResponseRedirect(request.session['last_page'])

def addLessonStandards(request):
	if request.method == 'POST':
		form = LessonStandardsForm(data=request.POST)

		teacher = base_methods.checkUserIsTeacher(request)
		if not teacher:
			logout(request)
			return HttpResponseRedirect('/')
		try:
			lesson = Lesson.objects.get(id=int(form.data['lesson_id']))
		except:
			return HttpResponseRedirect(request.session['last_page'])
		
		unit = lesson.unit
		standard_list = unit_methods.getUnitStandards(unit, True)
		form.fields['standards'].choices = standard_list
		if form.is_valid():
			for sid in form.cleaned_data['standards']:
				s = Standard.objects.get(id=sid)
				lesson.standards.add(s)
		else:
			print form.errors
		return HttpResponseRedirect("/lessons/?unit_id="+str(unit.id))
	return HttpResponseRedirect(request.session['last_page'])


def addLesson(request):
        if request.method == 'POST':
                addLessonForm = AddLessonForm(request.POST)
                if addLessonForm.is_valid():
			addLessonForm.save()
			return HttpResponse(simplejson.dumps({'success': '1'}))
		else:
			context = {'lessonAddForm':addLessonForm}
			return direct_json_to_template(request,'lesson_add_modal.html', 'addLesson', context, {'success':'0'})
			
        return HttpResponse('')

def editLesson(request):
	print request
        if request.method == 'POST':
		lesson_id = request.POST['selectedLesson']
		lesson = Lesson.objects.get(id=lesson_id)
                lessonForm = EditLesson(request.POST, instance=lesson)
                if lessonForm.is_valid():
			lesson=lessonForm.save()
			return HttpResponse(simplejson.dumps({'success': '1'}))
		else:
			context = {'editLessonForm':lessonForm, 'selectedLesson':lesson_id}
			return direct_json_to_template(request,'lesson_edit_modal.html', 'editLesson', context, {'success':'0'})
        return HttpResponseRedirect(request.session['last_page'])

def deleteLesson(request):
        if request.method == 'POST':
                lessonForm = DeleteLesson(data=request.POST)
                if deleteLessonData(lessonForm,request.user):
                        return HttpResponseRedirect(request.session['last_page'])
        return HttpResponseRedirect(request.session['last_page'])


def DeleteLessonRequest(request):
	if request.method == 'POST':
		lessonID = request.POST.get('lesson_id')
	        lesson = Lesson.objects.get(id=lessonID)
        	deleteLessonForm = DeleteLesson(lesson_id=lesson.id)
		context = {'deleteLessonForm':deleteLessonForm}
		return direct_block_to_template(request,"lesson_delete_modal.html", 'deleteLesson', context)
	return HttpResponse('')

def EditLessonRequest(request):
	if request.method == 'POST':
		lessonID = request.POST.get('lesson_id')
        	lesson = Lesson.objects.get(id=lessonID)
		editLessonForm = EditLesson(instance=lesson)
		context = {'editLessonForm':editLessonForm, 'selectedLesson':lessonID}
		return direct_block_to_template(request,'lesson_edit_modal.html', 'editLesson', context)
	return HttpResponse('')



def deleteLessonData(lessonForm, request_user):
        if 'lesson_id' in lessonForm.data:
                Lesson.objects.get(id=lessonForm.data['lesson_id']).delete()
                return True;
        return False;
