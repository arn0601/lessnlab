from django import forms
from django.forms.extras.widgets import SelectDateWidget
from LessonPlanner.models import *
from Standards.models import *
import custom_widgets 

SUBJECTS = [('Mathematics','Mathematics'),('Science','Science'),('English','English')]
SUBJECTS_STRING = '[' + ",".join(["\"%s\"" % s for (s, s2) in SUBJECTS]) + ']'
GRADES = [('K','K'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12')]
GRADES_STRING = '[' + ",".join(["\"%s\"" % s for (s, s2) in GRADES]) + ']'

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
	

class AddCourse(forms.ModelForm):
	class Meta:
		model = Course
		widgets = { 'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters']


class AddGroups(forms.Form):
	groups = forms.MultipleChoiceField(label='Standards groups')
	course_id = forms.ChoiceField(label='')
	course_id.widget = forms.HiddenInput()

class EditCourse(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditCourse, self).__init__(*args,**kwargs)

	
		self.fields['grade'].choices = createChoices(Grade)
		self.fields['grade'].widget = createInputWidget(Grade)

		self.fields['subject'].choices = createChoices(Subject)
		self.fields['subject'].widget = createInputWidget(Subject)

	def save(self):
		self.instance.grade = getInstanceFromField(Grade, self.cleaned_data['grade'])
		self.instance.subject = getInstanceFromField(Subject, self.cleaned_data['subject'])
		return super(EditCourse, self).save()
	
	class Meta:
		model = Course
		widgets = {  'owner': forms.HiddenInput(), 'start_date': custom_widgets.CalendarDateSelectField(), 'end_date': custom_widgets.CalendarDateSelectField() }
		exclude = ['standard_grouping', 'cumulative_rating', 'number_raters']

class DeleteCourse(forms.Form):
	course_id = forms.CharField(label="")
	course_id.widget = forms.HiddenInput()

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

class AddLessonForm(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards','objectives', 'cumulative_rating', 'number_raters']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput() }

class EditLesson(forms.ModelForm):
	class Meta:
		model = Lesson
		exclude = ['standards', 'objectives', 'cumulative_rating', 'number_raters']
		widgets = { 'unit': forms.HiddenInput() , 'owner': forms.HiddenInput() }

class DeleteLesson(forms.Form):
	lesson_id = forms.CharField(label="")
	lesson_id.widget = forms.HiddenInput()

class AddSectionForm(forms.ModelForm):
	class Meta:
		model = Section
		exclude = ['standards','objectives', 'cumulative_rating', 'number_raters']
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
	link = forms.CharField(label="Add a Link:",required=False)
	recommended_links = custom_widgets.MyCheckboxSelectMultiple(attrs={'class': 'myclass'})
	rl = forms.MultipleChoiceField(label="Add/Search Videos:",widget=recommended_links,required=False,choices=[('0',u'https://www.youtube.com/watch?feature=player_embedded&v=IFKnq9QM6_A')])

class AddActivityContent(forms.ModelForm):
	section = forms.CharField(label="",widget=forms.HiddenInput())
	class Meta:
		exclude = ['standards','objectives', 'cumulative_rating', 'number_raters','owner']
                model = ActivityContent
          	widgets = {'creation_date' : custom_widgets.CalendarDateSelectField(attrs={'id': 'activity_creation_date'}), 'placement' : forms.HiddenInput(), 'content_type': forms.HiddenInput() }	
	def clean_section(self):
		try:
			return Section.objects.get(id=self.cleaned_data["section"])
		except:
			raise django.Forms.ValidationError("Section does not exist")
		return data
	def __init__(self, *args, **kwargs):
                super(AddActivityContent, self).__init__(*args, **kwargs)
                self.fields['placement'].label = ""
		self.fields['content_type'].label = ""


class AddPowerPointContent(AddContentForm):
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

class TeacherRequestForm(forms.Form):
	email = forms.CharField(label='Teacher Email')

class CourseRequestForm(forms.Form):
	teacher_id = forms.CharField(label='')
	teacher_id.widget = forms.HiddenInput()
	courses = forms.MultipleChoiceField(label='Choose courses')

class StandardAnalysisForm(forms.Form):
	standard_id = forms.CharField(label='')
	standard_id.widget = forms.HiddenInput()
	analysis = forms.CharField(label='Guidance')
	analysis.widget = forms.Textarea()
