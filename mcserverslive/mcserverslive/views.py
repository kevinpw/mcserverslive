from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone

from datetime import timedelta
import random
import string

from mcserverslive.models import Server, ServerComment
from mcserverslive.forms import ServerUpdateForm, ServerCreateForm, ServerCommentForm

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

class MyServerListView(ServerListView):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MyServerListView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return Server.objects.filter(user=self.request.user)

##############################
# Server Detail ##############
##############################

class ServerDetailView(DetailView):
	model = Server

######################################
# Comment List View ##################
######################################

class ServerCommentView(ListView):
	model = ServerComment
	paginate_by = 30
	template_name = 'server_list.html'

	def get_queryset(self):
		return ServerComment.objects.filter(server = self.kwargs['pk']).order_by('-comment_time')

######################################
# Create a Comment ###################
######################################

class ServerCommentSubmitView(CreateView):
	form_class = ServerCommentForm
	success_url = '/'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ServerCommentSubmitView, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.server = get_object_or_404(Server,id=self.kwargs['pk'])
		return super(ServerCommentSubmitView, self).form_valid(form)

####################################
# Create a Server Listing ##########
####################################

class ServerCreateView(CreateView):
	form_class = ServerCreateForm
	template_name = 'server_form.html'
	success_url = '/'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ServerCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ServerCreateView, self).get_context_data(**kwargs)
		context['rand_motd'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ServerCreateView, self).form_valid(form)

##################################
# Update a Server Listing ########
##################################

class ServerUpdateView(UpdateView):
	form_class = ServerUpdateForm
	template_name = 'server_form.html'
	success_url = '/'

	model = Server

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user == self.get_object().user:
			return super(ServerUpdateView, self).dispatch(*args, **kwargs)
		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Please only update your own posts.</p>')

#################################
# Delete a Listing ##############
#################################

class ServerDeleteView(DeleteView):
	model = Server
	template_name = 'server_confirm_delete.html'
	success_url = '/'
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if self.request.user == self.get_object().user:
			return super(ServerDeleteView, self).dispatch(*args, **kwargs)
		else:
			return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Please only delete your own posts.</p>')
