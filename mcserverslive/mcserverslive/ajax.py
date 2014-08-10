import json
import pytz
from datetime import datetime
from dajaxice.decorators import dajaxice_register
from django.utils import timezone
from django.shortcuts import get_object_or_404

from mcserverslive.models import Server
from accounts.models import UserProfile

def milli_since_epoch(dt):
	tz_local = pytz.timezone('US/Eastern')
	dt = dt.astimezone(tz_local)
	dt = dt.replace(tzinfo=None)
	epoch = datetime(1970,1,1)
	delta_secs = (dt - epoch).total_seconds()
	return int(delta_secs*1000)

@dajaxice_register
def get_plot_data(request, pk):

	data = Server.objects.get(pk=pk).archivenumplayers_set.all()
	data = { milli_since_epoch(d.query_time): d.num_players for d in data }
	
	return json.dumps({'data': data})

@dajaxice_register
def get_text_data(request, pk):

	server = Server.objects.get(pk=pk)
	num_players = server.numplayers_set.latest('query_time')
	plugins = server.plugin_set.all()
	# banner ?
	data = {}
	data['version'] = server.version
	data['game_type'] = server.game_type
	data['max_players'] = server.max_players
	data['numplayers'] = num_players.num_players
	last_queried = int((timezone.now() - num_players.query_time).total_seconds() // 60)
	if last_queried == 1:
		s = ''
	else:
		s = 's'
	data['last_queried'] = '{0} minute{1} ago'.format(last_queried,s) 
	data['motd'] = server.motd
	data['website']	= server.website
	data['votes'] = server.votes


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





