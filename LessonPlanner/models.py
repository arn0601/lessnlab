from django.db import models
from accounts.models import UserProfile
from Standards.models import Standard
HEADER = ((1,'Review Previous'),(2,'New Content'),(3,'Assessment'))


CONTENTTYPE = (('Text','Text'),('VideoLink','VideoLink'),('ArticleLink','ArticleLink'))

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))


class AssessmentType(models.Model):
	assessment_type = models.CharField(max_length=32, choices = ASSESSMENTTYPE)

class Tag(models.Model):
	tagname = models.CharField(max_length=32)

class Course(models.Model):
	owner = models.ForeignKey('accounts.UserProfile')
	department = models.CharField(max_length=32)
	subject = models.CharField(max_length=32)
	year = models.PositiveIntegerField()

class Unit(models.Model):
	name = models.CharField(max_length=32)
	description = models.TextField()
	assessment_type = models.ManyToManyField(AssessmentType)
	course = models.ForeignKey('Course')
	owner = models.ForeignKey('accounts.UserProfile')
	parent_unit = models.ForeignKey('self', null=True)
	standards = models.ManyToManyField('Standards.Standard')
	tags = models.ManyToManyField(Tag)
	week_length = models.IntegerField()
	
# Create your models here.
class Lesson(models.Model):
	name = models.CharField(max_length=30)
	unit = models.ForeignKey(Unit)
	owner = models.ForeignKey('accounts.UserProfile')
	tags = models.TextField()
	standards = models.ManyToManyField('Standards.Standard')

class Section(models.Model):
	lesson = models.ForeignKey(Lesson)
	section_placement = models.IntegerField()
	section_name = models.CharField(max_length=32)
	section_description = models.TextField()
	creation_date = models.DateTimeField()	

class Content(models.Model):
	content_type = models.IntegerField(choices=CONTENTTYPE)
	section = models.ForeignKey(Section)
	creation_date = models.DateTimeField()
	section_position = models.IntegerField()
	content_subtype = models.CharField(choices=CONTENTTYPE, max_length=32)

#All content types will be subclasses of Content
class TextContent(Content):
	text = models.TextField()

class OnlineVideoContent(Content):
	link = models.CharField(max_length=256)

class ArticleLinkContent(Content):
	link = models.CharField(max_length=256)

