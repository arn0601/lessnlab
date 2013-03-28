from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from accounts.forms import *

def registerUserProfile(sender, user, request, **kwargs):
	from accounts.models import TeacherProfile, StudentProfile
	form = UserProfileRegistrationForm(request.POST)
	print form.data['user_type']
	if form.data['user_type'] == 'Teacher':
		form = TeacherRegistrationForm(request.POST)
	
		user_profile = TeacherProfile(user=user)
		user_profile.user_firstname = form.data['first_name']
		user_profile.user_lastname = form.data['last_name']
		user_profile.user_dob = form.data['birthdate']
		user_profile.user_school_name = form.data['school']
		user_profile.user_school_district = form.data['school_district']
		user_profile.user_school_state = form.data['school_state']
		user_profile.teacher_code = form.data['teacher_code']
		user_profile.user_type = 'Teacher'
		user_profile.save()
	else:
		user_profile = StudentProfile(user=user)
		user_profile.user_firstname = form.data['first_name']
		user_profile.user_lastname = form.data['last_name']
		user_profile.user_dob = form.data['birthdate']
		user_profile.user_school_name = form.data['school']
		user_profile.user_school_district = form.data['school_district']
		user_profile.user_school_state = form.data['school_state']
		user_profile.user_type = 'Student'
		user_profile.save()
