from django.db import models

# Create your models here.
class ModelMapDictionary(models.Model):
  model_name          = models.CharField(max_length=32)
  app_name            = models.CharField(max_length=32)
  attribute_name      = models.CharField(max_length=64)
  humanreadable_name  = models.CharField(max_length=64)
