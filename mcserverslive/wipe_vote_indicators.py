import os, sys
cwd = os.path.split(sys.argv[0])[0]
sys.path.append(cwd)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mcserverslive.settings'

from accounts.models import UserProfile

profiles = UserProfile.objects.all()

for profile in profiles:
	profile.voted = False
	profile.save()
