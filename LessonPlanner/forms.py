from django import forms

class AddCourse(forms.Form):
	name = forms.CharField(label='Course Name')
	department = forms.CharField(label='Department')
	year = forms.IntegerField(label='Year')

