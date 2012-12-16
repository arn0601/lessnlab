# Create your views here.
from LessonPlanner.models import Lesson
from django.shortcuts import render_to_response

def showLesson(request):
	creatorID = request.user.id
	creatorName = request.user.username
	print creatorID
	print creatorName
	title =  "'s Lessons "
	allLessons = Lesson.objects.filter(CreatorID=creatorID)
	return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})


