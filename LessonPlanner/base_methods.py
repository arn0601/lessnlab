
from django.core.exceptions import *
from django.template import RequestContext
from LessonPlanner.models import Lesson
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Standards.models import Standard
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile, StudentProfile
import simplejson

def getStandardsList(course, user):
	print course.department, user.user_school_state
	slist = Standard.objects.filter(department=course.department, owner_type=user.user_school_state)
	s_choices = [(s.id, s.description) for s in slist]
	return s_choices	


def createBaseDict(request):
	(courseAddForm, unitAddForm,lessonAddForm,sectionAddForm) = returnBlankForms()
	try:
		user = TeacherProfile.objects.get(user=request.user)
        	courseAddForm.fields['owner'].initial = user
        	unitAddForm.fields['owner'].initial = user
        	lessonAddForm.fields['owner'].initial = user
	except TeacherProfile.DoesNotExist:
		user = StudentProfile.objects.get(user=request.user)
	#get all courses associated with the user
	user_courses =  Course.objects.filter(owner=user)
	
	lesson = None	
	
	#####################################
	#get the lesson
	###################################
	lesson_id = request.GET.get('lesson_id')
	if ( not lesson_id == None ):
		lesson = Lesson.objects.get(id=lesson_id)
		lessonAddForm.fields['unit'].initial = lesson.unit
                unitAddForm.fields['course'].initial = lesson.unit.course
		sectionAddForm.fields['lesson'].initial = lesson
	#####################################
	#get the unit
	####################################

	unit = None
	user_lessons = None

	#if we have lesson, get unit:
	if ( lesson ):
		unit = lesson.unit
	
	#get unit id
	unit_id = request.GET.get('unit_id')
	if ( not unit_id == None ):
		unit = Unit.objects.get(id=unit_id)
		lessonAddForm.fields['unit'].initial = unit
		unitAddForm.fields['course'].initial = unit.course
	##########################################
	#get the course
	##############################################	

	course = None
	user_units = None
	standards_list = []
	
	#if we have a unit get a course, and get the lesson for the unit
	if ( unit ):
		user_lessons = Lesson.objects.filter(unit=unit)
		course = unit.course

	#get the course id and course
	course_id = request.GET.get('course_id')
	if ( not course_id == None ):
		course = Course.objects.get(id=course_id)
		unitAddForm.fields['course'].initial = course
	
	#check course
	if ( course ):
        	user_units =  Unit.objects.filter(course=course)
                standards_list = getStandardsList(course, user)
	
	uname = request.user.username

	unitAddForm.fields['standards'].choices = standards_list
	
	#return (stuff for function, stuff to render)
	return {'course': course, 'unit': unit, 'lesson': lesson, 'userCourses': user_courses, 'userUnits':user_units, 'userLessons': user_lessons, 'username': uname, 'fullname': uname, 'courseAddForm':courseAddForm, 'unitAddForm':unitAddForm, 'lessonAddForm':lessonAddForm, 'standardlist':standards_list, 'sectionAddForm':sectionAddForm}

<<<<<<< HEAD
def getLessonSpecificInfo(lesson):
	lesson_sections = Section.objects.filter(lesson=lesson)
	section_dict = {}
	assessment_dict = {}
	add_content_form_dict = {}
	for section in lesson_sections:
		content_list = []
		section_content = Content.objects.filter(section=section)
		for content in section_content:
			if (content.content_type == 'Text'):
				content_list.append(content.textcontent)
			elif (content.content_type == 'OnlineVideo'):
				content_list.append(content.onlinevideocontent)
			elif (content.content_type == 'OnlineArticle'):
				content_list.append(content.onlinearticlecontent)
			elif (content.content_type == 'OnlinePicture'):
                                content_list.append(content.onlinepicturecontent)
			elif (content.content_type == 'TeacherNote'):
				content_list.append(content.teachernotecontent)
			elif (content.content_type == 'AdministratorNote'):
				content_list.append(content.administratornotecontent)
 			elif (content.content_type == 'Assessment'):
                                content_list.append(content.assessmentcontent)
				questions = Question.objects.filter(assessment = content.assessmentcontent)
				question_answer_map = {}
				for q in questions:
					a = FreeResponseAnswer.objects.get(question = q)
					question_answer_map[q] = a
				assessment_dict[content.assessmentcontent.id] = question_answer_map
		section_dict[section] = content_list
	add_content_form_dict = getAddContentForms(str(-1))
	print section_dict
	return { 'sections' : section_dict,  'assessment_dict':assessment_dict, 'section_content_forms': add_content_form_dict, 'dropdown_order': LESSONPLANNER_DROPDOWN_ORDER, 'section_types' : getSectionMapping() }

