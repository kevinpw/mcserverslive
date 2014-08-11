from django.forms import ModelForm, ValidationError, Textarea, CharField, HiddenInput, Form, ChoiceField
from django.core.files.images import get_image_dimensions
from django.core.files import File
from django.conf import settings
from django.utils import timezone

from mcserverslive.models import Server, ServerComment
from mcstatus.minecraft_query import MinecraftQuery

###########################
# Server Update Form ######
###########################

class ServerUpdateForm(ModelForm):
	full_status = {}

	class Meta:
		model = Server
		fields = ['server_name','banner','description','website']
		widgets = { 'description': Textarea(attrs={ 'style': 'resize: none;',
			'cols': 80, 'rows': 20,'onKeyUp': "textCounter(this,'counter_description',2000);"}), }

	def clean(self):
		cleaned_data = super(ServerUpdateForm, self).clean()

		width, height = get_image_dimensions(cleaned_data['banner'])
		if width is not 300 and height is not 50:
			raise ValidationError(u'Banners need to be 300x50 pixels. Please resize image.')

		return cleaned_data

############################
# Server Create Form #######
############################

class ServerCreateForm(ModelForm):
	rand_motd = CharField(widget=HiddenInput())

	class Meta:
		model = Server
		fields = ['server_name','banner','ip','port','description','website']
		widgets = { 'description': Textarea(attrs={ 'style': 'resize: none;',
			'cols': 80, 'rows': 20,'onKeyUp': "textCounter(this,'counter_description',2000);"}), }

	def clean(self):
		cleaned_data = super(ServerCreateForm, self).clean()

		query = MinecraftQuery(cleaned_data['ip'], cleaned_data['port'])
		try:
			self.full_status = query.get_rules()
		except:
			raise ValidationError(u'Cannot query server. Is server.properties enable-query true?')

		if self.full_status['motd'] != cleaned_data['rand_motd']:
			raise ValidationError(u'Check that your server was reloaded with the random MOTD')

		return cleaned_data

	def clean_banner(self):
		data = self.cleaned_data['banner']
		width, height = get_image_dimensions(data)
		if width is not 300 and height is not 50:
			raise ValidationError(u'Banners need to be 300x50 pixels. Please resize image.')
		return data

	def save(self, commit=True):
		instance = super(ServerCreateForm, self).save(commit=False)
		instance.motd = self.full_status['motd']
		instance.version = self.full_status['version']
		instance.max_players = self.full_status['maxplayers']
		instance.game_type = self.full_status['gametype']

		if commit:
			instance.save()

		right_now = timezone.now()
		num_players=self.full_status['numplayers']
		instance.numplayers_set.create(query_time = right_now, num_players = num_players)
		instance.archivenumplayers_set.create(query_time = right_now, num_players = num_players, percent_up=100)	

		plugins = self.full_status['plugins']
		
		for plugin in plugins:
			instance.plugin_set.create(plugin=plugin)

		return instance

############################
# Server Comment Form ######
############################

class ServerCommentForm(ModelForm):
	
	class Meta:
		model = ServerComment
		fields = ['comment']
		widgets = { 'comment': Textarea(attrs={ 'style': 'resize: none;',
			'cols': 50, 'rows': 4,'onKeyUp': "textCounter(this,'counter_description',300);"}), }

	def clean_comment(self):
		data = self.cleaned_data['comment']
		words = data.split()
		for word in words:
			if len(word) > 60:
				raise ValidationError(u'No words more than 60 characters')
		return data
			
	def save(self, commit=True):
		instance = super(ServerCommentForm, self).save(commit=False)
		instance.comment_time = timezone.now()
		if commit:
			instance.save()
		return instance

