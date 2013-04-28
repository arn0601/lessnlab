from django.db import models

# Create your models here.

RATING_TYPE = [('All','All')]
class Rating(models.Model):
	rating = models.IntegerField()
	rater = models.ForeignKey('accounts.UserProfile')
	rating_type = models.CharField(max_length=16, choices = RATING_TYPE)
