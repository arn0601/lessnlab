from Classes.models import *
import class_methods
from Utils import base_methods
from Utils.ajax_helpers import direct_json_to_template
import simplejson
from Classes.forms import *
from Courses.models import *
from accounts.models import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def editClassStudents(request):
	if request.method == 'POST':
		cid = request.POST['class_id']
		try:
			class_ = Class.objects.get(id=cid)
		except:
			return HttpResponse(simplejson.dumps({'success':'1'}))
		student_id = request.POST.get('student_id')
		student = StudentProfile.objects.get(user__id__exact=student_id)
		action = request.POST.get('action')
		if action =='D':
			cs = ClassStudents.objects.get(student=student, course_class=class_)
			cs.delete()
		elif action=='A':
			cs = ClassStudents.objects.get(student=student, course_class=class_)
			cs.approved = True
			cs.save()
		student_list = (class_methods.getClassStudents(class_)).order_by('approved')
		context = {'classStudents': student_list}
		return direct_json_to_template(request, "manage_students.html", "manage_students", context, {'success':'1'})

def addClass(request):
	if request.method == 'POST':
		teacher = base_methods.checkUserIsTeacher(request)
		if teacher == None:
			logout(request)
			return HttpResponse(simplejson.dumps({'success':'0'}))
		addClassForm = AddClassForm(data=request.POST)
		if addClassForm.is_valid():
			addClassForm.save()
			return HttpResponse(simplejson.dumps({'success':'1'}))
		else:
			context = {'addClassForm':addClassForm}
			return direct_json_to_template(request, 'class_add_form.html', 'addClassForm', context, {'success':'0'})
	else:
		return HttpResponse(simplejson.dumps({'success':'0'}))

def requestAddClassForm(request):
	if request.method == 'POST':
		course_id = request.POST.get('course_id')
		try:
			course = Course.objects.get(id=course_id)
		except:
			return HttpResponse(simplejson.dumps({'success':'0'}))
		teacher = base_methods.checkUserIsTeacher(request)
		if teacher == None:
			logout(request)
			return HttpResponse(simplejson.dumps({'success':'0'}))
		else:
			acf = AddClassForm()
			acf.fields['course'].initial = course
			context = {'addClassForm':acf}
			return direct_json_to_template(request, 'class_add_form.html', 'addClassForm', context, {'success':'1'})
	else:
		return HttpResponse(simplejson.dumps({'success':'0'}))

def showClasses(request):
	if base_methods.checkUserIsTeacher(request):
		base_dict = base_methods.createBaseDict(request)
		return render(request, "classes.html", base_dict)
	elif base_methods.checkUserIsStudent(request):
		student_dict = base_methods.createStudentDict(request)	
		return render(request, "student_classes.html", student_dict)
	else:
		return HttpResponseRedirect('/')

def showClass(request):
	class_id = request.GET.get('class_id')
	print class_id
	try:
		class_ = Class.objects.get(id=class_id)
	except:
		return HttpResponseRedirect('/classes/')
	class_dict = class_methods.getClassInfo(class_)
	for cs in class_dict['classStudents']:
		print cs.student.user.first_name
	base_dict = base_methods.createBaseDict(request)
	base_dict.update(class_dict)
	return render(request, "class.html", base_dict)


def studentRequestClass(request):
	if not base_methods.checkUserIsStudent(request):
		return HttpResponse(simplejson.dumps({'success':'0'}))
	teacher_request = TeacherRequestForm(data=request.POST)
	if teacher_request.is_valid():
		generic_user = User.objects.get(email=teacher_request.data['email'])
		teacher = TeacherProfile.objects.get(user=generic_user)
		course_request = ClassRequestForm(teacher=teacher)
		classes = Class.objects.filter(course__owner__exact=teacher)
		course_request.fields['classes'].queryset = classes
		base_dict = {'classesForm':course_request}
		x = direct_json_to_template(request,'student_choose_courses.html', 'choose_course_form', base_dict, {'success':'1'})
		return x
	else:
		return HttpResponse(simplejson.dumps({'success':'0'}))

def studentAddClass(request):
	classRequestForm = ClassRequestForm(data=request.POST)
	teacher_id = classRequestForm.data['teacher']
	try:
		teacher = TeacherProfile.objects.get(id=teacher_id)
		student = StudentProfile.objects.get(user=request.user)
	except:
		return HttpResponseRedirect('/classes/')
	
	classes = Class.objects.filter(course__owner__exact=teacher)
	classRequestForm.fields['classes'].queryset = classes
	if classRequestForm.is_valid():
		try:
			for course_class in classRequestForm.cleaned_data['classes']:
				cs_exists = ClassStudents.objects.filter(student=student, course_class=course_class)
				if cs_exists and len(cs_exists) > 0:
					return HttpResponseRedirect('/classes/')
				cs = ClassStudents()
				cs.course_class = course_class
				cs.student = student
				cs.approved = False
				cs.save()
			return HttpResponseRedirect('/classes/')
		except:
			return HttpResponseRedirect(request.session['last_page'])
	else:	
		return HttpResponseRedirect(request.session['last_page'])
