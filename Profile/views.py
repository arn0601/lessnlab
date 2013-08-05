# Create your views here.
from django.shortcuts import render_to_response,render
from Utils import base_methods,json_helpers
from accounts.models import TeacherProfileAttributes
from Utils.models import ModelMapDictionary

def view_profile(request):
	base_dict = base_methods.createBaseDict(request)
	teacher = TeacherProfileAttributes.objects.get(teacher=base_dict['user'])
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="bio",app_name="accounts" )
	
	about_attrs = []
	bio = {}
	bio["model_map_id"] 			= row.id
	bio["id"] 								= teacher.id
	bio["value"] 							= getattr(teacher, 'bio')
	bio["humanreadable_name"] = teacher._meta.get_field('bio').verbose_name
	
	about_attrs.append(bio)
	education_attrs = []
	skills_attrs = []
	
	base_dict["about_attrs"] = about_attrs
	return render(request,"profile.html",base_dict)

def setData(request):
		return json_helpers.setData(request)