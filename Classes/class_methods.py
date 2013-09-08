from Classes.models import *
from accounts.models import *

def getClassStudents(class_):
	try:
		students = ClassStudents.objects.filter(course_class=class_).order_by("approved")
		return students
	except:
		return None

def getClassInfo(class_):
	class_dict = {}
	students = getClassStudents(class_)
	class_dict['classStudents'] = students
	return class_dict
