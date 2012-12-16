# Create your views here.
from LessonPlanner.models import Lesson

def showLesson(request):
	creator = request.session.get('uesrname')
	title = creator + "'s Lessons "
	allLessons = Lesson.objects.filter(CreatorID=creator)
	return render_to_response('lessons.html', {'allLessons':allLessons, 'title':title})


