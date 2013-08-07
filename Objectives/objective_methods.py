from Objectives.models import Objective


def shallowcopy_objective(objective, teacher, lesson):
	new_objective = Objective()
	cloned = new_objective.clone_from_parent(objective, teacher, lesson)
	if cloned:
		return new_objective
	else:
		return None

def deepcopy_objective(objective, teacher, lesson):
	#first copy over the course
	new_objective = shallowcopy_objective(objective, teacher, lesson)

	if not new_objective:
		return None

	new_objective.save()


	return new_objective
