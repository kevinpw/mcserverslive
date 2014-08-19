from django.db import models
from django.contrib.auth.models import User
from accounts.pytz_choices import PYTZ_CHOICES

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	timezone = models.CharField(max_length = 32, choices=PYTZ_CHOICES)
	voted = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.user)

class EmailSetting(models.Model):

	user = models.OneToOneField(User)
	setting = models.BooleanField(default=True)

	def __unicode__(self):
		return unicode(self.user)

from registration.signals import user_registered

def user_registered_callback(sender, user, request, **kwargs):
	profile = UserProfile(user=user)
	profile.timezone = request.POST['timezone']
	profile.voted = False
	profile.save()

user_registered.connect(user_registered_callback)

