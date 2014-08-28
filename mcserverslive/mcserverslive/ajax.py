import json, pytz
from datetime import datetime
from dajaxice.decorators import dajaxice_register
from django.utils import timezone

from mcserverslive.models import Server
from django.contrib.auth.models import User
from django.conf import settings

#######################
# Get plot data #######
#######################

def milli_since_epoch(dt, timezone):
	tz_local = pytz.timezone(timezone)
	dt = dt.astimezone(tz_local)
	dt = dt.replace(tzinfo=None)
	epoch = datetime(1970,1,1)
	delta_secs = (dt - epoch).total_seconds()
	return int(delta_secs*1000)

@dajaxice_register
def get_plot_data(request, pk, timezone, ymax):

	if ymax == "0.5":
		ymax = Server.objects.get(pk=pk).max_players

	data = Server.objects.get(pk=pk).archivenumplayers_set.all().order_by('query_time')
	data = { milli_since_epoch(d.query_time, timezone): d.num_players for d in data }
	
	return json.dumps({'data': data, 'ymax': ymax})

############################
# Get current info #########
############################

def get_server_data(server, variables):

	data = {}
	data['server_name'] = server.server_name
	data['banner'] = settings.MEDIA_URL + str(server.banner)
	data['version'] = server.version
	data['game_type'] = server.game_type
	data['max_players'] = server.max_players
	data['motd'] = server.motd
	data['votes'] = server.votes

	num_players = server.numplayers_set.latest('query_time')
	if num_players.num_players != None:
		data['num_players'] = num_players.num_players
	else:
		data['num_players'] = 'offline'

	last_queried = int((timezone.now() - num_players.query_time).total_seconds() // 60)
	if last_queried == 1:
		s = ''
	else:
		s = 's'

	data['last_queried'] = '{0} minute{1} ago'.format(last_queried,s) 

	if 'website' in variables:
		data['website']	= server.website

	if 'plugins' in variables:
		plugins = ''
		if server.plugin_set.all():
			for plugin in server.plugin_set.all():
				plugins = plugins + plugin.plugin + ' '
		else:
			plugins = 'Vanilla server. No plugins.'
	
		data['plugins'] = plugins

	return data

@dajaxice_register
def get_current_data(request, servers, variables):

	data = {}
	servers = Server.objects.filter(pk__in=servers)
	for server in servers:
		data[server.pk] = get_server_data(server, variables)
	
	return json.dumps({'data': data, 'variables': variables})


############################
# Vote up a server #########
############################

@dajaxice_register
def vote(request, user_pk, pk):

	try:
		userprofile = User.objects.get(pk=user_pk).userprofile
	except:
		userprofile = None
		
	if userprofile.voted:
		data = 'You already voted today!'
	else:
		userprofile.voted = True
		userprofile.save()
		server = Server.objects.get(pk=pk)
		server.votes = server.votes + 1
		server.save()
		data = 'Voted Up!'

	return json.dumps({'data': data})





