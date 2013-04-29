from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from Standards.models import Standard
from LessonPlanner.models import StandardGrouping
import datetime

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
	slist = ['Science;6;Identify the biotic factors (populations of organisms) and abiotic factors (e.g., quantity of light and water, range of temperatures, soil composition) that make up an ecosystem','Science;6;Identify populations within a community that are in competition with one another for resources','Science;6;Predict the possible effects of changes in the number and types of organisms in an ecosystem on the populations of other organisms within that ecosystem','Science;6;Describe possible solutions to potentially harmful environmental changes within an ecosystem','Science;6;Predict how certain adaptations, such as behavior, body structure, or coloration, may offer a survival advantage to an organism in a particular environment','Science;6;Explain the types of fossils and the processes by which they are formed (i.e., replacement, mold and cast, preservation, trace)','Science;6;Use fossil evidence to make inferences about changes on Earth and in its environment  (i.e., superposition of rock layers, similarities between fossils in different geographical locations, fossils of seashells indicate the area was once underwater)','Science;6;Relate the comparative amounts of fresh water and salt water on the Earth to the availability of water as a resource for living organisms and human activity','Science;6;Describe the affect of human activities (e.g., landfills, use of fertilizers and herbicides, farming, septic systems) on the quality of water','Science;6;Analyze the ways humans affect the erosion and deposition of soil and rock materials (e.g., clearing of land, planting vegetation, paving land, construction of new buildings, building or removal of dams) and propose possible solutions']
	sg = StandardGrouping()
	sg.name = '6th Grade Science - MO'
	sg.subject = 'Science'
	sg.grade = '6'
	sg.state = 'MO'
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


