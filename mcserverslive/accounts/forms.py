from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField
from django.forms import ValidationError, CharField, Select, ModelForm, RadioSelect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import *
from accounts.pytz_choices import PYTZ_CHOICES

class CustomRegistrationForm(RegistrationFormUniqueEmail):
	captcha = ReCaptchaField(attrs={'theme':'white'})
	timezone = CharField(widget=Select(choices=PYTZ_CHOICES))

	def __init__(self, *args, **kwargs):
		super(CustomRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['timezone'].initial = 'US/Eastern'

	def clean_password1(self):
		data = self.cleaned_data['password1']
		if len(data) < 8:
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')	 
		if not any(d.isalpha() for d in data):
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')	
		if not any(d.isnumeric() for d in data):
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')					
		return data

class EmailSettingsForm(ModelForm):

	class Meta:
		model = EmailSetting
		fields = ['setting']
		widgets = {'setting': RadioSelect(choices=[
			(True, 'Keep updated with emails.'),
			(False, 'No, don\'t email me.')				
			])}

