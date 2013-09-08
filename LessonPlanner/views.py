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
	print "Hitting SErver"
	return render(request,"lesson_presentation.html", base_dict)


def get_content_element(request):
	if request.method == 'GET':
		base_dict = base_methods.createBaseDict(request)
		lesson = base_dict['lesson']
		if ( lesson ):
			origcontent_num = int(request.GET.get('content_num',-1))
			origsection_num = int(request.GET.get('section_num',0))
			direction = int(request.GET.get('direction',0))
				
			secs = Section.objects.filter(lesson=lesson).order_by('placement')
			curSec = secs[origsection_num]
			conts = Content.objects.filter(section=curSec).order_by('placement')
			section_num = origsection_num
			content_num = origcontent_num + direction
			
			curCont = None
			origContent = None
			if origcontent_num != -1:
				origContent = conts[origcontent_num]
			if content_num != -1:
				curCont = conts[content_num] if len(conts) > content_num else None
			
			while len(conts) <= content_num or 0 > content_num:
				section_num = section_num + direction
				if len(secs) <= section_num or section_num < 0 :
					content_num = int(request.GET.get('content_num',-1))
					section_num = int(request.GET.get('section_num',0))
					curCont = origContent
					break
				curSec = secs[section_num]
				conts = Content.objects.filter(section=curSec).order_by('placement')
				if direction != -1:
					content_num = 0
				else:
					content_num = len(conts) - 1
				curCont = conts[content_num]
			context = { 'content' : curCont.as_leaf_class() }
			print str(curCont)
			additional_params = {'success':'1', 'lesson_id' : lesson.id,
														'content_num' : content_num, 'section_num' : section_num}
			if content_num  < 0:
				print "No Content"
				return HttpResponse(simplejson.dumps({'success':'0'}))
	
			htmlFile = "content/" + curCont.content_typename + "_presentation.html"
			print htmlFile
			return direct_json_to_template(request,htmlFile, 'contentData', context, additional_params)
		return HttpResponse(simplejson.dumps({'success':'0'}))
	return HttpResponseRedirect('/courses/')


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
			content.content_typename = contentForm.data['content_type']
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
			content.content_typename = contentForm.data['content_type']
			content.placement = getMaxCount(section)+1
			content.save()
		for link in online_video_form.cleaned_data['rl']:
			content = OnlineVideoContent()
			content.link = cleanVideoLink(link)
			section = Section.objects.get(id=int(contentForm.data['section_id']))
			content.section = section
			content.creation_date=datetime.now()
			content.content_typename = contentForm.data['content_type']
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

