# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


from django.contrib.auth import logout

def logout_view(request):
    logout(request)


from django.contrib.auth.decorators import login_required

@csrf_exempt
def login_user(request):
        print 'login user'
	if request.POST:
		username = request.POST['username']
    		password = request.POST['password']
	    	user = authenticate(username=username, password=password)
	        print username,password,'HERERER'
        	if user is not None:
        		if user.is_active:
            			login(request, user)
				return HttpResponseRedirect('/lessons/')
        		
            			# Return a 'disabled account' error message
    		else:
			error = "Invalid User Credentials"
                        print 'invalid cred'
        		return render_to_response('registration/login.html', {'errors':error, 'username':username, 'password':password})
			# Return an 'invalid login' error message.
	else:
                print "login really try this"
		return render_to_response('registration/login.html')


