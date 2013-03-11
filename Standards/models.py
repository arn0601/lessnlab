from django.db import models

STATE_CHOICES = [('', 'None'),('PA','Pennsylvania'), ('MO', 'Missouri'), ('NY', 'New York')]

class Standard(models.Model):
	name = models.CharField(max_length=32)
	owner_type = models.CharField(max_length=32, choices=STATE_CHOICES)
	description = models.TextField()
	creation_date = models.DateTimeField()
	start_date = models.DateField()
	expiration_date = models.DateField()
	department = models.CharField(max_length=32)
	subject = models.CharField(max_length=32)
	grade = models.CharField(max_length=32)


	
	
