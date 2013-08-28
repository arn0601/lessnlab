from django.db import models

# Create your models here.
class State(models.Model):
	dummy = models.CharField(max_length=1, null=True, blank=True)
	value = models.CharField(max_length=8)

	def __unicode__(self):
		return u'%s' % (self.value)
class StandardType(models.Model):
	value = models.CharField(max_length=32)

	def __unicode__(self):
		return u'%s' % (self.value)
class Subject(models.Model):
	value = models.CharField(max_length=16)

	def __unicode__(self):
		return u'%s' % (self.value)
class Grade(models.Model):
	value = models.CharField(max_length=8)
	
	def __unicode__(self):
		return u'%s' % (self.value)
