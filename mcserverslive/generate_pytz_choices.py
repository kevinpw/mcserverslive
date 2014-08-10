import os, sys
cwd = os.path.split(sys.argv[0])[0]
sys.path.append(cwd)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mcserverslive.settings'


from pytz import all_timezones

f = open('accounts/pytz_choices.py', 'w')

f.write('PYTZ_CHOICES = (\n')

for tz in all_timezones:
	timezone = '\'' + tz + '\''
	string = '	(' + timezone + ',' + timezone + '),\n'
	f.write(string)

f.write(')\n')

f.close()
