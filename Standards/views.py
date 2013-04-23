from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from Standards.models import Standard
from LessonPlanner.models import StandardGrouping
from Objectives.models import Objective
# Create your views here.

def getStandard(request):
	if request.method == 'GET':
		standard_id = request.GET['standard_id']
		try:
			s = Standard.objects.get(id=standard_id)
		except:
			return HttpResponseRedirect('/courses/')
		objectives = Objective.objects.filter(standard=s)
		return render_to_response('standard_view.html', { 'standard':s, 'objectives':objectives})

	return HttpResponseRedirect('/courses/')
