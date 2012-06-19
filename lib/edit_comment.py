import jira
import sys
import editor
import json

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print 'Usage: python %s [issueKey] [commentId]' % __file__
		sys.exit(0)
	issue_key = sys.argv[1]
	comment_id = sys.argv[2]
	existing_comment = jira.Comment.get(issue_key, comment_id)
	message = editor.get_input('# New comment to replace #%s (this line will be ignored)\n%s' % (comment_id, existing_comment.body)).strip()
	if existing_comment.body.strip() == message:
		print 'Comment not changed, exiting...'
		sys.exit(0)
	existing_comment.update(message)
