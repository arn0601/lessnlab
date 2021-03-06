from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
import extra_methods
from Standards.models import State
from Rating.models import Rating
from Types.models import *


USERTYPES = [('Teacher','Teacher'),('Student','Student')]

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	user_firstname = models.CharField(max_length=32)
	user_lastname = models.CharField(max_length=32)
	user_dob = models.DateField(null=True, blank=True)
	user_school_name = models.CharField(max_length=32, null=True, blank=True)
	user_school_district = models.CharField(max_length=32, null=True, blank=True)
	user_school_state = models.ForeignKey('Types.State')
	user_type = models.CharField(max_length=32, choices=USERTYPES)

class TeacherProfile(UserProfile):
  teacher_code = models.CharField(max_length=32)


class TeacherProfileAttributes(models.Model):
	teacher					= models.OneToOneField(TeacherProfile)
	bio							= models.CharField(null=True, verbose_name="Bio", max_length=1024)
	linkedIn_url 		= models.CharField(null=True, verbose_name="LinkedIn",max_length=32)
	twitter_handle 	= models.CharField(null=True, verbose_name="Twitter", max_length=32)
	college 				= models.CharField(null=True, verbose_name="College", max_length=128)
	gradschool			= models.CharField(null=True, verbose_name="Grad School", max_length=128)
	major   				= models.CharField(null=True, verbose_name="Major", max_length=128)
	skills					= models.CharField(null=True, verbose_name="Skills", max_length=128)
	expertise				= models.CharField(null=True, verbose_name="Expertise", max_length=128)


class TeacherRating(Rating):
	teacher = models.ForeignKey('TeacherProfile')

class StudentProfile(UserProfile):
	dummy = models.CharField(max_length=32)
	
	
class StudentProfileAttributes(models.Model):
	student					= models.OneToOneField(StudentProfile)
	bio							= models.CharField(null=True, verbose_name="Bio", max_length=1024)


from registration.signals import user_registered
user_registered.connect(extra_methods.registerUserProfile)
