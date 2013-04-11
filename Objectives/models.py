from django.db import models
from Standards.models import Standard
from accounts.models import TeacherProfile
from LessonPlanner.models import Course, Lesson
# Create your models here.

class Objective(models.Model):
	description = models.CharField(max_length=64)
	standard = models.ForeignKey('Standards.Standard')
	owner = models.ForeignKey('accounts.TeacherProfile')
	creation_date = models.DateField()
	parent_objective = models.ForeignKey('self')
	children_objectives = models.ManyToManyField('self')
	rating = models.PositiveIntegerField()
