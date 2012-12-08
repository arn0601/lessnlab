from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
	TEACHER = 'T'
	STUDENT = 'S'
	user = models.OneToOneField(User)
	is_teacher = models.BooleanField()
	is_admin = models.BooleanField()
	is_student = models.BooleanField()
	
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
