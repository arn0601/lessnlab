# Create your views here.
from django.template import RequestContext
from LessonPlanner.models import Lesson,Course,Unit,Section
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Standards.models import *
from Objectives.models import Objective, ObjectiveRating
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile
from accounts.forms import TeacherRegistrationForm
from datetime import datetime
from django.utils.timezone import utc
import simplejson
import base_methods 
from ajax_helpers import render_block_to_string
from django.template import loader,Context
from django.contrib.auth.models import User
import sys, traceback
import urlparse


@csrf_exempt
def activity_add(request):
	if request.method == 'POST':
                addCourseForm = AddActivityContent(data=request.POST)
		if addCourseForm.is_valid():
			addCourseForm.save()
		else:
			print addCourseForm.errors
	return HttpResponseRedirect(lastPageToView(request))


@csrf_exempt
def activity_ajax_view(request):
	return_str = ""
	if request.method == 'POST':
		activity_id = request.POST.get('activity_id',-1)
		section_id = request.POST.get('section_id',-1)
		if activity_id==-1:
			placement = getMaxCount(Section.objects.get(id=section_id))+1
			activityForm = AddActivityContent(initial={'section': section_id,'placement' : placement,'content_type':"Activity"})
			context = Context({'activityForm': activityForm, 'activity_id':activity_id})
			return_str = render_block_to_string('ActivityViewModal.html', 'results', context)
		else:
			placement = getMaxCount(Section.objects.get(id=section_id))+1
			ac = ActivityContent.objects.get(id=activity_id)
			activityForm = AddActivityContent(instance=ac,initial={'section': section_id,'placement' : placement,'content_type':"Activity"})
			context = Context({'activityForm': activityForm, 'activity_id':activity_id})
			return_str = render_block_to_string('ActivityViewModal.html', 'results', context)
	
	return HttpResponse(return_str)

@csrf_exempt
def requestLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		unit = lesson.unit
		standard_list = []
		for standard in unit.standards.all():
			standard_list.append((standard.id, standard.description))
		form = LessonStandardsForm()
		form.fields['standards'].choices = standard_list
		form.fields['lesson_id'].initial = lesson_id
		context = Context({ 'lessonStandardsForm':form})
		return HttpResponse(render_block_to_string('lesson_standards_modal.html', 'addLessonStandards', context))

@csrf_exempt
def requestUnitStandards(request):
	if request.method == 'POST':
		unit_id = request.POST['unit_id']
		try:
			unit = Unit.objects.get(id=unit_id)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		course = unit.course
		standard_list = []
		for group in course.standard_grouping.all():
			for standard in group.standard.all():
				standard_list.append((standard.id, standard.description))
		form = UnitStandardsForm()
		form.fields['standards'].choices = standard_list
		form.fields['unit_id'].initial = unit_id
		context = Context({'unitStandardsForm': form})
		return HttpResponse(render_block_to_string('unit_standards_modal.html', 'addStandards', context))

@csrf_exempt
def search_activity_ajax_view(request):
	if request.method == 'POST':
		section_id = request.POST.get('section_id',-1)
		act_type = request.POST['type']
		act_length = request.POST['length']
		act_obj = request.POST['objective']
	# some random context
		dataset = ActivityContent.objects.all()
		if act_type != "":
			dataset = dataset.filter(activity_type__contains=act_type)
		if act_length != "":
			dataset = dataset.filter(length__contains=act_length)
		print dataset
		context = Context({'activities_found':dataset, 'section_id' : section_id})
	# passing the template_name + block_name + context
		return_str = render_block_to_string('ActivitySearchModal.html', 'results', context)
		return HttpResponse(return_str)

def team(request):
        return render(request,'team.html', {})

def landing(request):
	teacher_registration_form = TeacherRegistrationForm()
	return render(request,'landing.html', {'teacherRegistrationForm': teacher_registration_form})

#show the units for a specific course

@csrf_exempt
def changeSectionPlacement(request):
	base_dict = base_methods.createBaseDict(request)
	lesson_info = base_methods.getLessonSpecificInfo(base_dict['lesson'])
	sectionList = lesson_info['sections'].keys()
	l = []
	for sec in sectionList:
		l.append((sec, sec.placement))
        l.sort(key=lambda x: x[1])

	start=int(request.POST["start"])-1
	final=int(request.POST["final"])-1
	a1 = l[start]
	del l[start]
	l.insert(final,a1)
	counter = 0
	for sec in l:
		sec[0].placement = counter
		sec[0].save()	
		counter = counter + 1
	return HttpResponse('')

