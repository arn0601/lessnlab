from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from Standards.models import *
from LessonPlanner.models import StandardGrouping
import datetime

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		glist = ['K','1','2','3','4','5','6','7','8','9','10','11','12']
		stlist = ['Common Core', 'IB', 'AP', 'State']
		statelist = ['Missouri']
		subjectlist = ['Mathematics','English','Science','Social Studies']
		for g in glist:
			grade,created = Grade.objects.get_or_create(value=g)
		for s in stlist:
			stype,c = StandardType.objects.get_or_create(value=s)
		for s in statelist:
			state,c = State.objects.get_or_create(value=s)
		for sub in subjectlist:
			subject,c = Subject.objects.get_or_create(value=sub)
			
