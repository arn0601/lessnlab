from django.db import models
from accounts.models import TeacherProfile, StudentProfile
from Standards.models import *
from Objectives.models import Objective
from Rating.models import Rating, Rateable


SECTIONTYPE = ((1,'Introduction'), (2,'Review'), (3,'New Material'), (4,'Guided Practice'), (5, 'Independent Practice'))

CONTENTTYPE = (('Text','Text'),('OnlineVideo','OnlineVideo'),('OnlineArticle','OnlineArticle'),('OnlinePicture','OnlinePicture'),('TeacherNote','TeacherNote'),('AdministratorNote','AdministratorNote'),('Assessment','Assessment'),('PowerPoint','PowerPoint'),('Activity','Activity'))

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))

LESSONPLANNER_DROPDOWN_ORDER = ['General', 'Media', 'Checks for Understanding', 'Activity', 'Assessment']

class AssessmentType(models.Model):
	assessment_type = models.CharField(max_length=32, choices = ASSESSMENTTYPE)

class Tag(models.Model):
	tagname = models.CharField(max_length=32)

class Course(Rateable):
	name = models.CharField(max_length=32)
	description = models.TextField()
	owner = models.ForeignKey('accounts.TeacherProfile')
	state = models.ForeignKey('Standards.State')
	department = models.CharField(max_length=32)
	subject = models.ForeignKey('Standards.Subject')
	grade = models.ForeignKey('Standards.Grade')
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
			

class Class(models.Model):
	course = models.ForeignKey('Course')
	name = models.CharField(max_length=32)
	current_unit = models.ForeignKey('Unit')
	current_lesson = models.ForeignKey('Lesson')
	current_section = models.ForeignKey('Section')
	current_content = models.ForeignKey('Content')

class ClassStudents(models.Model):
	course_class = models.ForeignKey('Class')
	student = models.ForeignKey('accounts.StudentProfile')
	registered = models.BooleanField()
	approved = models.BooleanField()

class CourseRating(Rating):
	course = models.ForeignKey('Course')

class StandardGrouping(models.Model):
	name = models.CharField(max_length=64)
	subject = models.ForeignKey('Standards.Subject')
	grade = models.ForeignKey('Standards.Grade')
	standard_type = models.ForeignKey('Standards.StandardType')
	state = models.ForeignKey('Standards.State', null=True, blank=True)
	standard = models.ManyToManyField('Standards.Standard')
	creation_date = models.DateField(null=True)
	prebuilt = models.BooleanField()


class Unit(Rateable):
	name = models.CharField(max_length=32)
	description = models.TextField()
	assessment_type = models.ManyToManyField(AssessmentType, blank=True)
	course = models.ForeignKey('Course')
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

# Create your models here.
class Lesson(Rateable):
	name = models.CharField(max_length=30)
	unit = models.ForeignKey(Unit)
	owner = models.ForeignKey('accounts.TeacherProfile')
	tags = models.TextField()
	description = models.TextField()
	standards = models.ManyToManyField('Standards.Standard', blank=True)
	objectives = models.ManyToManyField('Objectives.Objective', blank=True)
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

class Section(Rateable):
	lesson = models.ForeignKey(Lesson)
	placement = models.IntegerField(blank=True)
	name = models.IntegerField(max_length=32, choices=SECTIONTYPE)
	description = models.TextField()
	creation_date = models.DateTimeField(blank=True, null=True)	

class Content(Rateable):
	section = models.ForeignKey(Section)
	creation_date = models.DateTimeField()
	placement = models.IntegerField()
	content_type = models.CharField(choices=CONTENTTYPE, max_length=32)
	objectives = models.ManyToManyField('Objectives.Objective', blank=True, null=True)

class ContentRating(Rating):
	content = models.ForeignKey('Content')

#All content types will be subclasses of Content
class TextContent(Content):
	text = models.TextField()

class PowerPointContent(Content):
        link = models.CharField(max_length=256)

class ActivityContent(Content):
	name = models.CharField(max_length=30)
        description = models.TextField()
	activity_type = models.CharField(max_length=30)
	instructions = models.TextField()
	length = models.FloatField()
	materials = models.TextField()

class CFUContent(Content):
        text = models.CharField(max_length=256)
	expected_response = models.CharField(max_length=256) 

class OnlineVideoContent(Content):
	link = models.CharField(max_length=256)

class OnlineArticleContent(Content):
	link = models.CharField(max_length=256)

class TeacherNoteContent(Content):
	note = models.CharField(max_length=256)

class AdministratorNoteContent(Content):
	note = models.CharField(max_length=256)

class OnlinePictureContent(Content):
	link = models.CharField(max_length=256)

class AssessmentContent(Content):
        title = models.CharField(max_length=256)

class Question(models.Model):
	question = models.CharField(max_length=256)
	placement = models.IntegerField()
	assessment =  models.ForeignKey(AssessmentContent)
	
class Answer(models.Model):
	owner = models.ForeignKey('accounts.UserProfile')
	question =  models.ForeignKey(Question)
	
class FreeResponseAnswer(Answer):
	answer = models.CharField(max_length=256)

class MultipleChoiceAnswer(Answer):
	answer = models.CharField(max_length=256)
	is_checked = models.BooleanField(default=False)

class StandardAnalysis(Rateable):
	teacher = models.ForeignKey('accounts.TeacherProfile')
	standard = models.ForeignKey('Standards.Standard')
	analysis = models.TextField(null=True, blank=True)

class StandardAnalysisRating(Rating):
	standard_analysis = models.ForeignKey('StandardAnalysis')
