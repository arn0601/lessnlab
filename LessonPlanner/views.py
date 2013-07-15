# Create your views here.
from LessonPlanner.models import *
from LessonPlanner.forms import *
from Courses.models import Course
from Units.models import Unit
from Lessons.models import Lesson
from Courses import course_methods
from Units import unit_methods
from Lessons import lesson_methods
from Standards.models import *
from Objectives.models import Objective, ObjectiveRating
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from accounts.models import TeacherProfile
from accounts.forms import TeacherRegistrationForm
from datetime import datetime
from django.utils.timezone import utc
from django.utils import simplejson
from Utils import base_methods 
from Utils.ajax_helpers import direct_block_to_template, direct_json_to_template
from Utils import base_methods
from django.template import loader,Context
from django.contrib.auth.models import User
import sys, traceback
import urlparse

def lesson_presentation(request):
	base_dict = base_methods.createBaseDict(request)
	return render(request,"lesson_presentation.html", base_dict)

def activity_add(request):
	if request.method == 'POST':
                addCourseForm = AddActivityContent(data=request.POST)
		if addCourseForm.is_valid():
			addCourseForm.save()
		else:
			print addCourseForm.errors
	return HttpResponseRedirect(request.session['last_page'])

def activity_ajax_view(request):
	return_str = ""
	if request.method == 'POST':
		activity_id = request.POST.get('activity_id',-1)
		section_id = request.POST.get('section_id',-1)
		if activity_id==-1:
			placement = getMaxCount(Section.objects.get(id=section_id))+1
			activityForm = AddActivityContent(initial={'section': section_id,'placement' : placement,'content_type':"Activity"})
			context = {'activityForm': activityForm, 'activity_id':activity_id}
			return_str = direct_block_to_template(request,'ActivityViewModal.html', 'results', context)
		else:
			placement = getMaxCount(Section.objects.get(id=section_id))+1
			ac = ActivityContent.objects.get(id=activity_id)
			activityForm = AddActivityContent(instance=ac,initial={'section': section_id,'placement' : placement,'content_type':"Activity"})
			context = {'activityForm': activityForm, 'activity_id':activity_id}
			return_str = direct_block_to_template(request,'ActivityViewModal.html', 'results', context)
	
	return return_str

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
		context = {'activities_found':dataset, 'section_id' : section_id}
	# passing the template_name + block_name + context
		return_str = direct_block_to_template(request,'ActivitySearchModal.html', 'results', context)
		return return_str

def team(request):
        return render(request,'team.html', {})

def landing(request):
	teacher_registration_form = TeacherRegistrationForm()
	return render(request,'landing.html', {'teacherRegistrationForm': teacher_registration_form})

#show the units for a specific course
def changeContentPlacement(request):
	section_id = request.POST["section"]
        contentList = Content.objects.all().filter(section=section_id)
        l = []
        for con in contentList:
                l.append((con, con.placement))
        l.sort(key=lambda x: x[1])

        start=int(request.POST["start"])-1
        final=int(request.POST["final"])-1
        a1 = l[start]
        del l[start]
        l.insert(final,a1)
        counter = 0
        for con in l:
                con[0].placement = counter
                con[0].save()
                counter = counter + 1
        return HttpResponse('')

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
	return render(request,'lessonPlanner.html', base_dict)




def deleteSection(request):
	if request.method == 'POST':
		sectionForm = DeleteSection(data=request.POST)
		if deleteSectionData(sectionForm,request.user):
			return HttpResponseRedirect(request.session['last_page'])
	return HttpResponseRedirect(request.session['last_page'])

def deleteContent(request):
        if request.method == 'POST':
                contentForm = DeleteContent(data=request.POST)
                if deleteContentData(contentForm,request.user):
                        return HttpResponseRedirect(request.session['last_page'])
        return HttpResponseRedirect(request.session['last_page'])

def addSection(request):
	if request.method == 'POST':
		sectionForm = AddSectionForm(request.POST)
		section = sectionForm.save(commit=False)
		otherSections = Section.objects.filter(lesson=section.lesson)
		size = len(otherSections)
		section.placement=size+1
		section.save()
	
		sectionForm.save_m2m()
		return HttpResponseRedirect(request.session['last_page'])
	return HttpResponseRedirect(request.session['last_page'])

def getMaxCount(section):
	section_content = Content.objects.filter(section=section)
        maxCont = 0
        for c in section_content:
        	if c.placement > maxCont:
                	maxCont = c.placement
        return  maxCont+1


