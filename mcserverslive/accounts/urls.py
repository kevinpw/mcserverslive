from django.conf.urls import patterns, url, include
from django.views.decorators.http import require_POST
from accounts.views import CustomRegistrationView

urlpatterns = patterns('',

	# registration
	url(r'^register/$', CustomRegistrationView.as_view(), name='register'),
)
