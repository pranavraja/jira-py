import jira
import sys
import json

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issue_key]' % __file__
		sys.exit(0)
	issue_key = sys.argv[1]
	comments = jira.Comment.get_by_issue(issue_key)
	for comment in comments:
		print '#%s %s:\n  %s' % (comment.id, comment.author, comment.body.replace('\n','\n  '))

