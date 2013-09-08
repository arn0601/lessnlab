from django import forms
from django.contrib.auth.models import User
import Utils.custom_widgets as custom_widgets
from Courses.models import *
from accounts.models import TeacherProfile
from Classes.models import *

class AddClassForm(forms.ModelForm):
	class Meta:
		model = Class
		widgets = { 'course': forms.HiddenInput() }
		exclude = ['current_unit', 'current_lesson', 'current_content', 'current_section']

	def __init__(self, *args, **kwargs):
		course = kwargs.pop('course', None)
		super(AddClassForm, self).__init__(*args, **kwargs)
		if course:
			self.fields['course'].initial = course
		self.fields['course'].label=''

class ClassRequestForm(forms.Form):
	teacher = forms.IntegerField(label='')
	teacher.widget = forms.HiddenInput()
	classes = forms.ModelMultipleChoiceField(label='Choose classes', queryset=Class.objects.none())

	def __init__(self, *args, **kwargs):
		teacher = kwargs.pop('teacher', None)
		super(ClassRequestForm, self).__init__(*args, **kwargs)
		if teacher:
			self.fields['teacher'].initial = teacher.id

class TeacherRequestForm(forms.Form):
	email = forms.CharField(label='Teacher Email')

	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = User.objects.get(email=data)
			teacher = TeacherProfile.objects.get(user=user)
			return data
		except:
			raise forms.ValidationError("Email doesn't exist")
