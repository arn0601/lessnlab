from django import forms
import Utils.custom_widgets as custom_widgets
from Courses.models import *
from accounts.models import TeacherProfile

class AddCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters', 'parent']
	
	def __init__(self, *args, **kwargs):
		subject = kwargs.pop('subject', None)
		owner = kwargs.pop('teacher', None)
		grade = kwargs.pop('grade', None)
		super(AddCourse, self).__init__(*args,**kwargs)
		self.fields['owner'].label=''
		if grade:
			self.fields['grade'].initial = grade
		if owner:
			self.fields['owner'].initial = owner
		if subject:
			self.fields['subject'].initial = subject



class AddGroups(forms.Form):
	groups = forms.MultipleChoiceField(label='Standards groups')
	course_id = forms.ChoiceField(label='')
	course_id.widget = forms.HiddenInput()

class EditCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = {  'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters', 'state', 'parent']

class DeleteCourse(forms.Form):
	course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()


class TeacherRequestForm(forms.Form):
	email = forms.CharField(label='Teacher Email')

class ClassRequestForm(forms.Form):
	teacher_id = forms.CharField(label='')
	teacher_id.widget = forms.HiddenInput()
	classes = forms.MultipleChoiceField(label='Choose classes')

	def __init__(self, *args, **kwargs):
		teacher_id = kwargs.pop(teacher_id, None)
		super(ClassRequestForm, self).__init__(*args, **kwargs)
		if teacher_id:
			course_request.fields['teacher_id'].initial = teacher_id

class RecommendCourseParametersForm(forms.Form):
	state = forms.ModelChoiceField(queryset=State.objects.all(), label='State')
	grade = forms.ModelChoiceField(queryset=Grade.objects.all(), label='Grade')
	subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject')

	
