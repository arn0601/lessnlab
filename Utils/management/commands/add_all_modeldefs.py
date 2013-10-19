from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from django.db.models import get_models
from Utils.models import ModelMapDictionary
import time

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		for model in get_models():
			model_name 	=  unicode(model.__name__)
			app_name		= unicode(model._meta.app_label)
			for field in model._meta.fields:
				field_name =  unicode(field.name)
				verbose_name = unicode(field.verbose_name)
				if (verbose_name == ""):
					verbose_name = field_name
				print model_name, app_name, field_name, verbose_name
				ModelMapDictionary.objects.get_or_create(model_name = model_name,
																								 app_name = app_name,
																								 attribute_name=field_name,
																								 humanreadable_name=verbose_name)
