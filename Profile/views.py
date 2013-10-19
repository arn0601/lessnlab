# Create your views here.
from django.shortcuts import render_to_response,render
from Utils import base_methods,json_helpers
from Utils.data_upload_helpers import getViewableURL
from accounts.models import TeacherProfileAttributes,StudentProfileAttributes
from Utils.models import ModelMapDictionary
from django.contrib.auth import logout

def view_profile(request):
	if base_methods.checkUserIsTeacher(request):
		return show_teacherprofile(request)
	elif base_methods.checkUserIsStudent(request):
		return show_studentprofile(request)
	else:
		logout(request)

def show_studentprofile(request):
	base_dict = base_methods.createStudentDict(request)
	student = StudentProfileAttributes.objects.get(student=base_dict['user'])
	
	base_dict['profile_picture_url'] = getViewableURL(30,base_dict['username']+"_profilepic");
		
	row = ModelMapDictionary.objects.get(model_name="StudentProfileAttributes",attribute_name="bio",app_name="accounts" )
	about_attrs = []
	bio = {}
	bio["model_map_id"] 			= row.id
	bio["id"] 								= student.id
	bio["value"] 							= getattr(student, row.attribute_name)
	bio["humanreadable_name"] = row.humanreadable_name
	bio["istextarea"]						= True
	
	row = ModelMapDictionary.objects.get(model_name="User",attribute_name="email",app_name="auth" )
	email = {}
	email["model_map_id"] 			= row.id
	email["id"] 								= request.user.id
	email["value"] 							= getattr(request.user, row.attribute_name)
	email["humanreadable_name"] = "Email"
	
	about_attrs = []
	about_attrs.append(bio)
	about_attrs.append(email)
	
	base_dict["about_attrs"] 			= about_attrs
	return render(request,"student/student_profile.html",base_dict)
	

def show_teacherprofile(request):
	base_dict = base_methods.createBaseDict(request)
	teacher = TeacherProfileAttributes.objects.get(teacher=base_dict['user'])
	
	base_dict['profile_picture_url'] = getViewableURL(30,base_dict['username']+"_profilepic");

	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="bio",app_name="accounts" )
	about_attrs = []
	bio = {}
	bio["model_map_id"] 			= row.id
	bio["id"] 								= teacher.id
	bio["value"] 							= getattr(teacher, row.attribute_name)
	bio["humanreadable_name"] = row.humanreadable_name
	bio["istextarea"]						= True
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="twitter_handle",app_name="accounts" )
	twitter = {}
	twitter["model_map_id"] 			= row.id
	twitter["id"] 								= teacher.id
	twitter["value"] 							= getattr(teacher, row.attribute_name)
	twitter["humanreadable_name"] = row.humanreadable_name
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="linkedIn_url",app_name="accounts" )
	linked = {}
	linked["model_map_id"] 			= row.id
	linked["id"] 								= teacher.id
	linked["value"] 						= getattr(teacher, row.attribute_name)
	linked["humanreadable_name"] = row.humanreadable_name
	
	row = ModelMapDictionary.objects.get(model_name="User",attribute_name="email",app_name="auth" )
	email = {}
	email["model_map_id"] 			= row.id
	email["id"] 								= request.user.id
	email["value"] 							= getattr(request.user, row.attribute_name)
	email["humanreadable_name"] = "Email"
	
	about_attrs = []
	about_attrs.append(bio)
	about_attrs.append(twitter)
	about_attrs.append(linked)
	about_attrs.append(email)
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="college",app_name="accounts" )
	
	edu = {}
	edu["model_map_id"] 			= row.id
	edu["id"] 								= teacher.id
	edu["value"] 							= getattr(teacher, row.attribute_name)
	edu["humanreadable_name"] = row.humanreadable_name
	edu["istextarea"]					= True
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="gradschool",app_name="accounts" )
	
	gra = {}
	gra["model_map_id"] 			= row.id
	gra["id"] 								= teacher.id
	gra["value"] 							= getattr(teacher, row.attribute_name)
	gra["humanreadable_name"] = row.humanreadable_name
	gra["istextarea"]					= True
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="major",app_name="accounts" )
	
	maj = {}
	maj["model_map_id"] 			= row.id
	maj["id"] 								= teacher.id
	maj["value"] 							= getattr(teacher, row.attribute_name)
	maj["humanreadable_name"] = row.humanreadable_name
	maj["istextarea"]					= True
	
	education_attrs = []
	education_attrs.append(edu)
	education_attrs.append(gra)
	education_attrs.append(maj)
	
	
	row = ModelMapDictionary.objects.get(model_name="TeacherProfileAttributes",attribute_name="skills",app_name="accounts" )
	
	ski = {}
	ski["model_map_id"] 			= row.id
	ski["id"] 								= teacher.id
	ski["value"] 							= getattr(teacher, row.attribute_name)
	ski["humanreadable_name"] = row.humanreadable_name
	ski["istextarea"]					= True
	
	
	skills_attrs = []
	skills_attrs.append(ski)
	
	base_dict["about_attrs"] 			= about_attrs
	base_dict["edu_attrs"] 	=	education_attrs
	base_dict["skills_attrs"] 	=	skills_attrs
	return render(request,"profile.html",base_dict)

def setData(request):
		return json_helpers.setData(request)
