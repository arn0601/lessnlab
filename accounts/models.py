from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
import extra_methods
from Rating.models import Rating

STATE_CHOICES = [('', 'None'),('PA','Pennsylvania'), ('MO', 'Missouri'), ('NY', 'New York')]

USERTYPES = [('Teacher','Teacher'),('Student','Student')]

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	user_firstname = models.CharField(max_length=32)
	user_lastname = models.CharField(max_length=32)
        user_dob = models.DateField()
	user_school_name = models.CharField(max_length=32)
	user_school_district = models.CharField(max_length=32)
        user_school_state = models.CharField(max_length=32, choices=STATE_CHOICES, default='')
	user_type = models.CharField(max_length=32, choices=USERTYPES)

class TeacherProfile(UserProfile):
        teacher_code = models.CharField(max_length=32)
	
class TeacherRating(Rating):
	teacher = models.ForeignKey('TeacherProfile')

class StudentProfile(UserProfile):
	dummy = models.CharField(max_length=32)


from registration.signals import user_registered
user_registered.connect(extra_methods.registerUserProfile)
