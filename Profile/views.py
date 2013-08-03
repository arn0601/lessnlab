# Create your views here.
from django.shortcuts import render_to_response,render
from Utils import base_methods

def view_profile(request):
	base_dict = base_methods.createBaseDict(request)
        return render(request,"profile.html",base_dict)

