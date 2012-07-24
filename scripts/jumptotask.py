
import webbrowser
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.config as config 

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	host = config.default_config().get('jira_default', 'host')
	webbrowser.open('https://%s/browse/%s' % (host, issueKey))
