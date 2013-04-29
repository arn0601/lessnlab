
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
from django.contrib.auth import logout

def returnStudentForms():
	teacherRequestForm = TeacherRequestForm()
	return (teacherRequestForm)

def createStudentDict(request):
	(teacherRequestForm) = returnStudentForms()
	try:
		print request.user
		user = StudentProfile.objects.get(user=request.user)
        except:
		print 'Student Does No Exist for ' + str(request.user.id)
		try:
			user = TeacherProfile.objects.get(user=request.user)
			return None
		except: 
			logout(request)
			return None
	#get all courses associated with the user
	courses = CourseStudents.objects.filter(student=user, approved=True)
	
	###################################
	#get the lesson
	###################################
	lesson = None
	lesson_id = request.GET.get('lesson_id')
	if ( not lesson_id == None ):
		lesson = Lesson.objects.get(id=lesson_id)

	####################################
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
	##########################################
	#get the course
	##############################################	
	course = None
	user_units = None
	#if we have a unit get a course, and get the lesson for the unit
	if ( unit ):
		user_lessons = Lesson.objects.filter(unit=unit)
		course = unit.course

	#get the course id and course
	course_id = request.GET.get('course_id')
	if ( not course_id == None ):
		course = Course.objects.get(id=course_id)
	
	#check course
	if ( course ):
        	user_units =  Unit.objects.filter(course=course)
		try:
			allowed = CourseStudents.objects.get(course=course, student=user, allowed=True)
		except:
			print 'Student not allowed to access course'
			return HttpResponseRedirect('/studentCourses/');
	
	uname = request.user.username

	#return (stuff for function, stuff to render)
	return {'course': course, 'unit': unit, 'lesson': lesson, 'userCourses': courses, 'userUnits':user_units, 'userLessons': user_lessons, 'username': uname, 'fullname': uname, 'teacherRequestForm': teacherRequestForm, 'coursesWereRequested': 0}

def createBaseDict(request):
	(courseAddForm, unitAddForm,lessonAddForm,sectionAddForm) = returnBlankForms()
	try:
		user = TeacherProfile.objects.get(user=request.user)
        	courseAddForm.fields['owner'].initial = user
        	unitAddForm.fields['owner'].initial = user
        	lessonAddForm.fields['owner'].initial = user
	except TeacherProfile.DoesNotExist:
		try:
			user = StudentProfile.objects.get(user=request.user)
			return None
		except:
			logout(request)
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
	
	uname = request.user.username
	firstname = user.user_firstname
	lastname = user.user_lastname
	fullname = firstname + " " + lastname
	
	#return (stuff for function, stuff to render)
	return {'course': course, 'unit': unit, 'lesson': lesson, 'userCourses': user_courses, 'userUnits':user_units, 'userLessons': user_lessons, 'username': uname, 'fullname': fullname, 'courseAddForm':courseAddForm, 'unitAddForm':unitAddForm, 'lessonAddForm':lessonAddForm, 'sectionAddForm':sectionAddForm}
	

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
					question_answer_map[q] = []
					frans = [FreeResponseAnswer.objects.filter(question = q)]
					question_answer_map[q]=frans
					mcans = [MultipleChoiceAnswer.objects.filter(question = q)]
					question_answer_map[q]+=mcans
				assessment_dict[content.assessmentcontent.id] = question_answer_map
		section_dict[section] = content_list
	add_content_form_dict = getAddContentForms(str(-1))
	return { 'sections' : section_dict,  'assessment_dict':assessment_dict, 'section_content_forms': add_content_form_dict, 'dropdown_order': LESSONPLANNER_DROPDOWN_ORDER, 'section_types' : getSectionMapping() }

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
	addLessonForm = AddLessonForm()
	addLessonForm.fields['unit'].label=''
	addLessonForm.fields['owner'].label=''
	addSectionForm = AddSectionForm()
	addSectionForm.fields['lesson'].label=''
	addSectionForm.fields['placement'].label=''
	addSectionForm.fields['creation_date'].label=''
	return (addCourseForm, addUnitForm , addLessonForm, addSectionForm)
