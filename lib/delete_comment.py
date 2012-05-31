import jira
import sys

def main(issueKey, comment_id):
	api = jira.JiraAPI.default_api()
	updater = jira.IssueUpdater(api, issueKey)
	resp = updater.delete_comment(comment_id)
	if resp.status == 204: print 'Deleted.'
	else: 
		print '%s %s' % (resp.status, resp.reason)
		#print resp.read()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	comment_id = raw_input('Comment ID: ')
	main(issueKey, comment_id)