@csrf_exempt
def showUnits(request):
	base_dict = base_methods.createBaseDict(request)
        action = request.GET.get('action')
	
	#return from base
	user = TeacherProfile.objects.filter(user=request.user)
	request.session['last_page'] = '/units/?course_id='+str(base_dict['course'].id)
	return render(request,"unit.html", base_dict)	
#show the lessons of a unit


@csrf_exempt
def addUnitStandards(request):
	if request.method == 'POST':
		form = UnitStandardsForm(data=request.POST)
		try:
			unit = Unit.objects.get(id=int(form.data['unit_id']))
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		course = unit.course
		standard_list = []
		for group in course.standard_grouping.all():
			for standard in group.standard.all():
				standard_list.append((standard.id, standard.description))
		form.fields['standards'].choices = standard_list
		if form.is_valid():
			
			for sid in form.cleaned_data['standards']:
				s = Standard.objects.get(id=sid)
				unit.standards.add(s)
		else:
			print form.errors
		return HttpResponseRedirect(lastPageToRedirect(request))				
	return HttpResponseRedirect(lastPageToRedirect(request))

def showLesson(request):
	base_dict = base_methods.createBaseDict(request)
        action = request.GET.get('action')

	request.session['last_page'] = '/lessons/?unit_id='+str(base_dict['unit'].id)
	return render(request,"lesson.html", base_dict)
	
#this function is used when creating objectives to select the initial standard
@csrf_exempt
def getLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponse("")
		standard_list = []
		for standard in lesson.standards.all():
			standard_list.append((standard.id, standard.description))
		form = SelectStandardsForm()
		form.fields['standard'].choices = standard_list
		form.fields['lesson_id'].initial = lesson_id
		print "here getting stnadards"
		context = Context({'selectStandardsForm':form})
		
		return HttpResponse(render_block_to_string("lesson_objectives_modal.html", "selectingStandard", context))

#this returns the form to add objectives
@csrf_exempt
def createLessonObjectives(request):
	if request.method == 'POST':
		standards_form = SelectStandardsForm(data=request.POST)
		try:
			lesson_id = standards_form.data.get('lesson_id')
			lesson = Lesson.objects.get(id=lesson_id)
		except:
			return HttpResponse("")
		standard_list = []
		for standard in lesson.standards.all():
			standard_list.append((standard.id,standard.description))
		standards_form.fields['standard'].choices = standard_list	
		if standards_form.is_valid():
			try:
				s = Standard.objects.get(id=standards_form.cleaned_data['standard'])
			except:
				print "standard not found"
				return HttpResponseRedirect(lastPageToRedirect(request))
			best_objectives = Objective.objects.filter(standard=s)[:5]
			obj_list = []
			for obj in best_objectives:
				obj_list.append((obj.id, obj.description))
			next_form = CreateObjectivesForm()
			next_form.fields['created'].choices = obj_list
			next_form.fields['standard_id'].initial = standards_form.cleaned_data['standard']
			next_form.fields['lesson_id'].initial = standards_form.cleaned_data['lesson_id']
			context = Context({'createObjectivesForm':next_form})
			return HttpResponse(render_block_to_string("lesson_objectives_modal.html","addingLessonObjectives",context))
		else:
			print standards_form.errors
	return HttpResponse("")

@csrf_exempt
def addLessonObjectives(request):
	if request.method == 'POST':
		form = CreateObjectivesForm(data=request.POST)
		try:
			lesson = Lesson.objects.get(id=int(form.data['lesson_id']))
			standard = Standard.objects.get(id=int(form.data['standard_id']))
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		if form.is_valid():
			already_created = form.cleaned_data['created']
			for obj_id in already_created:
				old_o = Objective.objects.get(id=obj_id)
				new_o = Objective()
				new_o.description = old_o.description
				new_o.standard = old_o.standard
				new_o.owner = teacher
				new_o.creation_date = datetime.today()
				new_o.save()
				lesson.objectives.add(new_o)
			new_count = form.cleaned_data['new_objectives_count']
			for index in range(0,int(new_count)):
				new_o = Objective()
				new_o.description = form.data['new_objective_{index}'.format(index=index)]
				new_o.standard = standard
				new_o.owner = teacher
				new_o.creation_date = datetime.today()
				new_o.save()
				lesson.objectives.add(new_o)
		else:
			print form.errors
		return HttpResponseRedirect(lastPageToRedirect(request))				
	return HttpResponseRedirect(lastPageToRedirect(request))


