from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from Standards.models import Standard
from LessonPlanner.models import StandardGrouping
import datetime

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		f = open('standards.csv')
		for line in f:
			print line
