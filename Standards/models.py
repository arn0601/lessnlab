from django.db import models
from Rating.models import Rating, Rateable
from Types.models import *

class Standard(models.Model):
	state = models.ForeignKey('Types.State', null=True, blank=True)
	description = models.TextField()
	creation_date = models.DateTimeField()
	start_date = models.DateField()
	expiration_date = models.DateField()
	department = models.CharField(max_length=32)
	subject = models.ForeignKey('Types.Subject')
	grade = models.ForeignKey('Types.Grade')
	numbering = models.CharField(max_length=32)
	standard_type = models.ForeignKey('Types.StandardType')

class StandardAnalysis(Rateable):
	teacher = models.ForeignKey('accounts.TeacherProfile')
	standard = models.ForeignKey('Standards.Standard')
	analysis = models.TextField(null=True, blank=True)

class StandardAnalysisRating(Rating):
	standard_analysis = models.ForeignKey('StandardAnalysis')
