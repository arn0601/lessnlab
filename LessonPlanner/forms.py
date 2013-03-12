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
	assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple(),required=False)
	tags = forms.CharField(label='Tags',required=False)
	courseID = forms.CharField(label="")
        courseID.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Standards', widget=forms.SelectMultiple(), required=False)

	'''def __init__(self, *args, **kwargs):
		standard_choices = kwargs.pop('standard_choices', None)
		super(AddUnitForm, self).__init__(*args, **kwargs)
		if standard_choices:
			self.fields['standards'].choices=standard_choices
	'''

class EditUnit(forms.Form):
	unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()
	name = forms.CharField(label='Unit Name')
        description = forms.CharField(widget=forms.Textarea, label='Description')
        week_length = forms.IntegerField(label='Number of weeks')
        assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple(), required=False)
        tags = forms.CharField(label='Tags',required=False)
        courseID = forms.CharField(label="")
        courseID.widget = forms.HiddenInput()

class DeleteUnit(forms.Form):
        unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()

class AddLessonForm(forms.Form):
        LessonTitle = forms.CharField(label='Lesson Name')
        unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()

class EditLesson(forms.Form):
        lessonID = forms.CharField(label="")
        lessonID.widget = forms.HiddenInput()
	LessonTitle = forms.CharField(label='Unit Name')
	unitID = forms.CharField(label="")
        unitID.widget = forms.HiddenInput()

class DeleteLesson(forms.Form):
        lessonID = forms.CharField(label="")
        lessonID.widget = forms.HiddenInput()
