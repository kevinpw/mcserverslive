import json
import pytz
from datetime import datetime
from dajaxice.decorators import dajaxice_register
from django.utils import timezone
from django.shortcuts import get_object_or_404

from mcserverslive.models import Server
from accounts.models import UserProfile
from django.conf import settings

def milli_since_epoch(dt):
	tz_local = pytz.timezone('US/Eastern')
	dt = dt.astimezone(tz_local)
	dt = dt.replace(tzinfo=None)
	epoch = datetime(1970,1,1)
	delta_secs = (dt - epoch).total_seconds()
	return int(delta_secs*1000)

@dajaxice_register
def get_plot_data(request, plot, pk):

	data = Server.objects.get(pk=pk).archivenumplayers_set.all()
	data = { milli_since_epoch(d.query_time): d.num_players for d in data }
	
	return json.dumps({'data': data})

@dajaxice_register
def get_text_data(request, pk):

	server = Server.objects.get(pk=pk)
	data = {}

	data['banner'] = settings.MEDIA_URL + str(server.banner)
	data['version'] = server.version
	data['game_type'] = server.game_type
	data['max_players'] = server.max_players
	data['motd'] = server.motd
	data['website']	= server.website
	data['votes'] = server.votes

	plugins = ''
	if server.plugin_set.all():
		for plugin in server.plugin_set.all():
			plugins = plugins + plugin.plugin + ' '
	else:
		plugins = 'Vanilla server. No plugins.'

	data['plugins'] = plugins

	num_players = server.numplayers_set.latest('query_time')
	if num_players.num_players != None:
		data['numplayers'] = num_players.num_players
	else:
		data['numplayers'] = 'offline'
	last_queried = int((timezone.now() - num_players.query_time).total_seconds() // 60)
	if last_queried == 1:
		s = ''
	else:
		s = 's'
	data['last_queried'] = '{0} minute{1} ago'.format(last_queried,s) 

	return json.dumps({'data': data})

@dajaxice_register
def vote(request, user_pk, pk):
	
	userprofile = get_object_or_404(UserProfile, id=user_pk)
	
	if userprofile.voted:
		data = 'You already voted today. Vote again tomorrow.'
	else:
		userprofile.voted = True
		userprofile.save()
		server = get_object_or_404(Server, id=pk)
		server.votes = server.votes + 1
		server.save()
		data = 'Voted Up!'

	return json.dumps({'data': data})





