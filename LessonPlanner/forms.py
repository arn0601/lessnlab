from django import forms
from django.forms.extras.widgets import SelectDateWidget
from LessonPlanner.models import *
from Standards.models import STATE_CHOICES
import custom_widgets 

SUBJECTS = [('Mathematics','Mathematics'),('Science','Science'),('Social Studies','Social Studies')]
SUBJECTS_STRING = '[' + ",".join(["\"%s\"" % s for (s, s2) in SUBJECTS]) + ']'
GRADES = [('7','7'),('8','8'),('9','9'),('Junior High','Junior High')]
GRADES_STRING = '[' + ",".join(["\"%s\"" % s for (s, s2) in GRADES]) + ']'

class AddCourse(forms.ModelForm):
	subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
	subject.widget = forms.TextInput(attrs={'data-provide':'typeahead', 'data-source': SUBJECTS_STRING, 'autocomplete':'off' })
	grade = forms.ChoiceField(label='Grade', choices = GRADES)
	grade.widget = forms.TextInput(attrs={'data-provide':'typeahead', 'data-source': GRADES_STRING, 'autocomplete':'off' })
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': SelectDateWidget(years=range(2015,2011,-1)), 'end_date': SelectDateWidget(years=range(2015,2011,-1)) }
		exclude = ['standard_grouping']

class AddGroups(forms.Form):
	groups = forms.MultipleChoiceField(label='Standards groups')
	course_id = forms.ChoiceField(label='')
	course_id.widget = forms.HiddenInput()

class EditCourse(forms.ModelForm):
	subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
	grade = forms.ChoiceField(label='Grade', choices = GRADES)
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': SelectDateWidget(years=range(2015,2011,-1)), 'end_date': SelectDateWidget(years=range(2015,2011,-1)) }
		exclude = ['standard_grouping']

class DeleteCourse(forms.Form):
	course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()

class AddUnitForm(forms.ModelForm):
	class Meta:
		model = Unit
		exclude = ['standards']
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': SelectDateWidget(years=range(2015,2011,-1)), 'end_date': SelectDateWidget(years=range(2015,2011,-1)), 'parent_unit': forms.HiddenInput() }

class EditUnit(forms.ModelForm):
	class Meta:
		model = Unit
		exclude = ['standards']
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': SelectDateWidget(years=range(2015,2011,-1)), 'end_date': SelectDateWidget(years=range(2015,2011,-1)), 'parent_unit': forms.HiddenInput() }

class DeleteUnit(forms.Form):
	unit_id = forms.CharField(label="")
	unit_id.widget = forms.HiddenInput()

class AddLessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards','objectives']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput() }

class EditLesson(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards', 'objectives']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput() }

class DeleteLesson(forms.Form):
	lesson_id = forms.CharField(label="")
	lesson_id.widget = forms.HiddenInput()

class AddSectionForm(forms.ModelForm):
	class Meta:
		model = Section
		widgets = { 'lesson': forms.HiddenInput() , 'owner': forms.HiddenInput(), 'placement': forms.HiddenInput(), 'creation_date': forms.HiddenInput() }

class DeleteSection(forms.Form):
	section_id = forms.CharField(label="")
	section_id.widget = forms.HiddenInput()

class DeleteContent(forms.Form):
	content_id = forms.CharField(label="")
	content_id.widget = forms.HiddenInput()


class AddContentForm(forms.Form):
	section_id = forms.CharField(label="")
	section_id.widget = forms.HiddenInput()
	content_type = forms.CharField(label="")
	content_type.widget = forms.HiddenInput()

class AddTextContent(AddContentForm):
	text = forms.CharField(label="Text", max_length=256, widget=forms.Textarea)

class AddOnlineVideoContent(AddContentForm):
	link = forms.CharField(label="Link",required=False)
	recommended_links = custom_widgets.MyCheckboxSelectMultiple(attrs={'class': 'myclass'})
	rl = forms.MultipleChoiceField(label="Add Recommended Videos:",widget=recommended_links,choices=(('http://www.youtube.com/embed/ImAMVqA6mug','0'),('http://www.youtube.com/embed/ImAMVqA6mug','1')),required=False)


class AddOnlineArticleContent(AddContentForm):
	link = forms.CharField(label="Link")

class AddTeacherNoteContent(AddContentForm):
        text = forms.CharField(label="Text", max_length=256, widget=forms.Textarea)

class AddAdministratorNoteContent(AddContentForm):
        text = forms.CharField(label="Text", max_length=256, widget=forms.Textarea)

class AddOnlinePictureContent(AddContentForm):
        link = forms.CharField(label="Link")

class AddAssessmentContent(AddContentForm):
        title = forms.CharField(label="Title")
	extra_field_count = forms.CharField(label="",widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
	        extra_fields = kwargs.pop('extra', 0)

        	super(AddAssessmentContent, self).__init__(*args, **kwargs)
	        self.fields['extra_field_count'].initial = extra_fields
	        for index in range(int(extra_fields)):
        	    # generate extra fields in the number specified via extra_fields
	            	self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(label='extra_field_{index}'.format(index=index),required=False)

class UnitStandardsForm(forms.Form):
	unit_id = forms.CharField(label='')
	unit_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Select Unit Standards')


class LessonStandardsForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standards = forms.MultipleChoiceField(label='Select Unit Standards')

class SelectStandardsForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standard = forms.ChoiceField(label='Select Standard')
	
class CreateObjectivesForm(forms.Form):
	lesson_id = forms.CharField(label='')
	lesson_id.widget = forms.HiddenInput()
	standard_id = forms.CharField(label='')
	standard_id.widget = forms.HiddenInput()
	created = forms.MultipleChoiceField(label='Choose from created objectives', required=False)
	new_objectives_count = forms.CharField(label='', widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		extra_fields = kwargs.pop('extra', 0)
		super(CreateObjectivesForm, self).__init__(*args, **kwargs)
		self.fields['new_objectives_count'].initial = extra_fields
		for index in range(int(extra_fields)):
			self.fields['new_objective_{index}'.format(index=index)] = forms.CharField(label='New Objective {index}'.format(index=index),required=False)

class StandardsSearchForm(forms.Form):
	state = forms.ChoiceField(label='State', choices=STATE_CHOICES)
	subject = forms.ChoiceField(label='Subject', choices=SUBJECTS)
	grade = forms.ChoiceField(label='Grade', choices=GRADES)
