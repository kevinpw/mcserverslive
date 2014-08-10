from django.db import models
from django.contrib.auth.models import User
from accounts.pytz_choices import PYTZ_CHOICES

class UserProfile(models.Model):

	user = models.OneToOneField(User)
	timezone = models.CharField(max_length = 32, choices=PYTZ_CHOICES)
	voted = models.BooleanField(default=False)

