import jira
import sys
import json

def main(issueKey):
	api = jira.JiraAPI.default_api()
	searcher = jira.IssueSearcher(api)
	resp = searcher.get_comments(issueKey)
	if resp.status == 200: 
		comments = json.load(resp)['comments']
		for comment in comments:
			print '#%s %s:\n  %s' % (comment['id'], comment['author']['name'], comment['body'].replace('\n','\n  '))
	else: 
		print '%s %s' % (resp.status, resp.reason)
		#print resp.read()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	main(issueKey)
