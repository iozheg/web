from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime

# Create your models here.

class QuestionManager(models.Manager):
	def new(self):
		return Question.objects.filter(added_at__gte=timezone.now()-datetime.timedelta(days=10)).order_by('-id')
	
	def popular(self):
		return Question.objects.order_by('-rating')

class Question (models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	added_at = models.DateField(auto_now_add=True)
	rating = models.IntegerField(default=0)
	
	author = models.ForeignKey(User, related_name='author', null=True, on_delete=models.SET_NULL)
	likes = models.ManyToManyField(User, related_name='likes')
	
	objects = QuestionManager()
	
	def __unicode__(self):
		return u'%s: %s' % (self.title, self.text)
		
	def __str__(self):
		return u'%s: %s' % (self.text, self.text)

class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateField(auto_now_add=True)
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
	author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	
	def __unicode__(self):
		return u'%s' % (self.text)
		
	def __str__(self):
		return u'%s' % (self.text)


	
	
