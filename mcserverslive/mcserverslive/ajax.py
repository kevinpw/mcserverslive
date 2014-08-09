import json
import pytz
from datetime import datetime
from dajaxice.decorators import dajaxice_register

from mcserverslive.models import Server

def milli_since_epoch(dt):
	tz_local = pytz.timezone('US/Eastern')
	dt = dt.astimezone(tz_local)
	dt = dt.replace(tzinfo=None)
	epoch = datetime(1970,1,1)
	delta_secs = (dt - epoch).total_seconds()
	return int(delta_secs*1000)

@dajaxice_register
def get_data(request, pk):

	data = Server.objects.get(pk=pk).archivenumplayers_set.all()
	data = { milli_since_epoch(d.query_time): d.num_players for d in data }
	
	return json.dumps({'data': data})

