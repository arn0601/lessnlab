from django.db import models
from Standards.models import Standard
from accounts.models import UserProfile
# Create your models here.

class Objective(models.Model):
	name = models.CharField(max_length=32)
	standard = models.ForeignKey('Standards.Standard')
	owner = models.ForeignKey('accounts.UserProfile')
	course = models.ForeignKey('Course') 
	creationDate = models.DateField()
	parentObjective = models.ForeignKey('self')
	childrenOnjectives = models.ManyToManyField('self')
	description = models.TextField()
	rating = models.PositiveIntegerField()

class Course(models.Model):
	owner = models.ForeignKey('accounts.UserProfile')
	department = models.CharField(max_length=32)
	subject = models.CharField(max_length=32)
	year = models.PositiveIntegerField()
