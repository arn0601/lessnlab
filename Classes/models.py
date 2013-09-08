from Units.models import Unit
from Courses.models import Course
from accounts.models import StudentProfile
from Lessons.models import Lesson
from LessonPlanner.models import Section, Content
from django.db import models

# Create your models here.
class Class(models.Model):
	course = models.ForeignKey('Courses.Course')
	name = models.CharField(max_length=32)
	current_unit = models.ForeignKey('Units.Unit', blank=True, null=True)
	current_lesson = models.ForeignKey('Lessons.Lesson', blank=True, null=True)
	current_section = models.ForeignKey('LessonPlanner.Section', blank=True, null=True)
	current_content = models.ForeignKey('LessonPlanner.Content', blank=True, null=True)

class ClassStudents(models.Model):
	course_class = models.ForeignKey('Class')
	student = models.ForeignKey('accounts.StudentProfile')
	registered = models.BooleanField()
	approved = models.BooleanField()
