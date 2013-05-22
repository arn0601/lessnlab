# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
from registration.backends import get_backend
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.forms import *
@csrf_exempt
def logout_user(request):
	logout(request)	
	return HttpResponseRedirect('/')

def validateLoginArgs(request):
	if request.POST:
		username = request.POST['username']
    		password = request.POST['password']
	    	user = authenticate(username=username, password=password)
		return user
	else:
		return None

@csrf_exempt
def login_user(request):
	user = validateLoginArgs(request)
       	if user is not None:
       		if user.is_active:
      			login(request, user)
			return HttpResponseRedirect('/courses/')
        		
            			# Return a 'disabled account' error message
	return HttpResponseRedirect('/')


def registerStudent(request, backend, success_url=None, form_class=None,
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
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

@csrf_exempt
def validateRegisterTeacher(request):
    print request.POST
    form = TeacherRegistrationForm(data=request.POST)
    if form.is_valid():
        return HttpResponse('')
    else:
	print form.errors
        return render_to_response('form_errors.html', { 'form' : form })

@csrf_exempt
def validateLogin(request):
	print request.POST
	user = validateLoginArgs(request)
	if user is not None:
		return HttpResponse('')
	else:
		return HttpResponse('Invalid Login Credentials')

@csrf_exempt
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
