import jira
import sys
import json

def main(query='not (status = Closed) and assignee = currentUser() order by updated desc'):
	api = jira.JiraAPI.default_api()
	searcher = jira.IssueSearcher(api)
	resp = searcher.search(query)
	if resp.status != 200:
		print '%s %s' % (resp.status, resp.reason)
	else:
		issues = json.load(resp)['issues']
		for issue in issues:
			print '%s %s' % (issue['key'], issue['fields']['summary'])

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1]:
		main(sys.argv[1])
	else:
		main()