@csrf_exempt
def addLessonStandards(request):
	if request.method == 'POST':
		form = LessonStandardsForm(data=request.POST)
		try:
			lesson = Lesson.objects.get(id=int(form.data['lesson_id']))
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		unit = lesson.unit
		standard_list = []
		for standard in unit.standards.all():
			standard_list.append((standard.id, standard.description))
		form.fields['standards'].choices = standard_list
		if form.is_valid():
			for sid in form.cleaned_data['standards']:
				s = Standard.objects.get(id=sid)
				lesson.standards.add(s)
		else:
			print form.errors
		return HttpResponseRedirect("/lessons/?unit_id="+str(unit.id))
	return HttpResponseRedirect(lastPageToRedirect(request))


def showLessonPlanner(request):
	base_dict = base_methods.createBaseDict(request)
	action = request.GET.get('action') 
	if action == "Edit":
		content_id = request.GET.get('content_id')
        	return EditContentRequest(request, content_id)
	base_dict = base_methods.createBaseDict(request)
	lesson_info = base_methods.getLessonSpecificInfo(base_dict['lesson'])
	base_dict.update(lesson_info)
	delete_section_form = DeleteSection()
	delete_content_form = DeleteContent()
	base_dict['deleteSectionForm'] = delete_section_form
	base_dict['deleteContentForm'] = delete_content_form
	request.session['last_page'] = '/lessonPlanner/?lesson_id='+str(base_dict['lesson'].id)
	user = TeacherProfile.objects.filter(user=request.user)
	return render(request,'lessonPlanner.html', base_dict)

def lastPageToView(request):
	if request.session['last_page'] == 'courses':
		return courses(request)
	elif 'units' in request.session['last_page']:
                return unit(request)
	elif 'lessons' in request.session['last_page']:
		return request.session['last_page']
	elif 'lessonPlanner' in request.session['last_page']:
		return request.session['last_page']
	elif 'studentCourses' in request.session['last_page']:
		return showStudentCourses(request)
	return courses(request)
	
def lastPageToRedirect(request):
	if request.session['last_page'] == 'courses':
		return '/courses/'
	elif 'units' in request.session['last_page']:
                return request.session['last_page']
	elif 'lessons' in request.session['last_page']:
                return request.session['last_page']
	elif 'lessonPlanner' in request.session['last_page']:
                return request.session['last_page']
	elif 'studentCourses' in request.session['last_page']:
		return '/studentCourses/'
	return '/courses/'

@csrf_exempt
def courses(request):
	base_dict = base_methods.createBaseDict(request)
	if base_dict == None:
		return HttpResponseRedirect('/studentCourses/')
	action = request.GET.get('action')
	
	request.session['last_page'] = 'courses'
	return render(request,'course.html', base_dict)	

@csrf_exempt
def addCourse(request):
	if request.method == 'POST':
		addCourseForm = AddCourse(data=request.POST)
		if addCourseForm.is_valid():
			course = addCourseForm.save()
			teacher = TeacherProfile.objects.get(user=request.user)
			groups_added = addCourseStandards(course, teacher)
			base_dict = base_methods.createBaseDict(request)
			base_dict['groupsAdded'] = groups_added
			base_dict['addCourseSecondStep'] = True
			return render(request,'course.html', base_dict)
		else:
			print addCourseForm.errors
	return HttpResponseRedirect(lastPageToRedirect(request))

def addCourseStandards(course, teacher):
	standards = Standard.objects.filter(subject=course.subject).filter(grade=course.grade)
	groups_to_render = []
        groups_add = {};
	print standards
	
	for standard in standards:
		good_standard = False
		if standard.standard_type == 'State':
			if (standard.state == teacher.state):
				good_standard=True
		else:
			good_standard=True
		print good_standard
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

