from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date published')
	
	def __unicode__(self):  #__str__ for python 3
		return self.question_text
	def was_published_recently(self):
		now = timezone.now()
		return now >=self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default = 0)
	
	def __unicode__(self): #__str__ for python 3
		return self.choice_text

class Voter(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)

#class User(AbstractBaseUser, PermissionsMixin):
#	USERNAME_FIELD = 'email'
#	email = models.EmailField(unique=True)
#	is_active = models.BooleanField(default=False)
#	is_staff = models.BooleanField(default=False)
#
#	def get_full_name(self):
		#return self.email
#	def get_short_name(self):
#		return self.email
