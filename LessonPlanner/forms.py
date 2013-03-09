from django import forms

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))

class AddCourse(forms.Form):
	
	name = forms.CharField(label='Course Name')
	department = forms.CharField(label='Department')
	year = forms.IntegerField(label='Year')


class EditCourse(forms.Form):
        courseID = forms.CharField(label="")
	courseID.widget = forms.HiddenInput()
        name = forms.CharField(label='Course Name')
        department = forms.CharField(label='Department')
        year = forms.IntegerField(label='Year')

class DeleteCourse(forms.Form):
        courseID = forms.CharField(label="")
        courseID.widget = forms.HiddenInput()

class AddUnitForm(forms.Form):
	name = forms.CharField(label='Unit Name')
	description = forms.CharField(widget=forms.Textarea, label='Description')
	week_length = forms.IntegerField(label='Number of weeks')		
	assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple(),blank=True)
	tags = forms.CharField(label='Tags',blank=True)
	courseID = forms.CharField(label="")
        courseID.widget = forms.HiddenInput()

class EditUnit(forms.Form):
	unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()
	name = forms.CharField(label='Unit Name')
        description = forms.CharField(widget=forms.Textarea, label='Description')
        week_length = forms.IntegerField(label='Number of weeks')
        assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple())
        tags = forms.CharField(label='Tags')
        courseID = forms.CharField(label="")
        courseID.widget = forms.HiddenInput()

class DeleteUnit(forms.Form):
        unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()

