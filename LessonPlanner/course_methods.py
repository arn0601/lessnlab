from LessonPlanner.models import Course, StandardGrouping
from Standards.models import Standard

def getCourseStandards(course, use_tuple):
	standard_list = []
	for group in course.standard_grouping.all():
		for standard in group.standard.all():
			if use_tuple:
				standard_list.append((standard.id, standard.description))
			else:
				standard_list.append(standard)
	return standard_list
