from django.db import models
from accounts.models import TeacherProfile
from Standards.models import Standard


SECTIONTYPE = ((1,'Introduction'), (2,'Review'), (3,'New Material'), (4,'Guided Practice'), (5, 'Independent Practice'))

CONTENTTYPE = (('Text','Text'),('OnlineVideo','OnlineVideo'),('OnlineArticle','OnlineArticle'),('OnlinePicture','OnlinePicture'),('TeacherNote','TeacherNote'),('AdministratorNote','AdministratorNote'))

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))

LESSONPLANNER_DROPDOWN_ORDER = ['General', 'Media', 'Checks for Understanding', 'Activity', 'Assessment']

class AssessmentType(models.Model):
	assessment_type = models.CharField(max_length=32, choices = ASSESSMENTTYPE)

class Tag(models.Model):
	tagname = models.CharField(max_length=32)

class Course(models.Model):
	owner = models.ForeignKey('accounts.TeacherProfile')
	department = models.CharField(max_length=32)
	subject = models.CharField(max_length=32)
	year = models.PositiveIntegerField()

class Unit(models.Model):
	name = models.CharField(max_length=32)
	description = models.TextField()
	assessment_type = models.ManyToManyField(AssessmentType)
	course = models.ForeignKey('Course')
	owner = models.ForeignKey('accounts.TeacherProfile')
	parent_unit = models.ForeignKey('self', null=True)
	standards = models.ManyToManyField('Standards.Standard')
	tags = models.ManyToManyField(Tag)
	week_length = models.IntegerField()
	
# Create your models here.
class Lesson(models.Model):
	name = models.CharField(max_length=30)
	unit = models.ForeignKey(Unit)
	owner = models.ForeignKey('accounts.TeacherProfile')
	tags = models.TextField()
	description = models.TextField()
	standards = models.ManyToManyField('Standards.Standard')

class Section(models.Model):
	lesson = models.ForeignKey(Lesson)
	placement = models.IntegerField()
	name = models.IntegerField(max_length=32, choices=SECTIONTYPE)
	description = models.TextField()
	creation_date = models.DateTimeField()	

class Content(models.Model):
	section = models.ForeignKey(Section)
	creation_date = models.DateTimeField()
	placement = models.IntegerField()
	content_type = models.CharField(choices=CONTENTTYPE, max_length=32)

#All content types will be subclasses of Content
class TextContent(Content):
	text = models.TextField()

class OnlineVideoContent(Content):
	link = models.CharField(max_length=256)

class OnlineArticleContent(Content):
	link = models.CharField(max_length=256)

class TeacherNote(Content):
	note = models.CharField(max_length=256)

class AdministratorNode(Content):
	note = models.CharField(max_length=256)

class OnlinePictureContent(Content):
	link = models.CharField(max_length=256)
