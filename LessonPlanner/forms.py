from django import forms

ASSESSMENTTYPE = ((1, 'Quiz'), (2, 'Unit Test'), (3, 'Complex Performance Task'), (4, 'Peer Eval'), (5, 'Presentation/Project'), (6, 'Other'))

class AddCourse(forms.Form):
	
	name = forms.CharField(label='Course Name')
	department = forms.CharField(label='Department')
	year = forms.IntegerField(label='Year')


class EditCourse(forms.Form):
        course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()
        name = forms.CharField(label='Course Name')
        department = forms.CharField(label='Department')
        year = forms.IntegerField(label='Year')

class DeleteCourse(forms.Form):
        course_id = forms.CharField(label="")
        course_id.widget = forms.HiddenInput()

class AddUnitForm(forms.Form):
	name = forms.CharField(label='Unit Name')
	description = forms.CharField(widget=forms.Textarea, label='Description')
	week_length = forms.IntegerField(label='Number of weeks')		
	assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple(),required=False)
	tags = forms.CharField(label='Tags',required=False)
	course_id = forms.CharField(label="")
        course_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Standards', widget=forms.SelectMultiple(), required=False)

	'''def __init__(self, *args, **kwargs):
		standard_choices = kwargs.pop('standard_choices', None)
		super(AddUnitForm, self).__init__(*args, **kwargs)
		if standard_choices:
			self.fields['standards'].choices=standard_choices
	'''

class EditUnit(forms.Form):
	unit_id = forms.CharField(label="")
        unit_id.widget = forms.HiddenInput()
	name = forms.CharField(label='Unit Name')
        description = forms.CharField(widget=forms.Textarea, label='Description')
        week_length = forms.IntegerField(label='Number of weeks')
        assessments = forms.MultipleChoiceField(label='Assessment Type', choices=ASSESSMENTTYPE, widget=forms.CheckboxSelectMultiple(), required=False)
        tags = forms.CharField(label='Tags',required=False)
        course_id = forms.CharField(label="")
        course_id.widget = forms.HiddenInput()

class DeleteUnit(forms.Form):
        unit_id = forms.CharField(label="")
        unit_id.widget = forms.HiddenInput()

class AddLessonForm(forms.Form):
        name = forms.CharField(label='Lesson Name')
        unit_id = forms.CharField(label="")
        unit_id.widget = forms.HiddenInput()

class EditLesson(forms.Form):
        lesson_id = forms.CharField(label="")
        lesson_id.widget = forms.HiddenInput()
	name = forms.CharField(label='Unit Name')
	unit_id = forms.CharField(label="")
        unit_id.widget = forms.HiddenInput()

class DeleteLesson(forms.Form):
        lesson_id = forms.CharField(label="")
        lesson_id.widget = forms.HiddenInput()
