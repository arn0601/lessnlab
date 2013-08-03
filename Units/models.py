from django.db import models
from accounts.models import TeacherProfile, StudentProfile
from Standards.models import *
from Rating.models import Rating, Rateable
from Courses.models import Course

from Types.models import *
ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))
# Create your models here.
class AssessmentType(models.Model):
	assessment_type = models.CharField(max_length=32, choices = ASSESSMENTTYPE)

class Unit(Rateable):
	name = models.CharField(max_length=32)
	description = models.TextField()
	assessment_type = models.ManyToManyField(AssessmentType, blank=True)
	course = models.ForeignKey('Courses.Course')
	owner = models.ForeignKey('accounts.TeacherProfile')
	parent_unit = models.ForeignKey('self', null=True, blank=True)
	standards = models.ManyToManyField('Standards.Standard', blank=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)

	def clone_from_parent(self, unit, teacher, course):
		if unit and unit.id:
			self.name = unit.name
			self.description = unit.description
			self.course = unit.course
			self.owner = unit.owner
			self.parent_unit = unit
			#skip standards, cant add unless you save
			#skip start and end date, who know what these are
		else:
			return False
		if teacher and teacher.id:
			self.owner = teacher
		else:
			return False
		if course and course.id:
			self.course = course
		else:
			return False
		return True

class UnitRating(Rating):
	unit = models.ForeignKey('Unit')
