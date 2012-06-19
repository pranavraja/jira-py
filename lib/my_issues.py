import jira
import sys
import json

def main(query='not (status = Closed) and assignee = currentUser() order by updated desc'):
	issues = jira.Issue.search(query)
	for issue in issues:
		print '%-15s %-15s %s' % (issue.key, issue.status, issue.summary)

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1]:
		main(sys.argv[1])
	else:
		main()
