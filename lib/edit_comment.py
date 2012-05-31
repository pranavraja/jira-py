import jira
import sys
import editor
import json

def update_comment(issueKey, comment_id, message):
	api = jira.JiraAPI.default_api()
	updater = jira.IssueUpdater(api, issueKey)
	resp = updater.update_comment(comment_id, message)
	if resp.status == 200: print 'Updated comment #%s.' % comment_id
	else: 
		print '%s %s' % (resp.status, resp.reason)
		#print resp.read()

def get_comment(issueKey, comment_id):
	api = jira.JiraAPI.default_api()
	searcher = jira.IssueSearcher(api)
	resp = searcher.get_comment(issueKey, comment_id)
	if resp.status == 200: return json.load(resp)['body']
	else: 
		print '%s %s' % (resp.status, resp.reason)
		#print resp.read()

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print 'Usage: python %s [issueKey] [commentId]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	comment_id = sys.argv[2]
	existing_comment = get_comment(issueKey, comment_id)
	message = editor.get_input('# New comment to replace #%s (this line will be ignored)\n%s' % (comment_id, existing_comment))
	if existing_comment.strip() == message.strip():
		print 'Comment not changed, exiting...'
		sys.exit(0)
	update_comment(issueKey, comment_id, message)
