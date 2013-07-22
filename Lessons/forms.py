from django import forms
from Lessons.models import *
import Utils.custom_widgets as custom_widgets

class AddLessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards','objectives', 'cumulative_rating', 'number_raters']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput(),'start_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'lesson_start_date'}), 'end_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'lesson_end_date'})}

class EditLesson(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards', 'objectives', 'cumulative_rating', 'number_raters']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput(),'start_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'lesson_start_date'}), 'end_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'lesson_end_date'}) }

	def __init__(self, *args, **kwargs):
		super(EditLesson, self).__init__(*args, **kwargs)
		self.fields['owner'].label=''
		self.fields['unit'].label=''

class DeleteLesson(forms.Form):
	lesson_id = forms.CharField(label="")
	lesson_id.widget = forms.HiddenInput()

	def __init__(self, *args, **kwargs):
		lesson_id = kwargs.pop('lesson_id', None)
		super(DeleteLesson, self).__init__(*args,**kwargs)
		if lesson_id:
	        	self.fields["lesson_id"].initial = lesson_id


class LessonStandardsForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Select Lesson Standards')

	def __init__(self, *args, **kwargs):
		lesson_id = kwargs.pop('lesson_id', None)
		super(LessonStandardsForm, self).__init__(*args, **kwargs)
		if lesson_id:
			self.fields['lesson_id'].initial = lesson_id


class SelectStandardsForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standard = forms.ChoiceField(label='Select Standard')
	
	def __init__(self, *args, **kwargs):
		lesson_id = kwargs.pop('lesson_id', None)
		super(SelectStandardsForm, self).__init__(*args, **kwargs)
		if lesson_id:
			self.fields['lesson_id'].initial = lesson_id

class CreateObjectivesForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standard_id = forms.CharField(label='')
	standard_id.widget = forms.HiddenInput()
	created = forms.MultipleChoiceField(label='Choose from created objectives', required=False)
	new_objectives_count = forms.CharField(label='', widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		standard_id = kwargs.pop('standard_id', None)
		lesson_id = kwargs.pop('lesson_id', None)
		extra_fields = kwargs.pop('extra', 0)
		super(CreateObjectivesForm, self).__init__(*args, **kwargs)
		self.fields['new_objectives_count'].initial = extra_fields
		print self.fields['new_objectives_count'].initial, "initial"
		for index in range(int(extra_fields)):
			self.fields['new_objective_{index}'.format(index=index)] = forms.CharField(label='New Objective {index}'.format(index=index),required=False)
		if standard_id:
			self.fields['standard_id'].initial = standard_id
		if lesson_id:
			self.fields['lesson_id'].initial = lesson_id
