from django.db import models
from Standards.models import Standard
from accounts.models import TeacherProfile
from Lessons.models import Lesson
from Rating.models import Rating, Rateable
from datetime import datetime
# Create your models here.

class Objective(Rateable):
	description = models.CharField(max_length=64)
	standard = models.ForeignKey('Standards.Standard')
	owner = models.ForeignKey('accounts.TeacherProfile')
	creation_date = models.DateField()
	parent_objective = models.ForeignKey('self', null=True, blank=True)
	children_objectives = models.ManyToManyField('self', null=True, blank=True)
	lesson = models.ForeignKey('Lessons.Lesson')

	def clone_from_parent(self, objective, teacher, lesson):
		if objective and objective.id:
			self.description = objective.description
			self.standard = objective.standard
			self.owner = objective.owner
			self.creation_date = datetime.now()
			self.parent_objective = objective
		else:
			return False
		if teacher and teacher.id:
			self.owner = teacher
		else:
			return False
		if lesson and lesson.id:
			self.lesson = lesson
		else:
			return False
		return True

class ObjectiveRating(Rating):
	objective = models.ForeignKey('Objective')