@csrf_exempt
def editCourse(request):
	if request.method == 'POST':
		course_id = request.POST['selectedCourse']
		course = Course.objects.get(id=course_id)
                editCourseForm = EditCourse(request.POST, instance=course)
                if editCourseForm.is_valid():
			editCourseForm.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def deleteCourse(request):
        if request.method == 'POST':
                if deleteCourseData(request.POST.get('course_id', None)):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToView(request))

@csrf_exempt
def addUnit(request):
	if request.method == 'POST':
                addUnitForm = AddUnitForm(request.POST)
                if addUnitForm.is_valid():
			addUnitForm.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
	print addUnitForm.errors
        return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def editUnit(request):
        if request.method == 'POST':
		unit_id = request.POST['selectedUnit']
		unit = Unit.objects.get(id=unit_id)
                unitForm = EditUnit(request.POST, instance=unit)
                if unitForm.is_valid():
			unitForm.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def deleteUnit(request):
        if request.method == 'POST':
                if deleteUnitData(request.POST.get('unit_id', None)):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToView(request))


@csrf_exempt
def addLesson(request):
        if request.method == 'POST':
                addLessonForm = AddLessonForm(request.POST)
                if addLessonForm.is_valid():
			addLessonForm.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
	print addLessonForm.errors
        return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def editLesson(request):
        if request.method == 'POST':
		lesson_id = request.POST['selectedLesson']
		lesson = Lesson.objects.get(id=lesson_id)
                lessonForm = EditLesson(request.POST, instance=lesson)
                if lessonForm.is_valid():
			lesson=lessonForm.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def deleteLesson(request):
        if request.method == 'POST':
                lessonForm = DeleteLesson(data=request.POST)
                if deleteLessonData(lessonForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToView(request))

@csrf_exempt
def deleteSection(request):
	if request.method == 'POST':
		sectionForm = DeleteSection(data=request.POST)
		if deleteSectionData(sectionForm,request.user):
			return HttpResponseRedirect(lastPageToRedirect(request))
	return HttpResponseRedirect(lastPageToView(request))

@csrf_exempt
def deleteContent(request):
        if request.method == 'POST':
                contentForm = DeleteContent(data=request.POST)
                if deleteContentData(contentForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToView(request))




@csrf_exempt
def addSection(request):
	if request.method == 'POST':
		sectionForm = AddSectionForm(request.POST)
		section = sectionForm.save(commit=False)
		otherSections = Section.objects.filter(lesson=section.lesson)
		size = len(otherSections)
		section.placement=size+1
		section.save()
	
		sectionForm.save_m2m()
		return HttpResponseRedirect(lastPageToRedirect(request))
	return HttpResponseRedirect(lastPageToRedirect(request))

def getMaxCount(section):
	section_content = Content.objects.filter(section=section)
        maxCont = 0
        for c in section_content:
        	if c.placement > maxCont:
                	maxCont = c.placement
        return  maxCont+1



@csrf_exempt
def addContent(request):
    	if request.method == 'POST':
		contentForm = AddContentForm(data=request.POST)
		content_type = contentForm.data['content_type']
		section = Section.objects.get(id=int(contentForm.data['section_id']))
		if content_type == "OnlineVideo":
			success = saveVideoContent(contentForm, request)
			if success:
				return HttpResponseRedirect(lastPageToRedirect(request))
		        return HttpResponseRedirect(lastPageToView(request))
                (success, content, fields, objectives) =  saveContent(contentForm,section,section.lesson, request)
		if success:
			section = Section.objects.get(id=int(contentForm.data['section_id']))
			content.section = section
			content.creation_date=datetime.now()
			content.content_type = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
			content.save()
			if content_type == "Assessment":
	                        for obj_id in objectives:
                                        o = Objective.objects.get(id=obj_id)
                                        content.objectives.add(o)
			if fields != None:
				for qa in fields:
					(q,ans) = qa
					q.assessment = content
					q.save()
					for a in ans:
						a.question = q
						a.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
	return HttpResponseRedirect(lastPageToView(request))

def cleanVideoLink(link):
	if "youtube" in link:
		url_data = urlparse.urlparse(link)
		query = urlparse.parse_qs(url_data.query)
		return "http://youtube.com/embed/"+query["v"][0]
	elif "vimeo" in link:
		url_data = urlparse.urlparse(link)
		embed_code = urlparse.urlparse(link).path.lstrip("/")
		return "http://player.vimeo.com/video/" + embed_code
	return link


