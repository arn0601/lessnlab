# Create your views here.
from LessonPlanner.models import Lesson
from LessonPlanner.models import Course
from LessonPlanner.forms import AddCourse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from accounts.models import UserProfile
import simplejson
@csrf_exempt
def showTemplateLesson(request):
	uname = request.user.username
	fullname = uname
	form = AddCourse()
	return render_to_response('unit.html', {'username':uname, 'fullname':uname, 'courseAddForm':form})


def showLesson(request):
    	if request.is_ajax():
		action = request.POST.get('action')
		if(int(action) == 0):
        		lessonID = request.POST.get('lID')
			content = ContentSection.objects.filter(LessonID=lessonID)
			if content.count() == 0:
				return HttpResponse("")
			data = serializers.serialize('json', content, fields=('Content','SectionNumber','Header','ContentType','LessonID'))
			return HttpResponse(data)
		else:
			print "ajax request 2"
			jsonobj = request.POST.get('section')
			data = simplejson.loads(jsonobj)
			content = ContentSection.objects.filter(LessonID=request.POST.get('lID')).filter(SectionNumber=1)
			print content
			for c in content:
				c.Content=data['content']
				print c.Content
				c.save()
			#data = serializers.serialize('json', content, fields=('Content','SectionNumber','Header','ContentType','LessonID'))
			print "pushing data"
			#return HttpResponse(data)
	else:
		creatorID = request.user.id
		creatorName = request.user.username
		title =  "'s Lessons "
		allLessons = Lesson.objects.filter(CreatorID=creatorID)
		return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})
@csrf_exempt
def addCourse(request):
	print "Adding Course"	
	uname = request.user.username
        fullname = uname
	form = AddCourse()
	if request.method == 'POST':
		print "POSTING COURSE"
		form = AddCourse(data=request.POST)
		if form.is_valid():
			course = Course()
			
			course.owner = UserProfile.objects.get(user=request.user)
			course.subject = form.data['name']
			course.department = form.data['department']
			course.year = str(form.data['year'])
			course.save()
			form = AddCourse()
		return render_to_response('course.html', {'username':uname, 'fullname':uname, 'courseAddForm':form})
	else:
		return render_to_response('course.html',{'username':uname, 'fullname':uname, 'courseAddForm':form} )

