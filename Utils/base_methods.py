from Courses import course_methods
from django.core.exceptions import *
from django.template import RequestContext
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Lessons.models import Lesson
from Lessons.forms import *
from Courses.models import Course
from Courses.forms import *
from Units.models import Unit
from Units.forms import *
from Standards.models import Standard
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile, StudentProfile, UserProfile
import simplejson
from Classes.models import Class, ClassStudents
from Classes.forms import TeacherRequestForm
from django.contrib.auth import logout
from datetime import datetime

def returnStudentForms():
	teacherRequestForm = TeacherRequestForm()
	return (teacherRequestForm)

def checkUserType(request):
	try:
		user = UserProfile.objects.get(user=request.user)
		return user.user_type
	except:
		return None

def checkUserIsStudent(request):
	if checkUserType(request) == 'Student':
		user = StudentProfile.objects.get(user=request.user)
		return user
	else:
		logout(request)
		return None

def createStudentDict(request):
	(teacherRequestForm) = returnStudentForms()
	user = checkUserIsStudent(request)
	if not user:
		return None
	#get all courses associated with the user
	classes = [c.course_class for c in ClassStudents.objects.filter(student=user, approved=True)]
	now = datetime.today()
	
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
	class_ = None
	user_units = None
	#if we have a unit get a course, and get the lesson for the unit
	if ( unit ):
		user_lessons = Lesson.objects.filter(unit=unit).filter(start_date__lt=now)

	#get the course id and course
	class_id = request.GET.get('class_id')
	if ( not class_id == None ):
		class_ = Class.objects.get(id=class_id)
	
	#check course
	if ( class_ ):
        	user_units =  Unit.objects.filter(course=class_.course).filter(start_date__lt=now)
		try:
			allowed = ClassStudents.objects.get(course_class=class_, student=user, approved=True)
		except:
			print 'Student not allowed to access course'
			return None
	
	uname = request.user.username

	#return (stuff for function, stuff to render)
	return {'user' : user, 'class_': class_, 'unit': unit, 'lesson': lesson, 'userClasses': classes, 'userUnits':user_units, 'userLessons': user_lessons, 'fullname': uname, 'teacherRequestForm': teacherRequestForm, 'coursesWereRequested': 0}

def checkUserIsTeacher(request):
	if checkUserType(request) == 'Teacher':
		user = TeacherProfile.objects.get(user=request.user)
		return user
	else:
		logout(request)
		return None

def createBaseDict(request):

	#initialize an empty base dict, as we create things, we should add them to the dictionary
	base_dict = {}

	(courseAddForm, unitAddForm,lessonAddForm,sectionAddForm, courseParametersForm) = returnBlankForms()
	user = checkUserIsTeacher(request)
	if not user:
		logout(request)
		return None

	base_dict['user'] = user

	courseAddForm.fields['state'].initial = user.user_school_state

       	courseAddForm.fields['owner'].initial = user
       	unitAddForm.fields['owner'].initial = user
       	lessonAddForm.fields['owner'].initial = user

	base_dict['courseAddForm'] = courseAddForm
	base_dict['unitAddForm'] = unitAddForm
	base_dict['lessonAddForm'] = lessonAddForm
	base_dict['sectionAddForm'] = sectionAddForm
	courseParametersForm.fields['state'].initial = user.user_school_state
	base_dict['recommendCourseParametersForm'] = courseParametersForm

	#get all courses associated with the user
	user_courses =  Course.objects.filter(owner=user)

	base_dict['userCourses'] = user_courses	

	lesson = None	
	
	#####################################
	#get the lesson
	###################################
	lesson_id = request.GET.get('lesson_id')

	if ( not lesson_id == None ):
		lesson = Lesson.objects.get(id=lesson_id)
		if lesson.owner == user:
			lessonAddForm.fields['unit'].initial = lesson.unit
        	        unitAddForm.fields['course'].initial = lesson.unit.course
			sectionAddForm.fields['lesson'].initial = lesson
		else:
			lesson = None

	base_dict['lesson'] = lesson

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
		if unit.owner == user:
			lessonAddForm.fields['unit'].initial = unit
			unitAddForm.fields['course'].initial = unit.course
		else:
			unit = None

	base_dict['unit'] = unit

	class_ = None
	class_id = request.GET.get('class_id')
	if ( not class_id == None ):
		try:
			class_ = Class.objects.get(id=class_id)
		except:
			class_ = None

	base_dict['class_'] = class_

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

	base_dict['userLessons'] = user_lessons

	if ( class_):
		course = class_.course;

	#get the course id and course
	course_id = request.GET.get('course_id')
	if ( not course_id == None ):
		course = Course.objects.get(id=course_id)
		base_dict.update(course_methods.getCourseInfo(course))
		if (course.owner == user):
			unitAddForm.fields['course'].initial = course
		else:
			course = None

	user_classes = None
	#check course
	if ( course ):
        	user_units =  Unit.objects.filter(course=course)
		user_classes = Class.objects.filter(course=course)

	base_dict['course'] = course
	base_dict['userUnits'] = user_units
	base_dict['userClasses'] = user_classes

	uname = request.user.username
	fullname = user.user_firstname + " " + user.user_lastname

	base_dict['username'] = uname
	base_dict['fullname'] = fullname	

	#return (stuff for function, stuff to render)
	return base_dict
	

