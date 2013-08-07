from Lessons.models import Lesson
from Units.models import Unit
from Lessons import lesson_methods
from Standards.models import Standard

def getUnitStandards(unit, use_tuple) :
	standard_list = []
	for standard in unit.standards.all():
		if use_tuple:
			standard_list.append((standard.id, standard.description))
		else:
			standard_list.append(standard)
	return standard_list

def shallowcopy_unit(unit, teacher, course):
	new_unit = Unit()
	cloned = new_unit.clone_from_parent(unit, teacher, course)
	if cloned:
		return new_unit
	else:
		return None

def deepcopy_unit(unit, teacher, course):
	#first copy over the course
	new_unit = shallowcopy_unit(unit, teacher, course)

	if not new_unit:
		return None

	new_unit.save()	

	for standard in unit.standards.all():
		new_unit.standards.add(standard)

	#deepcopy lessons
	lessons = Lesson.objects.filter(unit=unit)
	for lesson in lessons:
		lesson_methods.deepcopy_lesson(lesson, teacher, new_unit)
	return new_unit
