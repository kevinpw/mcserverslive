from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View 
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template import RequestContext

from datetime import timedelta
import random, string

from mcserverslive.models import *
from mcserverslive.forms import *
from accounts.models import UserProfile

#####################################
# Server List View ##################
#####################################

class ServerListView(ListView):
	model = Server
	paginate_by = 20

	def get_context_data(self, **kwargs):
		context = super(ServerListView, self).get_context_data(**kwargs)
		object_list = context['object_list']
		object_tuples = []
		for obj in object_list:
			num_players = obj.numplayers_set.all().latest('query_time')
			right_now = timezone.now()
			if num_players:	
				seconds = (right_now - num_players.query_time).total_seconds()
			else:
				num_players = self.get_object().archivenumplayers_set.all().latest('query_time')
				seconds = (right_now - num_players.query_time).total_seconds()			
			dt = int((seconds % 3600) // 60)
			np = num_players.num_players
			object_tuples.append((obj, dt, np))			
		context['object_tuples'] = object_tuples
		return context

##########################################
# User Server List View ##################
##########################################

class MyServerListView(ListView):
	template_name = 'mcserverslive/my_server_list.html'
	model = Server
	paginate_by = 20

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MyServerListView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return Server.objects.filter(user=self.request.user)

####################################
# Create a Server Listing ##########
####################################

class ServerCreateView(CreateView):
	form_class = ServerCreateForm
	template_name = 'server_add_form.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ServerCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ServerCreateView, self).get_context_data(**kwargs)
		context['rand_motd'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ServerCreateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('my_list')


##################################
# Update a Server Listing ########
##################################

class ServerUpdateView(UpdateView):
	form_class = ServerUpdateForm
	template_name = 'server_update_form.html'
	model = Server

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user == self.get_object().user:
			return super(ServerUpdateView, self).dispatch(*args, **kwargs)
		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Please only update your own posts.</p>')

	def get_success_url(self):
		return reverse('detail', kwargs={'pk': self.kwargs['pk']})

#################################
# Delete a Listing ##############
#################################

class ServerDeleteView(DeleteView):
	model = Server
	template_name = 'server_confirm_delete.html'
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user == self.get_object().user:
			return super(ServerDeleteView, self).dispatch(*args, **kwargs)
		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Please only delete your own posts.</p>')

	def get_success_url(self):
		return reverse('my_list')

#################################
# Server Detail  ################
#################################

class ServerDetailView(FormMixin, DetailView):
	model = Server
	form_class = TimezoneForm

	def get_form_kwargs(self):
		kwargs = super(ServerDetailView, self).get_form_kwargs()
		if self.request.user.is_authenticated():
			timezone = get_object_or_404(User, pk=self.request.user.pk).userprofile.timezone
		else:
			timezone = 'US/Eastern'
		kwargs['timezone'] = timezone
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(ServerDetailView, self).get_context_data(**kwargs)
		form_class = self.get_form_class()
		context['form'] = self.get_form(form_class)
		return context

######################################
# Comment List View ##################
######################################

class ServerCommentListView(ListView):
	model = ServerComment
	paginate_by = 30
	template_name = 'server_list.html'

	def get_queryset(self):
		return ServerComment.objects.filter(server = self.kwargs['pk']).order_by('-comment_time')

	def get_context_data(self, **kwargs):
		context = super(ServerCommentListView, self).get_context_data(**kwargs)
		context['server'] = self.object_list[0].server
		return context

#############################
# Comment Create View #######
#############################

class ServerCommentCreateView(CreateView):
	form_class = ServerCommentForm
	template_name = 'server_comment_form.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ServerCommentCreateView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.server = get_object_or_404(Server,id=self.kwargs['pk'])
		return super(ServerCommentCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(ServerCommentCreateView, self).get_context_data(**kwargs)
		context['server'] = get_object_or_404(Server, id=self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse('detail', kwargs={'pk': self.kwargs['pk']})

