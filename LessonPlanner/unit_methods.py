from LessonPlanner.models import Unit
from Standards.models import Standard

def getUnitStandards(unit, use_tuple) :
	standard_list = []
	for standard in unit.standards.all():
		if use_tuple:
			standard_list.append((standard.id, standard.description))
		else:
			standard_list.append(standard)
	return standard_list

