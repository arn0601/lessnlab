from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from accounts.forms import *

def registerUserProfile(sender, user, request, **kwargs):
	from accounts.models import TeacherProfile, StudentProfile, TeacherProfileAttributes
	form = UserProfileRegistrationForm(data=request.POST)
	if form.data['user_type'] == 'Teacher':
		form = TeacherRegistrationForm(request.POST)
	
		user_profile = TeacherProfile(user=user)
		user_profile.user_firstname = form.data['first_name']
		user_profile.user_lastname = form.data['last_name']
		val = form.data['school_state']
		state, created = State.objects.get_or_create(value=val)
		user_profile.user_school_state = state
		user_profile.teacher_code = form.data['teacher_code']
		user_profile.user_type = 'Teacher'
		user_profile.save()
		user_profile = TeacherProfile.objects.get(user = user)
		teacher_profileAttrs = TeacherProfileAttributes(teacher=user_profile)
		teacher_profileAttrs.save()
	else:
		user_profile = StudentProfile(user=user)
		user_profile.user_firstname = form.data['first_name']
		user_profile.user_lastname = form.data['last_name']
		val = form.data['school_state']
		state, created = State.objects.get_or_create(value=val)
		user_profile.user_school_state = state
		user_profile.user_type = 'Student'
		user_profile.save()
