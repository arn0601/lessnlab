from django.db import models
from accounts.models import UserProfile
from Standards.models import Standard
HEADER = ((1,'Review Previous'),(2,'New Content'),(3,'Assessment'))


CONTENTTYPE = ((1,'Video'),(2,'TEXT'),(3,'PICTURE'))

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))

class AssessmentType(models.Model):
	assessment_type = models.CharField(max_length=32, choices = ASSESSMENTTYPE)

class Tag(models.Model):
	tagname = models.CharField(max_length=32)

# Create your models here.
class Lesson(models.Model):
	LessonID = models.AutoField(primary_key=True)
	LessonTitle = models.CharField(max_length=30)
	CreatorID = models.ForeignKey('accounts.UserProfile')
	Tags = models.TextField()

class Course(models.Model):
	owner = models.ForeignKey('accounts.UserProfile')
	department = models.CharField(max_length=32)
	subject = models.CharField(max_length=32)
	year = models.PositiveIntegerField()

class Unit(models.Model):
	name = models.CharField(max_length=32)
	description = models.TextField()
	assessmentType = models.ManyToManyField(AssessmentType)
	courseID = models.ForeignKey('Course')
	owner = models.ForeignKey('accounts.UserProfile')
	parent_unit_id = models.ForeignKey('self', null=True)
	standards = models.ManyToManyField('Standards.Standard')
	tags = models.ManyToManyField(Tag)
	
	
