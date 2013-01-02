# Create your views here.
from LessonPlanner.models import Lesson
from LessonPlanner.models import ContentSection
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
import simplejson
@csrf_exempt
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
			print jsonobj
			data = simplejson.loads(jsonobj)
			print data['sectionNumber'], request.POST.get('lID')
			content = ContentSection.objects.filter(LessonID=request.POST.get('lID')).filter(SectionNumber=1)
			print content
			content.Content=data['content']
			print content.Content
			content.save()
			#data = serializers.serialize('json', content, fields=('Content','SectionNumber','Header','ContentType','LessonID'))
			print "pushing data"
			#return HttpResponse(data)
	else:
		creatorID = request.user.id
		creatorName = request.user.username
		title =  "'s Lessons "
		allLessons = Lesson.objects.filter(CreatorID=creatorID)
		return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})

