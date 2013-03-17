from django.template import RequestContext
from LessonPlanner.models import Lesson
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Standards.models import Standard
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import UserProfile
import simplejson

def getStandardsList(course, user):
	print course.department, user.user_school_state
	slist = Standard.objects.filter(department=course.department, owner_type=user.user_school_state)
	s_choices = [(s.id, s.description) for s in slist]
	return s_choices	

def createBaseDict(request):
	(courseAddForm, unitAddForm,lessonAddForm,sectionAddForm) = returnBlankForms()
	user = UserProfile.objects.get(user=request.user)

	#get all courses associated with the user
	user_courses =  Course.objects.filter(owner=user)
	
	lesson = None	
	
	#####################################
	#get the lesson
	###################################
	lesson_id = request.GET.get('lesson_id')
	if ( not lesson_id == None ):
		lesson = Lesson.objects.get(id=lesson_id)
		lessonAddForm.fields['unit_id'].initial = lesson.unit.id
                unitAddForm.fields['course_id'].initial = lesson.unit.course.id
		sectionAddForm.fields['lesson_id'].initial = lesson_id
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
		lessonAddForm.fields['unit_id'].initial = unit_id
		unitAddForm.fields['course_id'].initial = unit.course.id
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
		unitAddForm.fields['course_id'].initial = course_id
	
	#check course
	if ( course ):
        	user_units =  Unit.objects.filter(course=course)
                standards_list = getStandardsList(course, user)
	
	uname = request.user.username

	unitAddForm.fields['standards'].choices = standards_list
	
	#return (stuff for function, stuff to render)
	return {'course': course, 'unit': unit, 'lesson': lesson, 'userCourses': user_courses, 'userUnits':user_units, 'userLessons': user_lessons, 'username': uname, 'fullname': uname, 'courseAddForm':courseAddForm, 'unitAddForm':unitAddForm, 'lessonAddForm':lessonAddForm, 'standardlist':standards_list, 'sectionAddForm':sectionAddForm}

def getLessonSpecificInfo(lesson):
	lesson_sections = Section.objects.filter(lesson=lesson)
	section_dict = {}
	add_content_form_dict = {}
	for section in lesson_sections:
		content_list = []
		section_content = Content.objects.filter(section=section)
		for content in section_content:
			if (content.subtype == 'Text'):
				content_list.append(content.textcontent)
			elif (content.subtype == 'VideoLink'):
				content_list.append(content.videolinkcontent)
			elif (content.subtype == 'ArticleLink'):
				content_list.append(content.articlelinkcontent)
		section_dict[section] = content_list
	
	add_content_form_dict = getAddContentForms(str(section.id))
	return { 'sections' : section_dict, 'section_content_forms': add_content_form_dict, 'section_types' : getSectionMapping() }

def getAddContentForms(section_id):
	content_form_dict = {}
	
	online_video_form = AddOnlineVideoContent()
	online_video_form.fields['content_type'].initial = 'OnlineVideo'
	online_video_form.fields['section_id'].initial = section_id
	content_form_dict["OnlineVideo"] = online_video_form
	
	online_picture_form = AddOnlinePictureContent()
	online_picture_form.fields['content_type'].initial = 'OnlinePicture'
	online_picture_form.fields['section_id'].initial = section_id
	content_form_dict["OnlinePicture"] = online_picture_form
	
	online_article_form = AddOnlineArticleContent()
	online_article_form.fields['content_type'].initial = 'OnlineArticle'
	online_article_form.fields['section_id'].initial = section_id
	content_form_dict['OnlineArticle'] = online_article_form
	
	text_form = AddTextContent()
	text_form.fields['content_type'].initial = 'Text'
	text_form.fields['section_id'].initial = section_id
	content_form_dict['Text'] = text_form
	
	teacher_note = AddTeacherNoteContent()
	teacher_note.fields['content_type'].initial = 'TeacherNote'
	teacher_note.fields['section_id'].initial = section_id
	content_form_dict['TeacherNote'] = teacher_note
	
	administrator_note = AddAdministratorNoteContent()
	administrator_note.fields['content_type'].initial = 'AdministratorNote'
	administrator_note.fields['section_id'].initial = section_id
	content_form_dict['AdministratorNote'] = administrator_note

	print "print",content_form_dict
	return content_form_dict


def getSectionMapping():
	section_mapping = {}
	for sec in SECTIONTYPE:
		section_mapping[sec[0]] = sec[1]
	return section_mapping

	
def returnBlankForms():
	addCourseForm = AddCourse()
	addUnitForm = AddUnitForm()
	addLessonForm = AddLessonForm()
	addSectionForm = AddSectionForm()
	return (addCourseForm, addUnitForm , addLessonForm, addSectionForm)
