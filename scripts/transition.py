import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira

def print_usage():
	print 'Usage: python %s [issueKey]' % __file__
	sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) <= 1: print_usage()
	issue_key = sys.argv[1]
	new_state = raw_input('New state: ')
	if issue_key and new_state:	
		try: jira.Issue.transition_issue(issue_key, new_state)
		except jira.APIException, e:
			if not e.response: print e.message
			else:
				print e.response.status, e.response.reason
				print e.response.read()
	else: print 'Skipping...'
