from Objective.models import Objective

def deepcopy_objective(objective, teacher):
	new_objective = Objective()
	
	cloned = new_objective.clone_from_parent(objective, teacher)

	if cloned:
		new_objective.owner = teacher
	else:
		return None

	new_objective.save()
	return new_objective
