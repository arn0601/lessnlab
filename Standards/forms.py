from Types.models import *

class StandardsSearchForm(forms.Form):
	
	standard_type = forms.ChoiceField(label='Type', widget=forms.Select(attrs={'style': 'width: 150px'}))
	state = forms.ChoiceField(label='State', required=False, widget=forms.Select(attrs={'style': 'width: 150px'}))
	grade = forms.ChoiceField(label='Grade', widget=forms.Select(attrs={'style': 'width: 50px'}))
	subject = forms.ChoiceField(label='Subject', widget=forms.Select(attrs={'style': 'width: 150px'}))

	def __init__(self, *args, **kwargs):
		
		super(StandardsSearchForm, self).__init__(*args,**kwargs)
		self.fields['grade'].choices = createChoices(Grade)
		self.fields['grade'].initial = ''

		self.fields['subject'].choices = createChoices(Subject)
		self.fields['subject'].initial = ''

		self.fields['state'].choices = createChoices(State)
		self.fields['state'].initial = ''

		self.fields['standard_type'].choices = createChoices(StandardType)
		self.fields['standard_type'].initial = ''


class StandardAnalysisForm(forms.Form):
	standard_id = forms.CharField(label='')
	standard_id.widget = forms.HiddenInput()
	analysis = forms.CharField(label='Guidance')
	analysis.widget = forms.Textarea()

	def __init__(self, *args, **kwargs):
		standard_id = kwargs.pop('standard_id', None)
		super(StandardAnalysisForm, self).__init__(args, kwargs)
		if standard_id:
			self.fields['standard_id'].initial = standard_id
