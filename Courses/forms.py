from django import forms
from django.contrib.auth.models import User
import Utils.custom_widgets as custom_widgets
from Courses.models import *
from accounts.models import TeacherProfile
from Classes.models import Class

class AddCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters', 'parent']
	
	def __init__(self, *args, **kwargs):
		subject = kwargs.pop('subject', None)
		owner = kwargs.pop('teacher', None)
		grade = kwargs.pop('grade', None)
		super(AddCourse, self).__init__(*args,**kwargs)
		self.fields['owner'].label=''
		if grade:
			self.fields['grade'].initial = grade
		if owner:
			self.fields['owner'].initial = owner
		if subject:
			self.fields['subject'].initial = subject

	def clean(self):
		cleaned_data = super(AddCourse, self).clean()
		if (cleaned_data.get('start_date') > cleaned_data.get('end_date')):
			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be before end date")
		return cleaned_data


class AddGroups(forms.Form):
	groups = forms.MultipleChoiceField(label='Standards groups')
	course_id = forms.ChoiceField(label='')
	course_id.widget = forms.HiddenInput()

class EditCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = {  'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters', 'state', 'parent']

        def clean(self):
                cleaned_data = super(EditCourse, self).clean()
                if (cleaned_data.get('start_date') > cleaned_data.get('end_date')):
			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be before end date")
                return cleaned_data


class DeleteCourse(forms.Form):
	course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()




class RecommendCourseParametersForm(forms.Form):
	state = forms.ModelChoiceField(queryset=State.objects.all(), label='State')
	grade = forms.ModelChoiceField(queryset=Grade.objects.all(), label='Grade')
	subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject')

	
