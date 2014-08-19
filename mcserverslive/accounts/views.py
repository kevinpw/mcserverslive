from django.shortcuts import render
from registration.backends.default.views import RegistrationView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

from accounts.forms import *
from accounts.models import EmailSetting

# Create your views here.

###########################
# Registration ############
###########################

class CustomRegistrationView(RegistrationView):
	template_name = 'registration/registration_form.html'
	form_class = CustomRegistrationForm

class EmailSettingsUpdateView(UpdateView):
	form_class = EmailSettingsForm
	template_name = 'email_settings_form.html'
	model = EmailSetting

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(EmailSettingsUpdateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(EmailSettingsUpdateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('home')
