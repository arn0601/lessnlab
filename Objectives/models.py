from django.db import models
from Standards import standard
# Create your models here.

class Objective(models.Model):
	name = models.charField(max_length=32)
	standard = models.ForeignKey('Standard')
	owner = models.charField(max_length=32)
	course = models.ForeignKey('Course') 
	creationDate = models.DateField()
	parentObjective = models.ForeignKey('Objective')
	childrenOnjectives = models.ManyToManyField(Objective)
	description = models.TextField()
	rating = models.PositiveIntegerField()

class Course(models.model)
	owner = models.ForiegnKey('Owner')
	department = models.charField(max_length=32)
	subject = models.charField(max_length=32)
	year = models.PositiveIntegerField()
