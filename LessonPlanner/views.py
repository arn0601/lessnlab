# Create your views here.
from django.template import RequestContext
from LessonPlanner.models import Lesson,Course,Unit,Section
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Standards.models import Standard
from Objectives.models import Objective
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile
from datetime import datetime
from django.utils.timezone import utc
import simplejson
import base_methods 
from django.contrib.auth.models import User

import urlparse

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
	user = TeacherProfile.objects.filter(user=request.user)
	request.session['last_page'] = '/units/?course_id='+str(base_dict['course'].id)
	
	if user and len(user) > 0:
		return render_to_response('unit.html', base_dict)
	else:
		return HttpResponseRedirect('/studentCourses/')

#show the lessons of a unit

@csrf_exempt
def requestUnitStandards(request):
	if request.method == 'POST':
		unit_id = request.POST['unit_id']
		try:
			unit = Unit.objects.get(id=unit_id)
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		print "here requesting unit"
		course = unit.course
		standard_list = []
		for group in course.standard_grouping.all():
			for standard in group.standard.all():
				standard_list.append((standard.id, standard.description))
		form = UnitStandardsForm()
		form.fields['standards'].choices = standard_list
		form.fields['unit_id'].initial = unit_id
		base_dict = base_methods.createBaseDict(request)
		base_dict['unitStandardsForm'] = form
		base_dict['addingUnitStandards'] = True
		return render_to_response('unit.html', base_dict)

@csrf_exempt
def addUnitStandards(request):
	print "adding unit standards"
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
        if action == "Edit":
                return EditLessonRequest(request, base_dict['lesson'].id)
        elif action == "Delete":
                return DeleteLessonRequest(request, base_dict['lesson'].id)

	request.session['last_page'] = '/lessons/?unit_id='+str(base_dict['unit'].id)
	user = TeacherProfile.objects.filter(user=request.user)
	if user and len(user) > 0:
		return render_to_response('lesson.html', base_dict)
	else:
		return HttpResponseRedirect('/studentCourses/')

#this function is used when creating objectives to select the initial standard
@csrf_exempt
def getLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		standard_list = []
		for standard in lesson.standards.all():
			standard_list.append((standard.id, standard.description))
		form = SelectStandardsForm()
		form.fields['standard'].choices = standard_list
		form.fields['lesson_id'].initial = lesson_id
		base_dict = base_methods.createBaseDict(request)
		base_dict['selectStandardsForm'] = form
		base_dict['selectingStandard'] = True
		
		return render_to_response('lesson.html', base_dict)

#this returns the form to add objectives
@csrf_exempt
def createLessonObjectives(request):
	if request.method == 'POST':
		standards_form = SelectStandardsForm(data=request.POST)
		try:
			lesson = Lesson.objects.get(id=standards_form.data['lesson_id'])
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
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
			base_dict = base_methods.createBaseDict(request)
			base_dict['createObjectivesForm'] = next_form
			base_dict['creatingObjectives'] = True
			return render_to_response('lesson.html',base_dict)
		else:
			print standards_form.errors
	return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def addLessonObjectives(request):
	print "adding lesson objectives"
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
def requestLessonStandards(request):
	if request.method == 'POST':
		lesson_id = request.POST['lesson_id']
		try:
			lesson = Lesson.objects.get(id=lesson_id)
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		
		print "here reaquesting lesson"
		unit = lesson.unit
		standard_list = []
		for standard in unit.standards.all():
			standard_list.append((standard.id, standard.description))
		form = LessonStandardsForm()
		form.fields['standards'].choices = standard_list
		form.fields['lesson_id'].initial = lesson_id
		base_dict = base_methods.createBaseDict(request)
		base_dict['lessonStandardsForm'] = form
		base_dict['addingLessonStandards'] = True
		return render_to_response('lesson.html', base_dict)

@csrf_exempt
def addLessonStandards(request):
	print "adding unit standards"
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
		return HttpResponseRedirect(lastPageToRedirect(request))				
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
	if user and len(user) > 0:
		return render_to_response('lessonPlanner.html', base_dict)
	else:
		return HttpResponseRedirect('/studentCourses/')

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

	action = request.GET.get('action')
	if action == "Edit":
		return EditCourseRequest(request, base_dict['course'].id)
	elif action == "Delete":
                return DeleteCourseRequest(request, base_dict['course'].id)
	
	request.session['last_page'] = 'courses'
	
	user = TeacherProfile.objects.filter(user=request.user)
	if user and len(user) > 0:
		return render_to_response('course.html', base_dict)
	else:
		return HttpResponseRedirect('/studentCourses/')

@csrf_exempt
def addCourse(request):
	if request.method == 'POST':
		addCourseForm = AddCourse(request.POST)
		if addCourseForm.is_valid():
			course = addCourseForm.save()
			teacher = TeacherProfile.objects.get(user=request.user)
			groups_added = addCourseStandards(course, teacher)
			base_dict = base_methods.createBaseDict(request)
			base_dict['groupsAdded'] = groups_added
			base_dict['addCourseSecondStep'] = True
			return render_to_response('course.html', base_dict)
		else:
			print addCourseForm.errors
	return HttpResponseRedirect(lastPageToRedirect(request))

