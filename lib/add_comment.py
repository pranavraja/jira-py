import jira
import sys
import json
import editor

def main(issueKey, comment):
	api = jira.JiraAPI.default_api()
	updater = jira.IssueUpdater(api, issueKey)
	resp = updater.add_comment(comment)
	if resp.status == 201: print 'Added comment #%s' % json.load(resp)['id']
	else: 
		print '%s %s' % (resp.status, resp.reason)
		#print resp.read()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	comment = editor.get_input('# Your comment for issue %s (this line will be ignored)\n' % issueKey)
	if not comment:
		print 'No comment entered, exiting...'
		sys.exit(0)
	main(issueKey, comment)
