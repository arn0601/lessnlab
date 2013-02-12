from django import forms
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
	first_name = forms.CharField(required=True, label="First Name")
	last_name = forms.CharField(required=True, label="Last Name")
	birthdate = forms.DateField(required=True, label="Date of Birth")
	school = forms.CharField(required=True, label="School")
	school_district = forms.CharField(required=True, label="School District")
	school_state = forms.CharField(required=True, label="School State")

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
