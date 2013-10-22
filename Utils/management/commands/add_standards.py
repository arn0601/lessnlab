from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from Standards.models import *
from Types.models import *
from Courses.models import StandardGrouping
import sys,traceback
import datetime
import csv

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		f = open('standards.csv', 'r')
		try:
			reader = csv.reader(f)
			rownum = 0
			header = []
			for row in reader:
				if rownum==0:
					rownum+=1
					header=row
				else:
					rownum+=1
					numbering = row[0]
					grade = row[1]
					stype = row[4]
					state = row[2]
					subject = row[5]
					description = row[8]
					standard = Standard()
					standard.standard_type = StandardType.objects.get(value=stype)
					if (stype == 'State'):
						standard.state = State.objects.get(value=state)
					standard.description = description
					standard.creation_date = datetime.datetime.today()
					standard.expiration_date = datetime.datetime.today()
					standard.start_date = datetime.datetime.today()
					standard.department = Subject.objects.get(value=subject)
					standard.subject = Subject.objects.get(value=subject)
					standard.grade = Grade.objects.get(value=grade)
					standard.numbering = numbering
					standard.save()
					sg, created = StandardGrouping.objects.get_or_create(subject=standard.subject, grade=standard.grade, standard_type=standard.standard_type, state=standard.state, prebuilt=True)
					sg.standard.add(standard)
					print rownum
		except:
			traceback.print_exc(file=sys.stdout)