def addContent(request):
    	if request.method == 'POST':
		contentForm = AddContentForm(data=request.POST)
		content_type = contentForm.data['content_type']
		section = Section.objects.get(id=int(contentForm.data['section_id']))
		if content_type == "OnlineVideo":
			success = saveVideoContent(contentForm, request)
			if success:
				return HttpResponseRedirect(request.session['last_page'])
		        return HttpResponseRedirect(request.session['last_page'])
                (success, content, fields, objectives) =  saveContent(contentForm,section,section.lesson, request)
		if success:
			section = Section.objects.get(id=int(contentForm.data['section_id']))
			content.section = section
			content.creation_date=datetime.now()
			content.content_type = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
			content.save()
			if objectives:
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
                        return HttpResponseRedirect(request.session['last_page'])
	return HttpResponseRedirect(request.session['last_page'])

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
		elif (content_type == 'OnlineArticle'):
			online_article_form = AddOnlineArticleContent(data=request.POST)
			if online_article_form.is_valid():
				content = OnlineArticleContent()
				content.link = online_article_form.data['link']
				return (True, content, None,None)
			return (False, None, None,None)
		elif (content_type == 'PowerPoint'):
                        powerpoint_form = AddPowerPointContent(data=request.POST)
                        if powerpoint_form.is_valid():
                                content = PowerPointContent()
                                content.link = powerpoint_form.data['link']
                                return (True, content, None,None)
                        return (False, None, None,None)	
		elif (content_type == 'Text'):
			text_form = AddTextContent(data=request.POST)
			if text_form.is_valid():
				content = TextContent()
				content.text = text_form.data['text']
				return (True, content, None,None)
			return (False, None, None,None)
		elif (content_type == 'TeacherNote'):
			teacher_note_form = AddTeacherNoteContent(data=request.POST)
			if teacher_note_form.is_valid():
				content = TeacherNoteContent()
				content.note = teacher_note_form.data['text']
				return (True, content, None,None)
			return (False, None, None,None)
		elif (content_type == 'CFU'):
			cfu_form = AddCFUContent(data=request.POST,objectives=base_methods.getObjectives(lesson))
			if cfu_form.is_valid():
				content = CFUContent()
				objectives = cfu_form.cleaned_data['objectives']
				content.text = cfu_form.data['text']
				content.expected_response = cfu_form.data['expected_response']
				return (True, content, None,objectives)
			return (False, None, None,None)
		elif (content_type == 'AdministratorNote'):
                        administrator_note_form = AddAdministratorNoteContent(data=request.POST)
                        if administrator_note_form.is_valid():
                                content = AdministratorNoteContent()
                                content.note = administrator_note_form.data['text']
                                return (True, content, None,None)
                        return (False, None, None,None)
		elif (content_type == 'Assessment'):
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


def manageStudents(request):
	base_dict = base_methods.createBaseDict(request)
	#get courses with students
	course_students = {}
	for course in base_dict['userCourses']:
		cs_list = ClassStudents.objects.filter(course_class__course__exact = course)
		
		student_list = [cs for cs in cs_list]
		for s in student_list:
			course_students[course] = student_list
	base_dict['courseStudents'] = course_students
	return render(request,'manage_students.html', base_dict)

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
		base_dict['teacherCoursesRequestForm'] = course_request
		base_dict['coursesWereRequested'] = True
		return render(request,'student_course.html', base_dict)
	else:
		return HttpResponseRedirect(request.session['last_page'])

def studentAddCourse(request):
	classRequestForm = ClassRequestForm(data=request.POST)
	teacher_id = classRequestForm.data['teacher_id']
	try:
		teacher = TeacherProfile.objects.get(id=teacher_id)
		student = StudentProfile.objects.get(user=request.user)
	except:
		return HttpResponseRedirect('/studentCourses/')
	
	classes = Class.objects.filter(course__owner__exact=teacher)
	class_list = []
	for c in classes:
		class_list.append((c.id, c.name))
	classRequestForm.fields['classes'].choices = class_list
	if classRequestForm.is_valid():
		try:
			for class_id in classRequestForm.cleaned_data['classes']:
				course_class = Class.objects.get(id=class_id)
				cs_exists = ClassStudents.objects.filter(course_class__student__exact=student, course_class=course_class)
				if cs_exists and len(cs_exists) > 0:
					return HttpResponseRedirect('/studentCourses/')
				cs = ClassStudents()
				cs.course_class = course_class
				cs.student = student
				cs.approved = False
				cs.save()
				return HttpResponseRedirect('/studentCourses/')
		except:
			return HttpResponseRedirect(request.session['last_page'])
	else:	
		print courseRequestForm.errors
		return HttpResponseRedirect(request.session['last_page'])

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

def getStandardsFromGroup(request):
	if request.method == 'POST':
		course_id = request.POST['course_id']
		try:
			course = Course.objects.get(id=course_id)
		except:
			return HttpResponse('')
		standard_list = course_methods.getCourseStandards(course, False)
		context = {'groupStandards': standard_list, 'justSynced': True}
		return direct_block_to_template(request,'course_view_standards.html', 'showGroupStandards', context)
	return HttpResponse('')

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

def manageCourseStudents(request):
	'''if request.method == 'POST':
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
				continue'''
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
		saf = StandardAnalysisForm(standard_id=s.id)
		base_dict['standardAnalysisForm'] = saf
		base_dict['ratingOptions'] = (1,2,3,4,5)
		base_dict['user_id'] = request.user.id
		return render(request,'standard_view.html', base_dict)

	return HttpResponseRedirect('/courses/')

def addStandardAnalysis(request):
	if request.method == 'POST':
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			return HttpResponseRedirect('/')

		form = StandardAnalysisForm(data=request.POST)
		if form.is_valid():
			standard_id = form.cleaned_data['standard_id']
			try:
				standard = Standard.objects.get(id=standard_id)
			except:
				print 'error in addStandardAnalysis'
				return HttpResponseRedirect('/standard/?standard_id='+str(standard_id))
			text = form.cleaned_data['analysis']
			sa, created = StandardAnalysis.objects.get_or_create(teacher=teacher,standard=standard)
			sa.analysis = text
			sa.number_raters=0
			sa.save()

	return HttpResponseRedirect('/standard/?standard_id='+str(standard_id))
		


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

'''
this will get the add form course given the standard
'''

#TODO finish this
def cloneUnit(request):
	if request.method  == 'POST':
		teacher = base_methods.checkUserIsTeacher(request.user)
		if not teacher:
			return HttpResponse('')
		course_id = request.POST.get('course_id')
		if course_id == None:
			return HttpResponse('')
		try:
			course = Course.objects.get(id=course_id)
		except:
			return HttpResponse('')
		new_course = course_methods.deepcopy_course(course, teacher)
		if new_course:
			return HttpResponse('success')
	return HttpResponse('')