def getObjectives(lesson):
	objective_list = []
	for objective in Objective.objects.filter(lesson=lesson):
                objective_list.append((objective.id, objective.description))
	return objective_list

def getStandards(lesson):
	standard_list = []
	for standard in lesson.standards.all():
                standard_list.append((standard.id, standard.description))
	return standard_list

def getLessonSpecificInfo(lesson):
	lesson_sections = Section.objects.filter(lesson=lesson)
	section_dict = {}
	assessment_dict = {}
	add_content_form_dict = {}
	standard_list = getStandards(lesson)
	objective_list = getObjectives(lesson)
	content_objs = {}
	for section in lesson_sections:
		content_list = []
		section_content = Content.objects.filter(section=section)
		for content in section_content:
			content_objs_m2m = content.objectives.all()
			contentobjs_list = []
			for c_o in content_objs_m2m:
				contentobjs_list.append((c_o.id, c_o.description))
			content_objs[content.id] = contentobjs_list
			if (content.content_typename == 'Assessment'):
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
			else:
				content_list.append(content.as_leaf_class())
		section_dict[section] = content_list
	add_content_form_dict = getAddContentForms(str(-1), objective_list)
	return { 'content_objs' : content_objs, 'standard_list' : standard_list,'objective_list' : objective_list,'sections' : section_dict,  'assessment_dict':assessment_dict, 'content_choices':getContentChoices(),  'section_content_forms': add_content_form_dict, 'dropdown_order': LESSONPLANNER_DROPDOWN_ORDER, 'section_types' : getSectionMapping() }

def getContentChoices():
	return {'General': [("Text","Text")], 'Media': [("PowerPoint","PowerPoint"),("Online Picture","OnlinePicture"),("Online Article","OnlineArticle"),("Online Video","OnlineVideo"),("Teacher Note","TeacherNote"),("Administrator Note","AdministratorNote")], 'Activity': [("Activity","Activity")], 'Checks for Understanding': [("Checks for Understanding","CFU")], 'Assessment': [("Assessment","Assessment")] }
	

def getAddContentForms(section_id, objective_list):
	
	content_form_dict = {'General': {} , 'Media': {}, 'Activity': {}, 'CFU': {}, 'Assessment': {} }
	
	online_video_form = AddOnlineVideoContent()
	online_video_form.fields['content_type'].initial = 'OnlineVideo'
	online_video_form.fields['section_id'].initial = section_id
	content_form_dict['Media']["OnlineVideo"] = ("Online Video",online_video_form)
	
	power_point_form = AddPowerPointContent()
	power_point_form.fields['content_type'].initial = 'PowerPoint'
	power_point_form.fields['section_id'].initial = section_id
	content_form_dict['Media']["PowerPoint"] = ("PowerPoint",power_point_form)
	
	online_picture_form = AddOnlinePictureContent()
	online_picture_form.fields['content_type'].initial = 'OnlinePicture'
	online_picture_form.fields['section_id'].initial = section_id
	content_form_dict['Media']["OnlinePicture"] = ("Online Picture",online_picture_form)
	
	online_article_form = AddOnlineArticleContent()
	online_article_form.fields['content_type'].initial = 'OnlineArticle'
	online_article_form.fields['section_id'].initial = section_id
	content_form_dict['Media']['OnlineArticle'] = ("Online Article",online_article_form)
	
	text_form = AddTextContent()
	text_form.fields['content_type'].initial = 'Text'
	text_form.fields['section_id'].initial = section_id
	content_form_dict['General']['Text'] = ("Text",text_form)
	
	teacher_note = AddTeacherNoteContent()
	teacher_note.fields['content_type'].initial = 'TeacherNote'
	teacher_note.fields['section_id'].initial = section_id
	content_form_dict['General']['TeacherNote'] = ("Teacher Note",teacher_note)
	
	cfu = AddCFUContent(objectives=objective_list)
	cfu.fields['content_type'].initial = 'CFU'
	cfu.fields['section_id'].initial = section_id
	content_form_dict['CFU']['CFU'] = ("Check for Understanding",cfu)
	
	administrator_note = AddAdministratorNoteContent()
	administrator_note.fields['content_type'].initial = 'AdministratorNote'
	administrator_note.fields['section_id'].initial = section_id
	content_form_dict['General']['AdministratorNote'] = ("Administrator Note",administrator_note)

	assessment_form = AddAssessmentContent(objectives=objective_list)
	assessment_form.fields['content_type'].initial = 'Assessment'
	assessment_form.fields['section_id'].initial = section_id
	content_form_dict['Assessment']['Assessment'] = ("Assessement",assessment_form)

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
	courseParametersForm = RecommendCourseParametersForm()
	return (addCourseForm, addUnitForm , addLessonForm, addSectionForm, courseParametersForm)
