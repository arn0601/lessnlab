from django import forms
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

USERTYPES = [('Teacher','Teacher'),('Student','Student')]
STATE_CHOICES = [('', 'None'),('PA','Pennsylvania'), ('MO', 'Missouri'), ('NY', 'New York')]
class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
	first_name = forms.CharField(required=True, label="First Name")
	last_name = forms.CharField(required=True, label="Last Name")
	birthdate = forms.DateField(required=True, label="Date of Birth")
	school = forms.CharField(required=True, label="School")
	school_district = forms.CharField(required=True, label="School District")
	school_state = forms.ChoiceField(required=True, choices=STATE_CHOICES, label="School State")
	user_type = forms.ChoiceField(label="User Type", choices=USERTYPES, required=True)

	def clean(self):
		cleaned_data = super(UserProfileRegistrationForm, self).clean()
		if len(cleaned_data['password1']) < 8:
			raise forms.ValidationError("Password length is too short")
		return cleaned_data

	def clean_school_state(self):
		data = self.cleaned_data['school_state'].lower()
		return data

	def clean_school(self):
		data = self.cleaned_data['school'].lower()
		return data

class TeacherRegistrationForm(UserProfileRegistrationForm):
	teacher_code = forms.CharField(required=True, label="Teacher Code")

	def clean(self):
		from accounts.models import *
		cleaned_data = super(TeacherRegistrationForm, self).clean()
		print 'cleaning'
		u = TeacherProfile.objects.filter(user_school_state=cleaned_data['school_state']).filter(teacher_code=cleaned_data['teacher_code'])
		print 'still here'
		if u:
			raise forms.ValidationError('Teacher code for state already in use')
		print 'asdasd'
		return cleaned_data

