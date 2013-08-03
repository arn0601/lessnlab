from django import forms
import Utils.custom_widgets as custom_widgets
from Units.models import *

class AddUnitForm(forms.ModelForm):
	class Meta:
		model = Unit
		exclude = ['standards', 'cumulative_rating', 'number_raters']
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_start_date'}), 'end_date': custom_widgets.CalendarDateSelectField(attrs={'id': 'unit_end_date'}), 'parent_unit': forms.HiddenInput() }

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

class UnitStandardsForm(forms.Form):
	unit_id = forms.CharField(label='')
	unit_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Select Unit Standards')

	def __init__(self, *args, **kwargs):
		unit_id = kwargs.pop('unit_id', None)
		super(UnitStandardsForm, self).__init__(*args, **kwargs)
		if unit_id:
			self.fields['unit_id'].initial = unit_id
