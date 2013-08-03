from django import forms
from LessonPlanner.models import *
from Standards.models import *
from Utils import custom_widgets

ACTIVITY_TYPE = [('Group','Group'),('Individual','Individual')]


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

class AddCFUContent(AddContentForm):
	text = forms.CharField(label="Text", max_length=256, widget=forms.Textarea)
	expected_response = forms.CharField(label="Expected Response", max_length=256, widget=forms.Textarea)
	objectives = forms.MultipleChoiceField(label='Select Content Objectives')
	def __init__(self, *args, **kwargs):
                obj_fields = kwargs.pop('objectives', 0)

                super(AddCFUContent, self).__init__(*args, **kwargs)
                self.fields['objectives'].choices = obj_fields


class AddTextContent(AddContentForm):
	text = forms.CharField(label="Text", max_length=256, widget=forms.Textarea)

class AddOnlineVideoContent(AddContentForm):
	link = forms.CharField(label="Add a Link:",required=False)
	recommended_links = custom_widgets.MyCheckboxSelectMultiple(attrs={'class': 'myclass'})
	rl = forms.MultipleChoiceField(label="Add/Search Videos:",widget=recommended_links,required=False,choices=[('0',u'https://www.youtube.com/watch?feature=player_embedded&v=IFKnq9QM6_A')])

class AddActivityContent(forms.ModelForm):
	section = forms.CharField(label="",widget=forms.HiddenInput())
	activity_type = forms.ChoiceField(label='Type', required=True, widget=forms.Select(attrs={'style': 'width: 150px'}))
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
		self.fields['activity_type'].choices = ACTIVITY_TYPE
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
	objectives = forms.MultipleChoiceField(label='Select Content Objectives')
	extra_field_count = forms.CharField(label="",widget=forms.HiddenInput())
	def __init__(self, *args, **kwargs):
	        extra_fields = kwargs.pop('extra', 0)
		obj_fields = kwargs.pop('objectives', 0)

        	super(AddAssessmentContent, self).__init__(*args, **kwargs)
	        self.fields['extra_field_count'].initial = extra_fields
		self.fields['objectives'].choices = obj_fields
	        for index in range(int(extra_fields)):
        	    # generate extra fields in the number specified via extra_fields
	            	self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(label='extra_field_{index}'.format(index=index),required=False)