=======
>>>>>>> c04a1f1dc29d19b317d11900ddb99b2498496c2f
def getAddContentForms(section_id):
	
	content_form_dict = {'General': {} , 'Media': {}, 'Activity': {}, 'Checks For Understanding': {}, 'Assessment': {} }
	
	online_video_form = AddOnlineVideoContent()
	online_video_form.fields['content_type'].initial = 'OnlineVideo'
	online_video_form.fields['section_id'].initial = section_id
	content_form_dict['Media']["OnlineVideo"] = online_video_form
	
	online_picture_form = AddOnlinePictureContent()
	online_picture_form.fields['content_type'].initial = 'OnlinePicture'
	online_picture_form.fields['section_id'].initial = section_id
	content_form_dict['Media']["OnlinePicture"] = online_picture_form
	
	online_article_form = AddOnlineArticleContent()
	online_article_form.fields['content_type'].initial = 'OnlineArticle'
	online_article_form.fields['section_id'].initial = section_id
	content_form_dict['Media']['OnlineArticle'] = online_article_form
	
	text_form = AddTextContent()
	text_form.fields['content_type'].initial = 'Text'
	text_form.fields['section_id'].initial = section_id
	content_form_dict['General']['Text'] = text_form
	
	teacher_note = AddTeacherNoteContent()
	teacher_note.fields['content_type'].initial = 'TeacherNote'
	teacher_note.fields['section_id'].initial = section_id
	content_form_dict['General']['TeacherNote'] = teacher_note
	
	administrator_note = AddAdministratorNoteContent()
	administrator_note.fields['content_type'].initial = 'AdministratorNote'
	administrator_note.fields['section_id'].initial = section_id
	content_form_dict['General']['AdministratorNote'] = administrator_note

	assessment_form = AddAssessmentContent()
        assessment_form.fields['content_type'].initial = 'Assessment'
        assessment_form.fields['section_id'].initial = section_id
        content_form_dict['Assessment']['Assessment'] = assessment_form

	return content_form_dict

def getLessonSpecificInfo(lesson):
	lesson_sections = Section.objects.filter(lesson=lesson)
	section_dict = {}
	add_content_form_dict = {}
	for section in lesson_sections:
		content_list = []
		section_content = Content.objects.filter(section=section)
		for content in section_content:
			if (content.content_type == 'Text'):
				content_list.append(content.textcontent)
			elif (content.content_type == 'OnlineVideo'):
				content_list.append(content.onlinevideocontent)
			elif (content.content_type == 'OnlineArticle'):
				content_list.append(content.onlinearticlecontent)
			elif (content.content_type == 'OnlinePicture'):
                                content_list.append(content.onlinepicturecontent)
			elif (content.content_type == 'TeacherNote'):
				content_list.append(content.teachernotecontent)
			elif (content.content_type == 'AdministratorNote'):
				content_list.append(content.administratornotecontent)
 			elif (content.content_type == 'Assessment'):
                                content_list.append(content.assessmentcontent)

		section_dict[section] = content_list
	print "HEY",section_dict
	add_content_form_dict = getAddContentForms(str(-1))
	return { 'sections' : section_dict, 'section_content_forms': add_content_form_dict, 'dropdown_order': LESSONPLANNER_DROPDOWN_ORDER, 'section_types' : getSectionMapping() }

def getSectionMapping():
	section_mapping = {}
	for sec in SECTIONTYPE:
		section_mapping[sec[0]] = sec[1]
	return section_mapping

	
def returnBlankForms():
	addCourseForm = AddCourse()
	addCourseForm.fields['owner'].label=''
	addUnitForm = AddUnitForm()
	addUnitForm.fields['owner'].label=''
	addUnitForm.fields['course'].label=''
	addUnitForm.fields['parent_unit'].label=''
	addUnitForm.fields['parent_unit'].initial = None
	addUnitForm.fields['standards'].initial = None
	addLessonForm = AddLessonForm()
	addLessonForm.fields['unit'].label=''
	addLessonForm.fields['owner'].label=''
	addSectionForm = AddSectionForm()
	addSectionForm.fields['lesson'].label=''
	addSectionForm.fields['placement'].label=''
	addSectionForm.fields['creation_date'].label=''
	return (addCourseForm, addUnitForm , addLessonForm, addSectionForm)
