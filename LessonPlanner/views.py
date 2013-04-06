# Create your views here.
from django.template import RequestContext
from LessonPlanner.models import Lesson,Course,Unit,Section
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Standards.models import Standard
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile
from datetime import datetime
from django.utils.timezone import utc
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
	
	return render_to_response('lessonPlanner.html', base_dict)

def lastPageToView(request):
	if request.session['last_page'] == 'courses':
		return courses(request)
	elif 'units' in request.session['last_page']:
                return unit(request)
	elif 'lessons' in request.session['last_page']:
		return request.session['last_page']
	elif 'lessonPlanner' in request.session['last_page']:
		return request.session['last_page']
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
		addCourseForm = AddCourse(request.POST)
		if addCourseForm.is_valid():
			addCourseForm.save()
			return HttpResponseRedirect(lastPageToRedirect(request))
		else:
			print addCourseForm.errors
	return HttpResponseRedirect(lastPageToRedirect(request))

@csrf_exempt
def addCourseStandards(request):
	if request.method == 'POST':
		form = CourseStandardsForm(data=request.POST)
		try:
			print 'course',form.data['course_id']	
			course = Course.objects.get(id=int(form.data['course_id']))
			
			print "addingggg course"
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		groups = StandardGrouping.objects.filter(subject=course.subject).filter(grade=course.grade)
		groups_to_render = []
		for group in groups:
			for standard in group.standard.all():
				print standard.owner_type, teacher.user_school_state
				if standard.owner_type == teacher.user_school_state:
					groups_to_render.append((group.id, group.name))
					break
		form.fields['groups'].choices = groups_to_render
		if form.is_valid():
			for gid in form.data['groups']:
				group = StandardGrouping.objects.get(id=gid)
				course.standard_grouping.add(group)
		else:
			print form.errors
		return HttpResponseRedirect('/courses/')
	return HttpResponseRedirect('/courses/')

@csrf_exempt
def requestCourseStandards(request):
	print "requesting"
	if request.method == 'POST':
		course_id = request.POST['course_id']
		try:
			course = Course.objects.get(id=course_id)
			teacher = TeacherProfile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(lastPageToRedirect(request))
		groups = StandardGrouping.objects.filter(subject=course.subject).filter(grade=course.grade)
		groups_to_render = []
		for group in groups:
			for standard in group.standard.all():
				if standard.owner_type == teacher.user_school_state:
					groups_to_render.append((group.id, group.name))
					break
		base_dict = base_methods.createBaseDict(request)
		course_std_form = CourseStandardsForm()
		course_std_form.fields['course_id'].initial = str(course_id)
		course_std_form.fields['groups'].choices = groups_to_render
		base_dict['courseStandardsForm'] = course_std_form
		base_dict['addingCourseStandards'] = True
		return render_to_response('course.html', base_dict)
		

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

@csrf_exempt
def addContent(request):
    	if request.method == 'POST':
		contentForm = AddContentForm(data=request.POST)
                (success, content, fields) =  saveContent(contentForm, request)
		if success:
			section = Section.objects.get(id=int(contentForm.data['section_id']))
			content.section = section
			content.creation_date=datetime.now()
			content.content_type = contentForm.data['content_type']
			section_content = Content.objects.filter(section=section)
			content.placement = len(section_content)+1
			content.save()
			for q,a in fields.items():
				q.assessment = content
				q.save()
				a.question = q
				a.save()
                        return HttpResponseRedirect(lastPageToRedirect(request))
	return HttpResponseRedirect(lastPageToView(request))

