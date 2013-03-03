from django import forms

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
