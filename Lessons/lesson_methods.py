from Standards.models import Standard
from Units.models import Unit
from Lessons.models import Lesson

def getLessonStandards(lesson, use_tuple):
	standard_list = []
	for standard in lesson.standards.all():
		if use_tuple:
			standard_list.append((standard.id, standard.description))
		else:
			standard_list.append(standard)
	return standard_list


def shallowcopy_lesson(lesson, teacher, unit):
	new_lesson = Lesson()
	cloned = new_lesson.clone_from_parent(lesson, teacher, unit)
	if cloned:
		return new_lesson
	else:
		return None

def deepcopy_lesson(lesson, teacher, unit):
	#first copy over the course
	new_lesson = shallowcopy_lesson(lesson, teacher, unit)

	if not new_lesson:
		return None

	new_lesson.save()

	for standard in lesson.standards.all():
		new_lesson.standards.add(standard)

	for objective in lesson.objectives.all():
		new_objective = objective_methods.deepcopy_objective(objective, teacher, new_lesson)
		new_lesson.objectives.add(new_objective)

	#deepcopy lesson stuff TODO for aman

	return new_lesson
