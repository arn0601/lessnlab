from django import forms
import Utils.custom_widgets as custom_widgets
from Units.models import *

class AddUnitForm(forms.ModelForm):
	class Meta:
		model = Unit
		exclude = ['standards', 'cumulative_rating', 'number_raters']
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_start_date'}), 'end_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_end_date'}), 'parent_unit': forms.HiddenInput() }

	def clean(self):
		cleaned_data = super(AddUnitForm, self).clean()
		course = cleaned_data.get("course")
		if (cleaned_data.get("start_date") > cleaned_data.get("end_date")) :

			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be before end date")
		if (cleaned_data.get("start_date") < course.start_date):

			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be after course start date")
		if (cleaned_data.get("end_date") > course.end_date):

			if not self._errors.has_key('end_date'):
		                from django.forms.util import ErrorList
		                self._errors['end_date'] = ErrorList()
			self._errors['end_date'].append("End date should be before course end date")

		return cleaned_data

class EditUnit(forms.ModelForm):
	class Meta:
		model = Unit
		exclude = ['standards', 'cumulative_rating', 'number_raters']
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_start_date'}), 'end_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_end_date'}), 'parent_unit': forms.HiddenInput() }

	def __init__(self, *args, **kwargs):
		super(EditUnit, self).__init__(*args, **kwargs)
		self.fields['owner'].label=''
		self.fields['course'].label=''
		self.fields['parent_unit'].label=''
		self.fields['parent_unit'].initial = None

	def clean(self):
		cleaned_data = super(EditUnit, self).clean()
		course = cleaned_data.get("course")
		if (cleaned_data.get("start_date") > cleaned_data.get("end_date")):

			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be before end date")
		if (cleaned_data.get("start_date") < course.start_date):

			if not self._errors.has_key('start_date'):
		                from django.forms.util import ErrorList
		                self._errors['start_date'] = ErrorList()
			self._errors['start_date'].append("Start date should be after unit start date")
		if (cleaned_data.get("end_date") > course.end_date):

			if not self._errors.has_key('end_date'):
		                from django.forms.util import ErrorList
		                self._errors['end_date'] = ErrorList()
			self._errors['end_date'].append("End date should be before unit end date")

		return cleaned_data

class UnitStandardsForm(forms.Form):
	unit_id = forms.CharField(label='')
	unit_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Select Unit Standards', widget=forms.CheckboxSelectMultiple())

	def __init__(self, *args, **kwargs):
		unit_id = kwargs.pop('unit_id', None)
		super(UnitStandardsForm, self).__init__(*args, **kwargs)
		if unit_id:
			self.fields['unit_id'].initial = unit_id
