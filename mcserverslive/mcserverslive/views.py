from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template import RequestContext

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

######################################################
# Server Detail with Comment Creation ################
######################################################

class ServerDetailView(View):

	def get(self, *args, **kwargs):
		view = ServerDetailDisplay.as_view()
		return view(self.request, *args, **kwargs)

	def post(self, *args, **kwargs):
		view = ServerCommentSubmit.as_view()
		return view(self.request, *args, **kwargs)

class ServerDetailDisplay(DetailView):
	model = Server

	def get_context_data(self, **kwargs):
		context = super(ServerDetailDisplay, self).get_context_data(**kwargs)
		context['comment_form'] = ServerCommentForm()
		return context

class ServerCommentSubmit(CreateView):
	form_class = ServerCommentForm
	template_name = 'mcserverslive/server_detail.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.server = get_object_or_404(Server,id=self.kwargs['pk'])
		return super(ServerCommentSubmit, self).form_valid(form)

	def form_invalid(self, form):
		server = get_object_or_404(Server, pk=self.kwargs['pk'])
		return render_to_response(self.template_name, {'comment_form': form, 'server': server },
			RequestContext(self.request)) 

	def get_success_url(self):
		return reverse('detail', kwargs={'pk': self.kwargs['pk']})

######################################
# Comment List View ##################
######################################

class ServerCommentView(ListView):
	model = ServerComment
	paginate_by = 30
	template_name = 'server_list.html'

	def get_queryset(self):
		return ServerComment.objects.filter(server = self.kwargs['pk']).order_by('-comment_time')

####################################
# Create a Server Listing ##########
####################################

class ServerCreateView(CreateView):
	form_class = ServerCreateForm
	template_name = 'server_form.html'

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

	def get_success_url(self):
		return reverse('my_list')

##################################
# Update a Server Listing ########
##################################

class ServerUpdateView(UpdateView):
	form_class = ServerUpdateForm
	template_name = 'server_form.html'
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
