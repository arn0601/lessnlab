from django.db import models
from accounts.models import TeacherProfile, StudentProfile
from Standards.models import *
from Objectives.models import Objective
from Rating.models import Rating, Rateable
from Lessons.models import Lesson
from Types.models import *
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from Utils.data_upload_helpers import getViewableURL
import urllib

SECTIONTYPE = ((1,'Introduction'), (2,'Review'), (3,'New Material'), (4,'Guided Practice'), (5, 'Independent Practice'))

CONTENTTYPE = (('Text','Text'),('OnlineVideo','OnlineVideo'),('OnlineArticle','OnlineArticle'),('OnlinePicture','OnlinePicture'),('TeacherNote','TeacherNote'),('AdministratorNote','AdministratorNote'),('Assessment','Assessment'),('PowerPoint','PowerPoint'),('Activity','Activity'))

LESSONPLANNER_DROPDOWN_ORDER = ['General', 'Media', 'Checks for Understanding', 'Activity', 'Assessment']

# Create your models here.

class Section(Rateable):
	lesson = models.ForeignKey('Lessons.Lesson')
	placement = models.IntegerField(blank=True)
	name = models.IntegerField(max_length=32, choices=SECTIONTYPE)
	description = models.TextField()
	creation_date = models.DateTimeField(blank=True, null=True)	


class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        return result.as_leaf_class()

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class ContentManager(models.Manager):
    def get_query_set(self):
			print self
			return SubclassingQuerySet(self.model)


class Content(Rateable):
	section = models.ForeignKey(Section)
	creation_date = models.DateTimeField()
	placement = models.IntegerField()
	content_typename = models.CharField(choices=CONTENTTYPE, max_length=32)
	content_type = models.ForeignKey(ContentType, editable=False, null=True)
	objectives = models.ManyToManyField('Objectives.Objective', blank=True, null=True)

			
	def save(self, *args, **kwargs):
		if not self.content_type:
				self.content_type = ContentType.objects.get_for_model(self.__class__)
		super(Content, self).save(*args, **kwargs)

	def as_leaf_class(self):
			content_type = self.content_type
			model = content_type.model_class()
			if model == Content:
					return self
			return model.objects.get(id=self.id)

class ContentRating(Rating):
	content = models.ForeignKey('Content')

#All content types will be subclasses of Content
class TextContent(Content):
	text = models.TextField()

class PowerPointContent(Content):
	data = models.FileField(upload_to="files",blank=True, null=True)
	link = models.CharField(max_length=256)
	def getSecureURL(self):
		print self.link
		return urllib.quote(getViewableURL(20,self.link))



class ActivityContent(Content):
	name = models.CharField(max_length=30)
	description = models.TextField()
	activity_type = models.CharField(max_length=30)
	instructions = models.TextField()
	length = models.FloatField()
	materials = models.TextField()

class CFUContent(Content):
	text = models.CharField(max_length=256)
	expected_response = models.CharField(max_length=256) 

class OnlineVideoContent(Content):
	link = models.CharField(max_length=256)

class OnlineArticleContent(Content):
	link = models.CharField(max_length=256)

class TeacherNoteContent(Content):
	note = models.CharField(max_length=256)

class AdministratorNoteContent(Content):
	note = models.CharField(max_length=256)

class OnlinePictureContent(Content):
	link = models.CharField(max_length=256)

class AssessmentContent(Content):
  title = models.CharField(max_length=256)

class Question(models.Model):
	question = models.CharField(max_length=256)
	placement = models.IntegerField()
	assessment =  models.ForeignKey(AssessmentContent)
	
class Answer(models.Model):
	owner = models.ForeignKey('accounts.UserProfile', null=True)
	question =  models.ForeignKey(Question)
	
class FreeResponseAnswer(Answer):
	answer = models.CharField(max_length=256)

class MultipleChoiceAnswer(Answer):
	answer = models.CharField(max_length=256)
	is_checked = models.BooleanField(default=False)