def saveVideoContent(contentForm, request):
       	online_video_form = AddOnlineVideoContent(data=request.POST)
	myDict = dict(request.POST.iterlists())
	for c in myDict['rl']:
		online_video_form.fields["rl"].choices.append((c,c))
	if online_video_form.is_valid():
		content = OnlineVideoContent()
		if online_video_form.data["link"] != "":
			content = OnlineVideoContent()
			content.link = cleanVideoLink(online_video_form.data['link'])
			section = Section.objects.get(id=int(contentForm.data['section_id']))
                        content.section = section
                        content.creation_date=datetime.now()
                        content.content_type = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
			content.save()
		for link in online_video_form.cleaned_data['rl']:
			content = OnlineVideoContent()
			content.link = cleanVideoLink(link)
                        section = Section.objects.get(id=int(contentForm.data['section_id']))
                        content.section = section
                        content.creation_date=datetime.now()
                        content.content_type = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
                        content.save()
		return True
	print online_video_form.errors
        return (False, None, None)


def slicedict(s, d):
    return {k:v for k,v in d.iteritems() if s in k}

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [(key,value) for key, value in items]

def saveContent(contentForm, section, lesson, request):
	
	if contentForm.is_valid():
		content_type = contentForm.data['content_type']
		if (content_type == 'OnlinePicture'):
			online_picture_form = AddOnlinePictureContent(data=request.POST)
			if online_picture_form.is_valid():
				content = OnlinePictureContent()
				content.link = online_picture_form.data['link']
				return (True, content, None,None)
			return (False, None, None,None)
		if (content_type == 'OnlineArticle'):
			online_article_form = AddOnlineArticleContent(data=request.POST)
			if online_article_form.is_valid():
				content = OnlineArticleContent()
				content.link = online_article_form.data['link']
				return (True, content, None,None)
			return (False, None, None,None)
		if (content_type == 'PowerPoint'):
                        powerpoint_form = AddPowerPointContent(data=request.POST)
                        if powerpoint_form.is_valid():
                                content = PowerPointContent()
                                content.link = powerpoint_form.data['link']
                                return (True, content, None,None)
                        return (False, None, None,None)	
		if (content_type == 'Text'):
			text_form = AddTextContent(data=request.POST)
			if text_form.is_valid():
				content = TextContent()
				content.text = text_form.data['text']
				return (True, content, None,None)
			return (False, None, None,None)
		if (content_type == 'TeacherNote'):
			teacher_note_form = AddTeacherNoteContent(data=request.POST)
			if teacher_note_form.is_valid():
				content = TeacherNoteContent()
				content.text = teacher_note_form.data['text']
				return (True, content, None,None)
			return (False, None, None,None)
		if (content_type == 'AdministratorNote'):
			administrator_note_form = AddAdministratorNoteContent(data=request.POST)
			if administrator_note_form.is_valid():
				content = AdministratorNoteContent()
				content.text = administrator_note_form.data['text']
				return (True, content, None,None)
			return (False, None, None,None)
		if (content_type == 'Assessment'):
                        assessment_form = AddAssessmentContent(data=request.POST,extra=request.POST.get('extra_field_count'),objectives=base_methods.getObjectives(lesson))
                        if assessment_form.is_valid():
                                content = AssessmentContent()
				objectives = assessment_form.cleaned_data['objectives']
                                content.title = assessment_form.data['title']
				questionAnswerList = []
				allq = sortedDictValues(slicedict("question",assessment_form.data))
				user = TeacherProfile.objects.get(user=request.user)
				for question in allq:
					(key, value) = question
					attrs = key.split('_')
					if len(attrs) != 3:
						continue
					qtype = attrs[1]
					formnum = attrs[2]
					q = Question()
					q.placement = formnum
					q.question = value
					q.owner = user
					ansKey = "answer_"+qtype+"_"+formnum
					allans = slicedict(ansKey,assessment_form.data)
					allCheckedAns = slicedict("answer_cb_"+formnum,assessment_form.data)
					allCheckAnsList = []
					for a in allCheckedAns:
						allCheckAnsList.append(a.split('_')[3])
					allAnswers = []
					for akey,avalue in allans.items():
						a = Answer
						if qtype == 'fr':
							a = FreeResponseAnswer()
						elif qtype == 'mc':
							a = MultipleChoiceAnswer()
							if str(akey.split('_')[3]) in allCheckAnsList:
								a.is_checked = True;
						a.answer = avalue
	                                        a.owner = user
						allAnswers.append(a)
					questionAnswerList.append((q,allAnswers))
                                return (True, content,questionAnswerList,objectives)

			print assessment_form.errors
                        return (False, None, None,None)
	return (False, None, None,None);

