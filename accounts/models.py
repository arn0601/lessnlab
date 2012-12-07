from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	TEACHER = 'T'
	STUDENT = 'S'
	user = models.OneToOneField(User)
	is_teacher = models.BooleanField()
	is_admin = models.BooleanField()
	is_student = models.BooleanField()
	
