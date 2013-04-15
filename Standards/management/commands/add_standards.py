from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from Standards.models import Standard
from LessonPlanner.models import StandardGrouping
import datetime

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
	slist = ['Mathematics;8;Generalize patterns represented graphically or numerically with words or symbolic rules, using explicit notation;', 'Mathematics;8;Compare and contrast various forms of representations of patterns;', 'Mathematics;8;Identify functions as linear or nonlinear from tables, graphs or equations;', 'Mathematics;8;Use symbolic algebra to represent and solve problems that involve linear relationships;', 'Mathematics;8;Use properties to generate equivalent forms for simple algebraic expressions that include all rationals;', 'Mathematics;8;Model and solve problems, using multiple representations such as graphs, tables, and linear equations;', 'Mathematics;8;Analyze the nature of changes (including slope an intercepts) in quantities in linear relationships;']
	sg = StandardGrouping()
	sg.name = '8th Grade Math - MO'
	sg.subject = 'Mathematics'
	sg.grade = '8'
	sg.creation_date = datetime.datetime.today()
	sg.save()
	i=1
	for line in slist:
		divided = line.split(';')
		dept = divided[0]
		grade = divided[1]
		desc = divided[2]
		s = Standard()
		s.name = 'S' + str(s.id)
		s.owner_type = 'MO'
		s.description = desc
		s.creation_date= datetime.datetime.today()
		s.start_date = datetime.datetime.today()
		s.expiration_date = datetime.datetime.max
		s.department = dept
		s.subject = ''
		s.grade = grade
		s.numbering = str(i)
		s.save()
		sg.standard.add(s)
		i = i+1