@csrf_exempt
def EditCourseRequest(request):
	if request.method == 'POST':
		course_id = request.POST['course_id']
		course = Course.objects.get(id=course_id)
		editCourseForm = EditCourse(instance=course)	
		context = Context({'editCourseForm':editCourseForm, 'selectedCourse':course_id})
        	return HttpResponse(render_block_to_string('course_edit_modal.html', 'editCourse', context))
	return HttpResponse('')

@csrf_exempt
def EditUnitRequest(request):
	if request.method == 'POST':
		print "change this"
		unitID = request.POST['unit_id']
	        unit = Unit.objects.get(id=unitID)
        	editUnitForm = EditUnit(instance=unit)
		editUnitForm.fields['owner'].label=''
		editUnitForm.fields['course'].label=''
		editUnitForm.fields['parent_unit'].label=''
		editUnitForm.fields['parent_unit'].initial = None
		context = Context({'editUnitForm':editUnitForm, 'selectedUnit':unitID})
        	return HttpResponse(render_block_to_string('unit_edit_modal.html', 'editUnit', context))
	return HttpResponse('')

@csrf_exempt
def DeleteLessonRequest(request):
	if request.method == 'POST':
		lessonID = request.POST.get('lesson_id')
	        lesson = Lesson.objects.get(id=lessonID)
        	deleteLessonForm = DeleteLesson()
	        deleteLessonForm.fields["lesson_id"].initial = lesson.id
		context = Context({'deleteLessonForm':deleteLessonForm})
		return HttpResponse(render_block_to_string("lesson_delete_modal.html", 'deleteLesson', context))
	return HttpResponse('')

@csrf_exempt
def EditLessonRequest(request):
	if request.method == 'POST':
		lessonID = request.POST.get('lesson_id')
        	lesson = Lesson.objects.get(id=lessonID)
		editLessonForm = EditLesson(instance=lesson)
		editLessonForm.fields['owner'].label=''
		editLessonForm.fields['unit'].label=''
		context = Context({'editLessonForm':editLessonForm, 'selectedLesson':lessonID})
		return HttpResponse(render_block_to_string('lesson_edit_modal.html', 'editLesson', context))
	return HttpResponse('')

