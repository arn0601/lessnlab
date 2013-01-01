# Create your views here.
from LessonPlanner.models import Lesson
from LessonPlanner.models import ContentSection
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
@csrf_exempt
def showLesson(request):
	print "IN REQUEST"
    	if request.is_ajax():
        	lessonID = request.POST.get('lID')
		print "AJAX REQUEST",lessonID
		content = ContentSection.objects.filter(LessonID=lessonID)
		print content.count()
		if content.count() == 0:
			return HttpResponse("")
		data = serializers.serialize('json', content, fields=('Content','SectionNumber','Header','ContentType','LessonID'))
		print data,"","asd"
		return HttpResponse(data)
	else:
		creatorID = request.user.id
		creatorName = request.user.username
		print creatorID
		print creatorName
		title =  "'s Lessons "
		allLessons = Lesson.objects.filter(CreatorID=creatorID)
		return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})

