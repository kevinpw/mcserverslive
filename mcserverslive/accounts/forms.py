from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField
from django.forms import ValidationError

class CustomRegistrationForm(RegistrationFormUniqueEmail):
	captcha = ReCaptchaField(attrs={'theme':'clean'})

	def clean_password1(self):
		data = self.cleaned_data['password1']
		if len(data) < 8:
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')	 
		if not any(d.isalpha() for d in data):
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')	
		if not any(d.isnumeric() for d in data):
			raise ValidationError(u'Passwords need to be at least 8 characters long and have at least one number and letter')					
		return data
