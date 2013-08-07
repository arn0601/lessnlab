from django.db import models
from Rating.models import Rateable, Rating
from Units.models import Unit
from Standards.models import Standard
from Types.models import *

# Create your models here.
class Tag(models.Model):
	tagname = models.CharField(max_length=32)

class Lesson(Rateable):
	name = models.CharField(max_length=30)
	unit = models.ForeignKey('Units.Unit')
	owner = models.ForeignKey('accounts.TeacherProfile')
	tags = models.TextField()
	description = models.TextField()
	standards = models.ManyToManyField('Standards.Standard', blank=True)
	start_date = models.DateField(null=True)
        end_date = models.DateField(null=True)

	def clone_from_parent(self, lesson, teacher, unit):
		if lesson and lesson.id:
			self.name = lesson.name
			self.unit = lesson.unit
			self.owner = lesson.owner
			self.tags = lesson.tags
			self.description = lesson.description
			#skip standards and objectives
			#skip start and end date who knows when there are
		else:
			return False
		if teacher and teacher.id:
			self.owner = teacher
		else:
			return False
		if unit and unit.id:
			self.unit = unit
		else:
			return False
		return True

class LessonRating(Rating):
	lesson = models.ForeignKey('Lesson')
