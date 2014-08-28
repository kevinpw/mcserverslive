from django.db import models
from django.contrib.auth.models import User
from mcserverslive.formatChecker import ContentTypeRestrictedFileField

####################
# Server model #####
####################

class Server(models.Model):

	user = models.ForeignKey(User)
	server_name = models.CharField(max_length = 40)
	ip = models.CharField(max_length = 50, blank=False)
	port = models.PositiveSmallIntegerField(default=25565, null=False) #query-port

	banner = ContentTypeRestrictedFileField(upload_to=".", 
		content_types=['image/gif', 'image/jpeg', 'image/png',], max_upload_size=5242880)

	host_port = models.PositiveSmallIntegerField(default=25565, null=True)
	motd = models.CharField(max_length = 100, null=True)
	version = models.CharField(max_length = 5, null=True)
	max_players = models.PositiveSmallIntegerField(null=True)
	game_type = models.CharField(max_length = 10, null=True) # are these choices? origin?
	website = models.URLField(blank=True)
	description = models.CharField(max_length=2000)
	votes = models.PositiveSmallIntegerField(default=0)

	class Meta:
		unique_together = (('ip','port'),) #query-port

	def __unicode__(self):
		return unicode(self.server_name)

##################
# Plugin #########
##################

class Plugin(models.Model):

	server = models.ForeignKey(Server)
	plugin = models.CharField(max_length = 50)

	def __unicode__(self):
		return unicode(self.plugin)

#######################
# Number of Players ###
#######################

class NumPlayers(models.Model):

	server = models.ForeignKey(Server)
	query_time = models.DateTimeField()
	num_players = models.PositiveSmallIntegerField(null=True)

	def __unicode__(self):
		return unicode(self.query_time)

##############################
# Long-term Archive Temporal #
##############################

class ArchiveNumPlayers(models.Model):
	
	server = models.ForeignKey(Server)
	query_time = models.DateTimeField()
	num_players = models.PositiveSmallIntegerField(null=True)

	def __unicode__(self):
		return unicode(self.query_time)

#########################
# Server Comment ########
#########################

class ServerComment(models.Model):

	server = models.ForeignKey(Server)
	comment_time = models.DateTimeField()
	user = models.ForeignKey(User)
	comment = models.CharField(max_length=300)	

	def __unicode__(self):
		return unicode(self.comment_time)	
