from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from Standards.models import Standard
from LessonPlanner.models import StandardGrouping
from Objectives.models import Objective
# Create your views here.

