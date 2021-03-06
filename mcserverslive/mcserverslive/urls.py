from django.conf.urls import patterns, include, url
from django.views.decorators.http import require_POST
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from mcserverslive.views import *

urlpatterns = patterns('',

	url(r'^$', ServerListView.as_view(), name='home'),
	url(r'^(?P<pk>\d+)/$', ServerDetailView.as_view(), name='detail'),
	url(r'^server_comments/(?P<pk>\d+)/$', ServerCommentListView.as_view(), name='server_comments'),
	url(r'my_servers/$', MyServerListView.as_view(), name='my_list'),
	url(r'server_create_form/$', ServerCreateView.as_view(), name='create'),
	url(r'server_update_form/(?P<pk>\d+)/$', ServerUpdateView.as_view(), name='update'),
	url(r'^server_delete/(?P<pk>\d+)/$', ServerDeleteView.as_view(), name='delete'),
	url(r'^server_comment_form/(?P<pk>\d+)/$', ServerCommentCreateView.as_view(), name='server_add_comment'),
	url(r'^donate/$', TemplateView.as_view(template_name='donate.html'), name='donate'),

	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

	url(r'^accounts/', include('accounts.urls',namespace='accounts')),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^accounts/', include('django.contrib.auth.urls')),
#	url(r'^summernote/', include('django_summernote.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
	urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)), )
