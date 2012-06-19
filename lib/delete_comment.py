import jira
import sys

def main(issue_key, comment_id):
	jira.Comment.get(issue_key, comment_id).delete()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: python %s [issueKey]' % __file__
		sys.exit(0)
	issueKey = sys.argv[1]
	comment_id = raw_input('Comment ID: ')
	main(issue_key, comment_id)
