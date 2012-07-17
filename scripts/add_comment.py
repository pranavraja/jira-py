import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira
import json
import editor

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issue_key]' % __file__
		sys.exit(0)
	issue_key = sys.argv[1]
	comment = editor.get_input('# Your comment for issue %s (this line will be ignored)\n' % issue_key)
	if not comment:
		print 'No comment entered, exiting...'
		sys.exit(0)
	try:
		jira.Comment.add(issue_key, comment)
	except jira.APIException, e:
		print e.response.status, e.response.reason
		print e.response.read()