def saveContent(contentForm, request):
	if contentForm.is_valid():
		content_type = contentForm.data['content_type']
		if (content_type == 'OnlineVideo'):
			online_video_form = AddOnlineVideoContent(data=request.POST)
			if online_video_form.is_valid():
				content = OnlineVideoContent()
				content.link = online_video_form.data['link']
				return (True, content)
			return (False, None)
		if (content_type == 'OnlinePicture'):
			online_picture_form = AddOnlinePictureContent(data=request.POST)
			if online_picture_form.is_valid():
				content = OnlinePictureContent()
				content.link = online_picture_form.data['link']
				return (True, content)
			return (False, None)
		if (content_type == 'OnlineArticle'):
			online_article_form = AddOnlineArticleContent(data=request.POST)
			if online_article_form.is_valid():
				content = OnlineArticleContent()
				content.link = online_article_form.data['link']
				return (True, content)
			return (False, None)
		if (content_type == 'Text'):
			text_form = AddTextContent(data=request.POST)
			if text_form.is_valid():
				content = TextContent()
				content.text = text_form.data['text']
				return (True, content)
			return (False, None)
		if (content_type == 'TeacherNote'):
			teacher_note_form = AddTeacherNoteContent(data=request.POST)
			if teacher_note_form.is_valid():
				content = TeacherNoteContent()
				content.text = teacher_note_form.data['text']
				return (True, content)
			return (False, None)
		if (content_type == 'AdministratorNote'):
			administrator_note_form = AddAdministratorNoteContent(data=request.POST)
			if administrator_note_form.is_valid():
				content = AdministratorNoteContent()
				content.text = administrator_note_form.data['text']
				return (True, content)
			return (False, None)
		if (content_type == 'Assessment'):
                        assessment_form = AddAssessmentContent(data=request.POST,extra=request.POST.get('extra_field_count'))
                        if assessment_form.is_valid():
                                content = AssessmentContent()
                                content.title = assessment_form.data['title']
				fields = assessment_form.data['extra_field_count']
				questionAnswerMap = {}
				print "num",fields
				for index in range(0,int(fields),2):
					print "Index",index
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
					print "Added",q,a
                                return (True, content,questionAnswerMap)
			print assessment_form.errors
                        return (False, None)
	return (False, None);

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


'''
def saveCourse(addCourseForm, request_user):
	if addCourseForm.is_valid():
		course = Course()
		if 'course_id' in addCourseForm.data:
			course = Course.objects.get(id=addCourseForm.data['course_id'])
		course.owner = TeacherProfile.objects.get(user=request_user)
		course.subject = addCourseForm.data['name']
		course.department = addCourseForm.data['department']
		course.year = str(addCourseForm.data['year'])
		course.save()
		return True;
	return False;

def saveUnit(addUnitForm, request_user):
	if addUnitForm.is_valid():
		unit = Unit()
		if 'unit_id' in addUnitForm.data:
                        unit = Unit.objects.get(id=addUnitForm.data['unit_id'])
		user = TeacherProfile.objects.get(user=request_user)
		course_id = addUnitForm.data['course_id']
                course = Course.objects.get(id=course_id)
                slist = Standard.objects.filter(department=course.department, owner_type=user.user_school_state)
                s_choices = [(s.id, s.description) for s in slist]
		addUnitForm.fields['standards'].choices = s_choices	
		unit.name = addUnitForm.data['name']
		unit.description = addUnitForm.data['description']
		unit.course = course
		unit.owner = TeacherProfile.objects.get(user=request_user)
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
			unit.standards.add(standard)
		return True
	print addUnitForm.errors
	return False

def saveLesson(addLessonForm, request_user):
        if addLessonForm.is_valid():
                lesson = Lesson()
                if 'lesson_id' in addLessonForm.data:
                        lesson = Lesson.objects.get(id=addLessonForm.data['lesson_id'])
                lesson.name = addLessonForm.data['name']
                unitID = addLessonForm.data['unit_id']
                unit = Unit.objects.get(id=unitID)
		lesson.description = addLessonForm.data['description']
                lesson.owner = TeacherProfile.objects.get(user=request_user)
		lesson.unit = unit
                lesson.save()
		return True
	print "invalid form - lesson"
        print addLessonForm.errors
        return False

def saveSection(addSectionForm, request_user):
	print "savingSection"
	if addSectionForm.is_valid():
		section = Section()
		lesson = Lesson.objects.get(id=addSectionForm.data['lesson_id'])
		otherSections = Section.objects.filter(lesson=lesson)
		size = len(otherSections)
		section.lesson=lesson
		section.placement=size+1
		section.name=addSectionForm.data['name']
		section.description = addSectionForm.data['description']
		section.creation_date = datetime.utcnow().replace(tzinfo=utc)
		section.save()
		print "Saved"
		return True
	print "invalid form - section"
	print addSectionForm.errors
	return False
'''
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
		return render_to_response('course.html', base_dict)
	return HttpResponseRedirect('/courses/')