def addCourseStandards(course, teacher):
	groups = StandardGrouping.objects.filter(subject=course.subject).filter(grade=course.grade)
	groups_to_render = []
        groups_add = {};
	
	for group in groups:
		for standard in group.standard.all():
			print standard.owner_type, teacher.user_school_state
			if standard.owner_type == teacher.user_school_state:
				course.standard_grouping.add(group)
				break
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
                addCourseForm = DeleteCourse(data=request.POST)
                if deleteCourseData(addCourseForm,request.user):
                        return HttpResponseRedirect(lastPageToRedirect(request))
        return HttpResponseRedirect(lastPageToRedirect(request))

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
                unitForm = DeleteUnit(data=request.POST)
                if deleteUnitData(unitForm,request.user):
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
			print lesson.id
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
		if content_type == "OnlineVideo":
			print "ONLINE VIDEO"
			success = saveVideoContent(contentForm, request)
			if success:
				return HttpResponseRedirect(lastPageToRedirect(request))
		        return HttpResponseRedirect(lastPageToView(request))
                (success, content, fields) =  saveContent(contentForm, request)
		if success:
			section = Section.objects.get(id=int(contentForm.data['section_id']))
			content.section = section
			content.creation_date=datetime.now()
			content.content_type = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
			content.save()
			if fields != None:
				for q,a in fields.items():
					q.assessment = content
					q.save()
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
			print content.link
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


def saveContent(contentForm, request):
	if contentForm.is_valid():
		content_type = contentForm.data['content_type']
		if (content_type == 'OnlinePicture'):
			online_picture_form = AddOnlinePictureContent(data=request.POST)
			if online_picture_form.is_valid():
				content = OnlinePictureContent()
				content.link = online_picture_form.data['link']
				return (True, content, None)
			return (False, None, None)
		if (content_type == 'OnlineArticle'):
			online_article_form = AddOnlineArticleContent(data=request.POST)
			if online_article_form.is_valid():
				content = OnlineArticleContent()
				content.link = online_article_form.data['link']
				return (True, content, None)
			return (False, None, None)
		if (content_type == 'Text'):
			text_form = AddTextContent(data=request.POST)
			if text_form.is_valid():
				content = TextContent()
				content.text = text_form.data['text']
				return (True, content, None)
			return (False, None, None)
		if (content_type == 'TeacherNote'):
			teacher_note_form = AddTeacherNoteContent(data=request.POST)
			if teacher_note_form.is_valid():
				content = TeacherNoteContent()
				content.text = teacher_note_form.data['text']
				return (True, content, None)
			return (False, None, None)
		if (content_type == 'AdministratorNote'):
			administrator_note_form = AddAdministratorNoteContent(data=request.POST)
			if administrator_note_form.is_valid():
				content = AdministratorNoteContent()
				content.text = administrator_note_form.data['text']
				return (True, content, None)
			return (False, None, None)
		if (content_type == 'Assessment'):
                        assessment_form = AddAssessmentContent(data=request.POST,extra=request.POST.get('extra_field_count'))
                        if assessment_form.is_valid():
                                content = AssessmentContent()
                                content.title = assessment_form.data['title']
				fields = assessment_form.data['extra_field_count']
				questionAnswerMap = {}
				for index in range(0,int(fields),2):
					qData = assessment_form.data['extra_field_{index}'.format(index=index)]
					aData = assessment_form.data['extra_field_{index}'.format(index=index+1)]
					user = TeacherProfile.objects.get(user=request.user)
					q = Question()
					q.question = qData
					q.owner = user
					a = FreeResponseAnswer()
					a.answer = aData
					a.owner = user
					questionAnswerMap[q] = a
                                return (True, content,questionAnswerMap)
			print assessment_form.errors
                        return (False, None, None)
	return (False, None, None);

def DeleteCourseRequest(request, course_id):
        uname = request.user.username
        user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        course = Course.objects.get(id=course_id)
        deleteCourseForm = DeleteCourse()
        deleteCourseForm.fields["course_id"].initial = course.id
        return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'deleteCourseForm':deleteCourseForm,'showDeleteCourse': 1}, context_instance=RequestContext(request))


def EditCourseRequest(request, course_id):
	uname = request.user.username
	user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
	course = Course.objects.get(id=course_id)
	editCourseForm = EditCourse(instance=course)	
	return render_to_response('course.html', {'userCourses': user_courses, 'username':uname, 'fullname':uname, 'editCourseForm':editCourseForm,'showEditCourse': 1, 'selectedCourse': course_id})

def DeleteUnitRequest(request, unitID):
        uname = request.user.username
        user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        unit = Unit.objects.get(id=unitID)
        deleteUnitForm = DeleteUnit()
        deleteUnitForm.fields["unit_id"].initial = unit.id
	course_units =  Unit.objects.filter(course=unit.course)
        return render_to_response('unit.html', {'course_id':unit.course.id,'userUnits':course_units,'userCourses': user_courses, 'username':uname, 'fullname':uname, 'deleteUnitForm':deleteUnitForm,'showDeleteUnit': 1}, context_instance=RequestContext(request))


