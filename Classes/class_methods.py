from Classes.models import *
from accounts.models import *
import sys

def getClassesAndStudentInformation(user):
	classInfo = {}
	classInfo['CourseClassInfo'] = {}
	classInfo['ClassStudents'] = {}
        try:
		courses = Course.objects.filter(owner=user)
		if not courses:
			return classInfo
                for c in courses:
			classInfo['CourseClassInfo'][c] = []
			allClasses = Class.objects.filter(course=c)
			if not allClasses:
				continue
			for cl in allClasses:
				students = ClassStudents.objects.filter(course_class=cl).order_by("approved")
				print students
				classInfo['ClassStudents'][cl] = students
                		classInfo['CourseClassInfo'][c].append(cl)
		return classInfo
        except:
		print sys.exc_info()[0]
                return classInfo

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
