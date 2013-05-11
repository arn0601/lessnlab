from django.db import models

class Standard(models.Model):
	state = models.ForeignKey('State', null=True, blank=True)
	description = models.TextField()
	creation_date = models.DateTimeField()
	start_date = models.DateField()
	expiration_date = models.DateField()
	department = models.CharField(max_length=32)
	subject = models.ForeignKey('Subject')
	grade = models.ForeignKey('Grade')
	numbering = models.CharField(max_length=32)
	standard_type = models.ForeignKey('StandardType')

class State(models.Model):
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
