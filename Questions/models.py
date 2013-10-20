from django.db import models
from Objectives.models import Objective
from accounts.models import UserProfile, TeacherProfile, StudentProfile
from Types.models import QuestionType

# Create your models here.
class Question(models.Model):
	question = models.CharField(max_length=256)
	owner = models.ForeignKey('accounts.TeacherProfile', null=True, blank=True)
	objective = models.ForeignKey('Objectives.Objective')

class TeacherAnswer(models.Model):
	owner = models.ForeignKey('accounts.TeacherProfile', null=True, blank=True)
	question = models.ForeignKey(Question)
	correct = models.BooleanField()
	answer = models.CharField(max_length=256)

class StudentAnswer(models.Model):
	answer = models.CharField(max_length=256)
	owner = models.ForeignKey('accounts.StudentProfile')

class AnswerGrade(models.Model):
	grade = models.CharField(max_length=256)
	percent = models.IntegerField()
