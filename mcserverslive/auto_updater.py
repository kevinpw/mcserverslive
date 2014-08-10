import os, sys
cwd = os.path.split(sys.argv[0])[0]
sys.path.append(cwd)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mcserverslive.settings'

from mcserverslive.models import Server
from mcstatus.minecraft_query import MinecraftQuery
from datetime import timedelta
from django.db.models import Avg
from django.utils import timezone

from django.conf import settings
minutes_to_archive = timedelta(minutes=settings.ARCHIVE_EVERY_MINUTES)

servers = Server.objects.all()

for server in servers:

	query = MinecraftQuery(server.ip, server.port)
	right_now = timezone.now()
	time_since_last_archive = right_now - server.archivenumplayers_set.latest('query_time').query_time

	if time_since_last_archive > minutes_to_archive:
		numplayers_set = server.numplayers_set.all()
		num_players = numplayers_set.aggregate(Avg('num_players'))['num_players__avg']
		count_tot = len(numplayers_set)
		count_not_null = len([ np for np in numplayers_set if np.num_players != None ])

		if count_not_null:
			percent_up = int(float(count_not_null)/count_tot*100)
		else:
			percent_up = 0

		server.archivenumplayers_set.create(query_time=right_now, num_players=num_players, percent_up=percent_up)

		for num_players in numplayers_set[-1]:
			num_players.delete()

	try:

		full_status = query.get_rules()

		server.motd = full_status['motd']
		server.version = full_status['version']
		server.max_players = full_status['maxplayers']
		server.game_type = full_status['gametype']

		server.save()
		
		target_plugins = set(full_status['plugins'])
		current_plugins = server.plugin_set.all()
		to_add = target_plugins.difference(set([ str(cp.plugin) for cp in current_plugins ]))
		to_remove = [ cp for cp in current_plugins if not str(cp.plugin) in target_plugins ]

		for plugin in to_add:
			server.plugin_set.create(plugin=plugin)

		for plugin in to_remove:
			plugin.delete()

		server.numplayers_set.create(query_time=right_now, num_players=full_status['numplayers'])

	except:

		server.numplayers_set.create(query_time=right_now, num_players=None)
		
		
