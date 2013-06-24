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

def shallowcopy_course(course, teacher):
	new_course = Course()
	cloned = new_course.clone_from_parent(course, teacher)
	if cloned:
		return new_course
	else:
		return None

def deepcopy_course(course, teacher):
	#first copy over the course
	new_course = shallowcopy_course(course, teacher)

	if not new_course:
		return None

	#this is so the units will have a course to attach to
	new_course.save()

	#now we can do standards goupign:
	for group in course:
		new_course.standard_grouping.add(group)

	#deepcopy units
	units = Unit.objects.filter(course=course)
	for unit in units:
		unit_methods.deepcopy_unit(unit, teacher, new_course)
	return new_course
