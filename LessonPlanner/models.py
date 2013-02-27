from django.db import models
from accounts.models import UserProfile

HEADER = ((1,'Review Previous'),(2,'New Content'),(3,'Assessment'))


CONTENTTYPE = ((1,'Video'),(2,'TEXT'),(3,'PICTURE'))

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
