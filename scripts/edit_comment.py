import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira
import lib.editor as editor
import json

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print 'Usage: python %s [issueKey] [commentId]' % __file__
		sys.exit(0)
	issue_key = sys.argv[1]
	comment_id = sys.argv[2]
	try: existing_comment = jira.Comment.get(issue_key, comment_id)
	except jira.APIException, e:
		print e.response.status, e.response.reason
		print e.response.read()
	message = editor.get_input('# New comment to replace #%s (this line will be ignored)\n%s' % (comment_id, existing_comment.body)).strip()
	if existing_comment.body.strip() == message:
		print 'Comment not changed, exiting...'
		sys.exit(0)
	try: existing_comment.update(message)
	except jira.APIException, e:
		print e.response.status, e.response.reason
		print e.response.read()