def EditContentRequest(request, contentID):
        uname = request.user.username
        user = UserProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        content = Content.objects.get(id=contentID)
	lesson = content.lesson
        unit = lesson.unit
        unit_lessons =  Lesson.objects.filter(unit=lesson.unit)
        editLessonForm = EditContent()
        editLessonForm.fields["lesson_id"].initial = lesson.id
        editLessonForm.fields["unit_id"].initial = unit.id
        editLessonForm.fields["name"].initial = lesson.name
        return render(request,'lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname,'userLessons':unit_lessons, 'fullname':uname, 'editLessonForm':editLessonForm,'showEditLesson': 1})


def deleteCourseData(course_id):
	if course_id:
       		Course.objects.get(id=course_id).delete()
                return True;
        return False;

def deleteUnitData(unit_id):
	if unit_id:
		Unit.objects.get(id=unit_id).delete()
		return True
	return False

def deleteLessonData(lessonForm, request_user):
        if 'lesson_id' in lessonForm.data:
                Lesson.objects.get(id=lessonForm.data['lesson_id']).delete()
                return True;
        return False;

@csrf_exempt
def manageStudents(request):
	base_dict = base_methods.createBaseDict(request)
	#get courses with students
	course_students = {}
	for course in base_dict['userCourses']:
		cs_list = CourseStudents.objects.filter(course=course)
		
		student_list = [cs for cs in cs_list]
		for s in student_list:
			course_students[course] = student_list
	base_dict['courseStudents'] = course_students
	return render(request,'manage_students.html', base_dict)

@csrf_exempt
def studentRequestCourse(request):
	base_dict = base_methods.createStudentDict(request)
	teacher_request = TeacherRequestForm(data=request.POST)
	if teacher_request.is_valid():
		generic_user = User.objects.get(email=teacher_request.data['email'])
		teacher = TeacherProfile.objects.get(user=generic_user)
		course_request = CourseRequestForm()
		courses = Course.objects.filter(owner=teacher)
		course_list = []
		for course in courses:
			course_list.append((course.id, course.name))
		course_request.fields['courses'].choices = course_list
		course_request.fields['teacher_id'].initial = teacher.id
		base_dict['teacherCoursesRequestForm'] = course_request
		base_dict['coursesWereRequested'] = True
		return render(request,'student_course.html', base_dict)
	else:
		return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def studentAddCourse(request):
	courseRequestForm = CourseRequestForm(data=request.POST)
	teacher_id = courseRequestForm.data['teacher_id']
	try:
		teacher = TeacherProfile.objects.get(id=teacher_id)
		student = StudentProfile.objects.get(user=request.user)
	except:
		return HttpResponseRedirect('/studentCourses/')
	courses = Course.objects.filter(owner=teacher)
	course_list = []
	for course in courses:
		course_list.append((course.id, course.name))
	courseRequestForm.fields['courses'].choices = course_list
	if courseRequestForm.is_valid():
		try:
			teacher = TeacherProfile.objects.get(id=courseRequestForm.data['teacher_id'])
			for course_id in courseRequestForm.cleaned_data['courses']:
				course = Course.objects.get(owner=teacher, id=course_id)
				cs_exists = CourseStudents.objects.filter(student=student, course=course)
				if cs_exists and len(cs_exists) > 0:
					return HttpResponseRedirect('/studentCourses/')
				cs = CourseStudents()
				cs.course = course
				cs.student = student
				cs.approved = False
				cs.save()
				return HttpResponseRedirect('/studentCourses/')
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
	else:	
		print courseRequestForm.errors
		return HttpResponseRedirect(lastPageToRedirect(request))

def studentShowCourses(request):
	base_dict = base_methods.createStudentDict(request)
	if base_dict == None:
		return HttpResponseRedirect('/courses/')
	request.session['last_page'] = 'studentCourses'
	return render(request,'student_course.html', base_dict)


def deleteSectionData(sectionForm, request_user):
	if 'section_id' in sectionForm.data:
		Section.objects.get(id=sectionForm.data['section_id']).delete()
		return True
	return False

def deleteContentData(contentForm, request_user):
	if 'content_id' in contentForm.data:
		Content.objects.get(id=contentForm.data['content_id']).delete()
		return True
	return False

@csrf_exempt
def getStandardsFromGroup(request):
	if request.method == 'POST':
		group_id = request.POST['group_id']
		try:
			group = StandardGrouping.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/courses/')
		base_dict = base_methods.createBaseDict(request)
		standard_list = []
		for standard in group.standard.all():
			standard_list.append(standard)
		base_dict['groupStandards'] = standard_list
		base_dict['showGroupStandards'] = True
		base_dict['selectedGroup'] = group
		base_dict['user_id'] = request.user.id
		return render(request,'course.html', base_dict)
	return HttpResponseRedirect('/courses/')

@csrf_exempt
def standardsSearch(request):
	base_dict = base_methods.createBaseDict(request)
	base_dict['standardsSearchForm'] = StandardsSearchForm()
	if request.method == 'POST':
		standards = []
		form = StandardsSearchForm(data=request.POST)
		if form.is_valid():
			has_state = False
			g = form.cleaned_data['grade']
			grade = Grade.objects.get(value=g)
			subject = Subject.objects.get(value=form.cleaned_data['subject'])
			standard_type = StandardType.objects.get(value=form.cleaned_data['standard_type'])
			qset = Standard.objects.filter(subject=subject,grade=grade,standard_type=standard_type)
			if ( form.cleaned_data['standard_type'] == 'State'):
				state = State.objects.get(value=form.cleaned_data['state'])
				qset.filter(state=state)
			for standard in qset:
				if standard.state != None:
					has_state=True
				standards.append(standard)
						
			standards.sort(key=lambda x: (int(x.numbering) if x.numbering.isdigit() else x.numbering))
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

@csrf_exempt
def manageCourseStudents(request):
	if request.method == 'POST':
		cid = request.POST['course_id']
		try:
			course = Course.objects.get(id=cid)
		except:
			return HttpResponseRedirect('/courses/')
		students = request.POST.getlist('students')
		for sid in students:
			try:
				user = User.objects.get(id=sid)
				s = StudentProfile.objects.get(user=user)
				cs = CourseStudents.objects.get(course=course, student=s)
				cs.approved=True
				cs.save()
			except:
				continue	
		return HttpResponseRedirect('/manageStudents/')
	else:
		return HttpResponseRedirect('/manageStudents/')

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
		saf = StandardAnalysisForm()
		saf.fields['standard_id'].initial = s.id
		base_dict['standardAnalysisForm'] = saf
		base_dict['ratingOptions'] = (1,2,3,4,5)
		base_dict['user_id'] = request.user.id
		return render(request,'standard_view.html', base_dict)

	return HttpResponseRedirect('/courses/')

def publicCourseView(request):
	base_dict = base_methods.createBaseDict(request)
	course_id = request.GET['course_id']
	course = Course.objects.get(id=course_id)
	course_delta = (course.end_date - course.start_date)
	base_dict['course_length']=(course_delta.days/7, course_delta.days%7)
	course_units = Unit.objects.filter(course=course).order_by('start_date')
	course_unit_list = []
	for unit in course_units:
		ratings = UnitRating.objects.filter(unit=unit)
		rating_list = [rating.rating for rating in ratings]
		rating = 0
		if ( len(rating_list) > 0):
			rating = reduce(lambda x, y: x+y, rating_list)/float(len(rating_list))
		course_unit_list.append((unit, rating))
	
	course_standards = []
	for sg in course.standard_grouping.all():
		for standard in sg.standard.all():
			course_standards.append(standard)
	base_dict['courseStandards'] = 	course_standards
	base_dict['courseUnits'] = course_unit_list
	return render(request,'public_course_view.html',base_dict)

@csrf_exempt
def addStandardAnalysis(request):
	if request.method == 'POST':
		form = StandardAnalysisForm(data=request.POST)
		if form.is_valid():
			standard_id = form.cleaned_data['standard_id']
			try:
				standard = Standard.objects.get(id=standard_id)
				teacher = TeacherProfile.objects.get(user=request.user)
			except:
				print 'error in addStandardAnalysis'
				return HttpResponseRedirect('/standard/?standard_id='+str(standard_id))
			text = form.cleaned_data['analysis']
			sa, created = StandardAnalysis.objects.get_or_create(teacher=teacher,standard=standard)
			sa.analysis = text
			sa.number_raters=0
			sa.save()

	return HttpResponseRedirect('/standard/?standard_id='+str(standard_id))
		

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
	unit_standards = []
	for standard in unit.standards.all():
		unit_standards.append(standard)
	base_dict['unitStandards'] = unit_standards
	base_dict['unitLessons'] = unit_lesson_list
	return render(request,'public_unit_view.html',base_dict)

@csrf_exempt
def rateAnalysis(request):
	if request.method == 'POST':
		print request.POST
		try:
			user = User.objects.get(id=request.POST['user_id'])
			teacher = TeacherProfile.objects.get(user=user)
			sa = StandardAnalysis.objects.get(id = request.POST['id'])
			sar, created = StandardAnalysisRating.objects.get_or_create(standard_analysis=sa, rater=teacher, rating_type='All')
		except:
			print traceback.format_exception(*sys.exc_info())
			return HttpResponseRedirect('/standard/?standard_id='+str(sa.id))
		new_rating =  int(request.POST['rating'])
		try:
			if created:
				sar.rating = new_rating
				sar.save()
				sa.cumulative_rating = (sa.cumulative_rating*sa.number_raters + sar.rating)/(sa.number_raters+1)
				sa.number_raters+=1
				sa.save()
			elif (sar.rating != new_rating):
				sa.cumulative_rating = (sa.cumulative_rating*sa.number_raters - sar.rating + new_rating)/sa.number_raters
				sar.rating = new_rating
				sar.save()
				sa.save()
		except:
			print traceback.format_exception(*sys.exc_info())
			
		return HttpResponse(str(sa.cumulative_rating))
		
