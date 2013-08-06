from Types.models import *
from django import forms

def createChoices(className):
	choices = [(c.value,c.value) for c in className.objects.all()]
        choices.insert(0,('',''))
	return choices

def createDataSource(className):
	return '[' + ",".join(["\"%s\"" % c.value for c in className.objects.all()]) + ']'

def getInstanceFromField(className, field):
	v, created = className.objects.get_or_create(value=field)
	return v	

def createInputWidget(className):
	return forms.TextInput(attrs={'data-provide':'typeahead', 'data-source': createDataSource(className), 'autocomplete':'off' })
	
class StandardsSearchForm(forms.Form):
	
	standard_type = forms.ModelChoiceField(queryset=StandardType.objects.all(), label='Type', widget=forms.Select(attrs={'style': 'width: 150px'}))
	state = forms.ModelChoiceField(queryset=State.objects.all(), label='State', required=False, widget=forms.Select(attrs={'style': 'width: 150px'}))
	grade = forms.ModelChoiceField(queryset=Grade.objects.all(), label='Grade', widget=forms.Select(attrs={'style': 'width: 50px'}))
	subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject', widget=forms.Select(attrs={'style': 'width: 150px'}))

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
