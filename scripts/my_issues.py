import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira
import json

def main(query='not (status = Closed) and assignee = currentUser() order by updated desc'):
	try:
		issues = jira.Issue.search(query)
		for issue in issues:
			print '%-15s %-15s %s' % (issue.key, issue.status, issue.summary)
	except jira.APIException, e:
		print e.response.status, e.response.reason
		print e.response.read()

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1]:
		main(sys.argv[1])
	else:
		main()
