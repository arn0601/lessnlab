from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from Utils import base_methods
from django.core import serializers
from Standards.models import Standard
from Standards.forms import *
from Objectives.models import Objective
from Types import *
from Courses.models import *
from Units.models import *
from Lessons.models import *
# Create your views here.

def standardsSearch(request):
	base_dict = base_methods.createBaseDict(request)
	base_dict['standardsSearchForm'] = StandardsSearchForm(auto_id='standard_search_%s')
	if request.method == 'POST':
		standards = []
		form = StandardsSearchForm(data=request.POST)
		if form.is_valid():
			has_state = False
			grade = form.cleaned_data['grade']
			subject = form.cleaned_data['subject']
			standard_type = form.cleaned_data['standard_type']
			qset = Standard.objects.filter(subject=subject,grade=grade,standard_type=standard_type)
			if ( form.cleaned_data['standard_type'] == 'State'):
				state = form.cleaned_data['state']
				qset.filter(state=state)
			print qset
			for standard in qset:
				if standard.state != None:
					has_state=True
				standards.append(standard)
			print grade, subject, standard_type				
			standards.sort(key=lambda x: (int(x.numbering) if x.numbering.isdigit() else x.numbering))
			print standards
			base_dict['standard_type'] = form.cleaned_data['standard_type']
			base_dict['state'] = form.cleaned_data['state']
			base_dict['searchedStandards'] = standards
			base_dict['standardsSearchForm'] = form
			base_dict['returnResults'] = True
			base_dict['has_state'] = has_state
			return render(request,'standards_search.html', base_dict)
		else:
			return HttpResponseRedirect('/standardsSearch/')
	return render(request,'standards_search.html', base_dict)

def getStandard(request):
	if request.method == 'GET':
		base_dict = base_methods.createBaseDict(request)
		if base_dict == None:
			return HttpResponseRedirect('/login/')
		standard_id = request.GET['standard_id']
		try:
			s = Standard.objects.get(id=standard_id)
		except:
			return HttpResponseRedirect('/courses/')
		standard_groupings = s.standardgrouping_set.all()
		courses = {}
		for sg in standard_groupings:
			for course in sg.course_set.all():
				courses[course] = 0
		for course in courses:
			ratings = CourseRating.objects.filter(course=course)
			rating_list = [rating.value for rating in ratings]
			course_rating = 0
			if ( len(rating_list) > 0 ):
				course_rating = reduce(lambda x, y: x+y, rating_list)/float(len(rating_list))
			courses[course] = course_rating
		objectives = Objective.objects.filter(standard=s)
		objective_dict = {}
		for objective in objectives:
			ratings= ObjectiveRating.objects.filter(objective=objective)
			rating_list = [rating.value for rating in ratings]
			objective_rating = 0
			if (len(rating_list) > 0):
				objective_rating = reduce(lambda x, y: x+y, rating_list)/float(len(rating_list))
			objective_dict[objective] = objective_rating
		sa = StandardAnalysis.objects.filter(standard=s).order_by('cumulative_rating')
		base_dict['analysis'] = sa
		base_dict['standardCourses'] = courses
		base_dict['standard'] = s
		base_dict['standardObjectives'] = objective_dict
		saf = StandardAnalysisForm(standard_id=s.id)
		base_dict['standardAnalysisForm'] = saf
		base_dict['ratingOptions'] = (1,2,3,4,5)
		base_dict['user_id'] = request.user.id
		return render(request,'standard_view.html', base_dict)

	return HttpResponseRedirect('/courses/')
