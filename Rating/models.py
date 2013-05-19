from django.db import models

# Create your models here.

RATING_TYPE = [('All','All')]
class Rating(models.Model):
	rating = models.IntegerField(default=0)
	rater = models.ForeignKey('accounts.UserProfile')
	rating_type = models.CharField(max_length=16, choices = RATING_TYPE)

class Rateable(models.Model):
	cumulative_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	number_raters = models.IntegerField(default=0)

