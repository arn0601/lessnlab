from Objectives.models import Objective
from Standards.models import Standard
from Standards.forms import StandardsSearchForm
from forms import *
from Questions.models import *
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from accounts.models import TeacherProfile

# Create your views here.

def StandardsSearch(request):
	base_dict = {}
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
			return render(request,'standards_list_for_objectives.html', base_dict)
		else:
			print form.errors
			return HttpResponseRedirect('/extra/standardsForObjectives/')
	else:
		print "not post"
		return render(request,'standards_list_for_objectives.html', base_dict)

def ObjectivesPage(request):
	base_dict = {}
	standard_id = request.GET.get('standard_id')
	try:
		print 'asfgfd'
		s = Standard.objects.get(id=standard_id)
		base_dict['standard'] = s
	except:
		return HttpResponseRedirect('/extra/standardsForObjectives/')
	if standard_id:
		base_dict['objectivesAddForm'] = CreateObjectivesPoolForm(standard_id=standard_id)
	else:
		return HttpResponseRedirect('/extra/standardsForObjectives/')
	if request.method == 'POST':
		form = CreateObjectivesPoolForm(data=request.POST)
		
		standard = Standard.objects.get(id=int(form.data['standard_id']))
		if form.is_valid():
			new_count = form.cleaned_data['new_objectives_count']
			for index in range(0,int(new_count)):
				new_o = Objective()
				new_o.description = form.data['new_objective_{index}'.format(index=index)]
				new_o.standard = standard
				new_o.creation_date = datetime.today()
				if request.user:
					new_o.owner = TeacherProfile.objects.get(user=request.user)
				if (new_o.description != ""):
					new_o.save()
		else:
			print form.errors
	base_dict['createdObj'] = Objective.objects.filter(standard=s)
	return render(request,'objectives_adding_content.html',base_dict)

def createCFU(request):
	objective_id = request.GET.get('objective_id')
	try:
		objective = Objective.objects.get(id=objective_id)
	except:
		HttpResponseRedirect('/extra/standardsForObjectives/')
	base_dict = {}
	base_dict['mcform'] = CreateMultipleChoiceQuestion(objective_id=objective_id)
	base_dict['frform'] = CreateFreeResponseQuestion(objective_id=objective_id)
	base_dict['objective'] = objective
	print request
	if request.method == 'POST':
		qtype = request.POST.get('qtype')
		if qtype:
			if (qtype == 'MC'):
				form = CreateMultipleChoiceQuestion(data=request.POST, objective_id=request.POST.get('objective_id'), new_answer_count=request.POST.get('new_answer_count'))
				if form.is_valid():
					print form
					q = form.cleaned_data['question']
					objective = Objective.objects.get(id=form.cleaned_data['objective_id'])
					question = Question()
					question.objective = objective
					question.question = q
					if request.user:
						question.owner = TeacherProfile.objects.get(user=request.user)
					question.save()
					answer_list = []
					for i in range(0,int(form.cleaned_data['new_answer_count'])):
						a = form.cleaned_data['new_answer_{index}'.format(index=i)]
						print a
						answer = TeacherAnswer()
						if request.user:
							answer.owner = TeacherProfile.objects.get(user=request.user)
						if a.startswith('correct:'):
							a=a[8:]
							answer.answer=a
							answer.correct = True
						else:
							answer.answer=a
							answer.correct = False
						answer.question = question
						answer.save()
			if (qtype == 'FR'):
				form = CreateFreeResponseQuestion(data=request.POST)
				if form.is_valid():
					q = form.cleaned_data['question']
					objective = Objective.objects.get(id=form.cleaned_data['objective_id'])
					question = Question()
					if request.user:
						question.owner = TeacherProfile.objects.get(user=request.user)
					question.objective = objective
					question.question = q
					saved_q = question.save()
					a = form.cleaned_data['answer']
					answer=TeacherAnswer()
					answer.question = question
					answer.answer=a
					answer.correct = True
					if request.user:
							answer.owner = TeacherProfile.objects.get(user=request.user)
					answer.save()
					
		else:
			return HttpResponseRedirect('/extra/standardsForObjectives/')

	qs=  Question.objects.filter(objective=objective)
	allqs = {}
        for q in qs:
		allqs[q] = TeacherAnswer.objects.filter(question=q)
	base_dict['allqs'] = allqs
	return render(request, 'questions_for_objective.html', base_dict)


