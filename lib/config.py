
from ConfigParser import RawConfigParser
import os
import getpass

FILENAME = '~/.jira.cfg'

parser = RawConfigParser()
filepath = os.path.expanduser(FILENAME)
if os.path.exists(filepath): parser.read(filepath)
else:
	# Set up config file
	parser.add_section('login')
	parser.set('login','username',raw_input('username: '))
	passwd_confirmed = False
	passwd = None
	passwd2 = None
	while not passwd_confirmed:
		passwd = getpass.getpass()
		passwd2 = getpass.getpass('Confirm: ')
		if passwd != passwd2: print 'passwords do not match.'
		else: passwd_confirmed = True
	parser.set('login','password', passwd)
	parser.add_section('endpoint')
	parser.set('endpoint','host',raw_input('host (e.g jira.atlassian.com): '))
	parser.set('endpoint','path','/rest/api/latest')
	f = open(filepath, 'w')
	parser.write(f)
	os.chmod(filepath, 0600) #Only user can read this

def get(section, key):
	return parser.get(section, key)

