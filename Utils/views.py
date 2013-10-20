# Create your views here.
from django.shortcuts import render_to_response,render
from Utils import base_methods,json_helpers, data_upload_helpers
from accounts.models import TeacherProfileAttributes,StudentProfileAttributes
from Utils.models import ModelMapDictionary
from django.contrib.auth import logout
from django.http import HttpResponse


def setData(request):
    return json_helpers.setData(request)

def getPrivateUrl(request):
    return json_helpers.getViewableURL_JSON(request)


def uploadData(request):
    return data_upload_helpers.uploadData(request)
