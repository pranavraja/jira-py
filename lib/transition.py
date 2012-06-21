import jira
import sys

def print_usage():
	print 'Usage: python %s [issueKey]' % __file__
	sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) <= 1: print_usage()
	issue_key = sys.argv[1]
	new_state = raw_input('New state: ')
	if issue_key and new_state:	jira.Issue.transition_issue(issue_key, new_state)
	else: print 'Skipping...'
