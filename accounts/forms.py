from django import forms
from registration.forms import *
from registration.models import RegistrationProfile
from Standards.models import State

import custom_widgets

USERTYPES = [('Teacher','Teacher'),('Student','Student')]
class UserProfileRegistrationForm(RegistrationForm):
	first_name = forms.CharField(required=True, label="First Name")
	last_name = forms.CharField(required=True, label="Last Name")
	#dateWidget = custom_widgets.CalendarDateSelectField()
	#birthdate = forms.CharField(required=True, label="Date of Birth",widget=dateWidget)
	#school = forms.CharField(required=True, label="School")
	#school_district = forms.CharField(required=True, label="School District")
	school_state = forms.CharField(label='State')
	user_type = forms.CharField(label="")
	user_type.widget = forms.HiddenInput()

	def isTeacher():
		return False;

	def clean(self):
		if len(self.cleaned_data['password1']) < 8:
			raise forms.ValidationError("Password length is too short")
		return self.cleaned_data

	def clean_school(self):
		data = self.cleaned_data['school'].lower()
		return data

class TeacherRegistrationForm(UserProfileRegistrationForm):
	teacher_code = forms.CharField(required=True, label="Teacher Code")

	def __init__(self, *args, **kwargs):
		super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['user_type'].initial='Teacher'

	def clean(self):
		from accounts.models import TeacherProfile
		cleaned_data = super(TeacherRegistrationForm, self).clean()
		code = teacher_code['teacher_code']
		if not (int(code) > 5000000 and (int(code) % 17 == 0)):
			raise forms.ValidationError('Teacher code invalid')
		val = cleaned_data['school_state']
		print "asd",cleaned_data['school_state']
		state = State.objects.get(value=cleaned_data['school_state'])
		print "asdasd"
		u = TeacherProfile.objects.filter(user_school_state=state).filter(teacher_code=cleaned_data['teacher_code'])
		if u:
			raise forms.ValidationError('Teacher code for state already in use')
		return cleaned_data

class StudentRegistrationForm(UserProfileRegistrationForm):
	def __init__(self, *args, **kwargs):
		super(StudentRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['user_type'].initial='Student'
