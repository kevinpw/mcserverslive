from django.conf.urls import patterns, url
from accounts.views import *

urlpatterns = patterns('',

	url(r'^register/$', CustomRegistrationView.as_view(), name='register'),
	url(r'^email_settings/$', EmailSettingsUpdateView.as_view(), name='email_settings'),

)
