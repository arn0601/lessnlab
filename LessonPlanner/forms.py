from django import forms
from django.forms.extras.widgets import SelectDateWidget
from LessonPlanner.models import *

class AddCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': SelectDateWidget(years=range(2000,1939,-1)), 'end_date': SelectDateWidget(years=range(2000,1939,-1)) }
		exclude = ['standard_grouping']

class EditCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': SelectDateWidget(years=range(2000,1939,-1)), 'end_date': SelectDateWidget(years=range(2000,1939,-1)) }
		exclude = ['standard_grouping']

class DeleteCourse(forms.Form):
	course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()

class AddUnitForm(forms.ModelForm):
	class Meta:
		model = Unit
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': SelectDateWidget(years=range(2000,1939,-1)), 'end_date': SelectDateWidget(years=range(2000,1939,-1)), 'parent_unit': forms.HiddenInput() }

class EditUnit(forms.ModelForm):
	class Meta:
		model = Unit
		widgets = {'course': forms.HiddenInput(), 'owner': forms.HiddenInput() , 'start_date': SelectDateWidget(years=range(2000,1939,-1)), 'end_date': SelectDateWidget(years=range(2000,1939,-1)), 'parent_unit': forms.HiddenInput() }

class DeleteUnit(forms.Form):
	unit_id = forms.CharField(label="")
	unit_id.widget = forms.HiddenInput()

class AddLessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput() }

class EditLesson(forms.ModelForm):
	class Meta:
		model = Lesson
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
	link = forms.CharField(label="Link")

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

class CourseStandardsForm(forms.Form):
	course_id = forms.CharField(label='')
	course_id.widget = forms.HiddenInput()
	groups = forms.MultipleChoiceField(label='Select Standards Group')
