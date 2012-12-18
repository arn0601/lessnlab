# Create your views here.
from LessonPlanner.models import Lesson
from django.shortcuts import render_to_response

def showLesson(request):
	print "IN REQUEST"
    	if request.is_ajax():
        	print "AJAX REQUEST"
		return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})
	else:
		creatorID = request.user.id
		creatorName = request.user.username
		print creatorID
		print creatorName
		title =  "'s Lessons "
		allLessons = Lesson.objects.filter(CreatorID=creatorID)
		return render_to_response('lessons.html', {'allLessons':allLessons, 'title':creatorName})

from datetime import date, timedelta
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
DATE_FORMAT='%m/%d/%Y'
@csrf_exempt
def today(request):
    print "IN REQUEST"
    if request.is_ajax():
        print "AJAX REQUEST"
	t = request.POST.get('today')
        dt = parser.parse(t)
        one_day = timedelta(days=1)
        yesterday = dt - one_day

        return HttpResponse(yesterday.strftime(DATE_FORMAT))
    else:
        today = date.today()
        return render_to_response('lessons.html', {'today': today.strftime(DATE_FORMAT)},
                context_instance=RequestContext(request))

