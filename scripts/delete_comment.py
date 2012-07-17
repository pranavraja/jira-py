import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira

def main(issue_key, comment_id):
	try: jira.Comment.get(issue_key, comment_id).delete()
	except jira.APIException, e:
		print e.response.status, e.response.reason
		print e.response.read()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	comment_id = raw_input('Comment ID: ')
	main(issue_key, comment_id)
