
import webbrowser
import sys

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	webbrowser.open('https://ninemsn.jira.com/browse/%s' % issueKey)
