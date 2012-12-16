# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


@csrf_exempt
def login_user(request):
	state = "Please log in below"
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "Successfully logged in"
				return HttpResponseRedirect('/lessons/')
			else:
				state = "Your account isnt active"
		else:
			state = "Something is incorrect"
	return render_to_response('auth.html', {'state':state, 'username':username, 'password':password})

