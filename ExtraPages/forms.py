from django import forms
class CreateObjectivesPoolForm(forms.Form):
        standard_id = forms.CharField(label='')
        standard_id.widget = forms.HiddenInput()
        new_objectives_count = forms.CharField(label='', widget=forms.HiddenInput())

        def __init__(self, *args, **kwargs):
                standard_id = kwargs.pop('standard_id', None)
                extra_fields = kwargs.pop('extra', 0)
                super(CreateObjectivesPoolForm, self).__init__(*args, **kwargs)
                self.fields['new_objectives_count'].initial = extra_fields
                print self.fields['new_objectives_count'].initial, "initial"
                for index in range(int(extra_fields)):
                        self.fields['new_objective_{index}'.format(index=index)] = forms.CharField(label='New Objective {index}'.format(index=index),required=False,widget=forms.Textarea(attrs={'rows':4, 'cols':25}))
                if standard_id:
                        self.fields['standard_id'].initial = standard_id

class CreateMultipleChoiceQuestion(forms.Form):
	objective_id = forms.CharField(label='')
	objective_id.widget = forms.HiddenInput()
	question = forms.CharField(label='Question',  widget=forms.Textarea(attrs={'rows':4, 'cols':25, 'class':'extrapage'}))
	new_answer_count = forms.CharField(label='', widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
		objective_id = kwargs.pop('objective_id',None)
		new_fields = kwargs.pop('new_answer_count', 0)
		super(CreateMultipleChoiceQuestion, self).__init__(*args, **kwargs)
		self.fields['new_answer_count'].initial = new_fields
		print new_fields
		for index in range(int(new_fields)):
			self.fields['new_answer_{index}'.format(index=index)] = forms.CharField(label='New Answer {index}'.format(index=index,required=False), widget=forms.Textarea(attrs={'rows':4, 'cols':25, 'class':'extrapage'}))
		if objective_id:
			self.fields['objective_id'].initial = objective_id


class CreateFreeResponseQuestion(forms.Form):
	objective_id = forms.CharField(label='')
	objective_id.widget = forms.HiddenInput()
	question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'rows':4, 'cols':25, 'class':'extrapage'}))
	answer = forms.CharField(label='Answer', widget=forms.Textarea(attrs={'cols':25, 'rows':4, 'class':'extrapage'}))
	def __init__(self, *args, **kwargs):
		objective_id = kwargs.pop('objective_id',None)
		super(CreateFreeResponseQuestion, self).__init__(*args, **kwargs)
		if objective_id:
			self.fields['objective_id'].initial = objective_id
		
