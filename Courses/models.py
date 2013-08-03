from django.db import models
from Types.models import *
from accounts.models import TeacherProfile, StudentProfile
from Standards.models import *
from Rating.models import Rating, Rateable
# Create your models here.

class Course(Rateable):
	name = models.CharField(max_length=32)
	description = models.TextField()
	owner = models.ForeignKey('accounts.TeacherProfile')
	state = models.ForeignKey('Types.State')
	department = models.CharField(max_length=32)
	subject = models.ForeignKey('Types.Subject')
	grade = models.ForeignKey('Types.Grade')
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	standard_grouping = models.ManyToManyField('StandardGrouping', blank=True, null=True)
	parent = models.ForeignKey('self', null=True, blank=True)

	def clone_from_parent(self, course, teacher=None):	
		if course and course.id:
			self.name = course.name
			self.owner = course.owner
			self.department = course.department
			self.subject = course.subject
			self.grade = course.grade
			#skip start and end date, who knows what these are
			self.state = course.state
		else:
			return False
		if teacher and teacher.id:
			self.owner = teacher
		else:
			return False
		return True
			


class CourseRating(Rating):
	course = models.ForeignKey('Course')

class StandardGrouping(models.Model):
	name = models.CharField(max_length=64)
	subject = models.ForeignKey('Types.Subject')
	grade = models.ForeignKey('Types.Grade')
	standard_type = models.ForeignKey('Types.StandardType')
	state = models.ForeignKey('Types.State', null=True, blank=True)
	standard = models.ManyToManyField('Standards.Standard')
	creation_date = models.DateField(null=True)
	prebuilt = models.BooleanField()
