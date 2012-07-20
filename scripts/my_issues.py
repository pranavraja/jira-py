import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import lib.jira as jira
import json
import search_issues

def main(query='not (status = Closed) and assignee = currentUser() order by updated desc'):
	search_issues.print_results(query)

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1]:
		main(sys.argv[1])
	else:
		main()