def EditUnitRequest(request, unitID):
        uname = request.user.username
        user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        unit = Unit.objects.get(id=unitID)
        editUnitForm = EditUnit(instance=unit)
	course_units =  Unit.objects.filter(course=unit.course)
        return render_to_response('unit.html', {'course_id':unit.course.id,'userUnits':course_units,'userCourses': user_courses, 'username':uname, 'fullname':uname, 'editUnitForm':editUnitForm,'showEditUnit': 1, 'selectedUnit':unitID})

def DeleteLessonRequest(request, lessonID):
        uname = request.user.username
        user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        lesson = Lesson.objects.get(id=lessonID)
        deleteLessonForm = DeleteLesson()
        deleteLessonForm.fields["lesson_id"].initial = lesson.id
	unit_lessons =  Lesson.objects.filter(unit=lesson.unit)
        return render_to_response('lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname, 'fullname':uname,'userLessons':unit_lessons, 'deleteLessonForm':deleteLessonForm,'showDeleteLesson': 1}, context_instance=RequestContext(request))


def EditLessonRequest(request, lessonID):
        uname = request.user.username
        user = TeacherProfile.objects.get(user=request.user)
        user_courses =  Course.objects.filter(owner=user)
        lesson = Lesson.objects.get(id=lessonID)
        unit = lesson.unit
	unit_lessons =  Lesson.objects.filter(unit=lesson.unit)
	editLessonForm = EditLesson(instance=lesson)
        return render_to_response('lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname,'userLessons':unit_lessons, 'fullname':uname, 'editLessonForm':editLessonForm,'showEditLesson': 1, 'selectedLesson':lessonID})

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
        return render_to_response('lesson.html', {'unitID':lesson.unit.id,'userCourses': user_courses, 'username':uname,'userLessons':unit_lessons, 'fullname':uname, 'editLessonForm':editLessonForm,'showEditLesson': 1})


def deleteCourseData(courseForm, request_user):
	if 'course_id' in courseForm.data:
       		Course.objects.get(id=courseForm.data['course_id']).delete()
                return True;
        return False;

def deleteUnitData(unitForm, request_user):
        if 'unit_id' in unitForm.data:
                Unit.objects.get(id=unitForm.data['unit_id']).delete()
                return True;
        return False;

def deleteLessonData(lessonForm, request_user):
        if 'lesson_id' in lessonForm.data:
                Lesson.objects.get(id=lessonForm.data['lesson_id']).delete()
                return True;
        return False;


def manageStudents(request):
	base_dict = base_methods.createBaseDict(request)
	#get courses with students
	course_students = {}
	for course in base_dict['userCourses']:
		cs_list = CourseStudents.objects.filter(course=course)
		
		student_list = [cs.student for cs in cs_list]
		course_students[course] = student_list
	base_dict['courseStudents'] = course_students
	print course_students
	return render_to_response('manage_students.html', base_dict)

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
		return render_to_response('student_course.html', base_dict)
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
			print teacher
			for course_id in courseRequestForm.cleaned_data['courses']:
				course = Course.objects.get(owner=teacher, id=course_id)
				print course
				cs = CourseStudents()
				cs.course = course
				cs.student = student
				cs.approved = False
				cs.save()
				print CourseStudents.objects.all()
				return HttpResponseRedirect('/studentCourses/')
		except:
			print "here again", courseRequestForm.data['teacher_id']
			return HttpResponseRedirect(lastPageToRedirect(request))
	else:	
		print courseRequestForm.errors
		return HttpResponseRedirect(lastPageToRedirect(request))

def studentShowCourses(request):
	base_dict = base_methods.createStudentDict(request)
	request.session['last_page'] = 'studentCourses'
	return render_to_response('student_course.html', base_dict)


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
		return render_to_response('course.html', base_dict)
	return HttpResponseRedirect('/courses/')

@csrf_exempt
def standardsSearch(request):
	base_dict = base_methods.createBaseDict(request)
	if request.method == 'POST':
		groups = []
		form = StandardsSearchForm(data=request.POST)
		if form.is_valid():
			qset = StandardGrouping.objects.filter(subject=form.cleaned_data['subject'])
			if form.cleaned_data['grade'] != '':
				qset = qset.filter(grade=form.cleaned_data['grade'])
			for group in qset:
				for standard in group.standard.all():
					if standard.owner_type == form.cleaned_data['state']:
						groups.append( group)
						break
			base_dict['searchedStandards'] = groups
			base_dict['returnResults'] = True
			return render_to_response('standards_search.html', base_dict)
		else:
			return HttpResponseRedirect('/standardsSearch/')
	else:
		standardsSearchForm = StandardsSearchForm()
		base_dict['standardsSearchForm'] = StandardsSearchForm()
		base_dict['searchingStandards'] = True
		return render_to_response('standards_search.html', base_dict)
