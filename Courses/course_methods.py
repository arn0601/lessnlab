from Courses.models import Course
from Classes.models import Class, ClassStudents
from Units import unit_methods
from Units.models import Unit
from Standards.models import Standard
import sets

#returns a list of students taking course
def getStudentsTaking(course):
	cs = ClassStudents.objects.filter(course_class__course__exact=course)
	student_list = []
	for item in cs:
		student_list.append(item.student)
	return student_list

#returns a set of child courses of this set
def getCourseClones(course):
	children = Course.objects.filter(parent=course)
	child_set = sets.Set()
	if children and len(children) > 0:
		for child in children:
			child_set = child_set.union(getClonesOfCourse(child))
	return child_set

def getCourseInfo(course):
	course_dict = {}
	course_dict['studentsTaking'] = getStudentsTaking(course)
	course_dict['courseClones'] = getCourseClones(course)
	course_units = Unit.objects.filter(course=course).order_by('start_date')
	course_dict['courseUnits'] = course_units
	
	#course length
	course_delta = (course.end_date - course.start_date)
	course_dict['courseLength']=(course_delta.days/7, course_delta.days%7)

	course_dict['courseStandards']= getCourseStandards(course, False)

	return course_dict

def getCourseStandards(course, use_tuple):
	standard_list = []
	for group in course.standard_grouping.all():
		for standard in group.standard.all():
			if use_tuple:
				standard_list.append((standard.id, standard.description))
			else:
				standard_list.append(standard)
	return standard_list

def shallowcopy_course(course, teacher):
	new_course = Course()
	cloned = new_course.clone_from_parent(course, teacher)
	if cloned:
		return new_course
	else:
		return None

def deepcopy_course(course, teacher):
	#first copy over the course
	new_course = shallowcopy_course(course, teacher)

	if not new_course:
		return None
	print "there"
	#this is so the units will have a course to attach to
	new_course.save()
	print "here"
	#now we can do standards goupign:
	for group in course.standard_grouping.all():
		new_course.standard_grouping.add(group)

	#deepcopy units
	units = Unit.objects.filter(course=course)
	for unit in units:
		unit_methods.deepcopy_unit(unit, teacher, new_course)
	return new_course
