from django.shortcuts import render
from registration.backends.default.views import RegistrationView
from accounts.forms import CustomRegistrationForm

# Create your views here.

###########################
# Registration ############
###########################

class CustomRegistrationView(RegistrationView):
	template_name = 'registration/registration_form.html'
	form_class = CustomRegistrationForm
