import jira
import sys
import json

def main(query):
	issues = jira.Issue.search("summary ~'%s' or comment ~'%s'" % (query,query))
	for issue in issues:
		print '%-15s %-15s %s' % (issue.key, issue.status, issue.summary)

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1]:
		main(sys.argv[1])
	else:
		print 'Usage: python %s [search]' % __file__
		sys.exit(0)
