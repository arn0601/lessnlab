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
	current_unit = models.ForeignKey('Units.Unit')
	current_lesson = models.ForeignKey('Lessons.Lesson')
	current_section = models.ForeignKey('LessonPlanner.Section')
	current_content = models.ForeignKey('LessonPlanner.Content')

class ClassStudents(models.Model):
	course_class = models.ForeignKey('Class')
	student = models.ForeignKey('accounts.StudentProfile')
	registered = models.BooleanField()
	approved = models.BooleanField()
