from django.db import models
from accounts.forms import UserProfileRegistrationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	user_firstname = models.CharField(max_length=32)
	user_lastname = models.CharField(max_length=32)
        user_dob = models.DateField()
	user_school_name = models.CharField(max_length=32)
	user_school_district = models.CharField(max_length=32)
        user_school_state = models.CharField(max_length=32)
        user_school_country = models.CharField(max_length=32)

def registerUserProfile(sender, user, request, **kwargs):
	form = UserProfileRegistrationForm(request.POST)
	user_profile = UserProfile(user=user)
	user_profile.user_firstname = form.data['first_name']
	user_profile.user_lastname = form.data['last_name']
	user_profile.user_dob = form.data['birthdate']
	user_profile.user_school_name = form.data['school']
	user_profile.user_school_district = form.data['school_district']
	user_profile.user_school_state = form.data['school_state']
	user_profile.save()

from registration.signals import user_registered
user_registered.connect(registerUserProfile)
