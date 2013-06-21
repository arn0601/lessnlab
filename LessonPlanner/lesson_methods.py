from LessonPlanner.models import Lesson
from Standards.models import Standard

def getLessonStandards(lesson, use_tuple):
	standard_list = []
	for standard in lesson.standards.all():
		if use_tuple:
			standard_list.append((standard.id, standard.description))
		else:
			standard_list.append(standard)
	return standard_list
