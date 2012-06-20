
import unittest
import mock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import lib.jira as jira

class MockHTTPResponse(object):
	def __init__(self, status, body):
		self.status = status
		self.body = body
		
	def read(self):
		return self.body

class APITests(unittest.TestCase):
	def test_issue_search(self):
		jira.Issue.api = mock.Mock()
		jira.Issue.api.get.return_value = MockHTTPResponse(200, '{ "issues": []}')
		issue = jira.Issue.search('jql')
		jira.Issue.api.get.assert_called_with('search', { 'jql': 'jql', 'fields': 'summary,status' })
		issue = jira.Issue.search('more jql', 'summary,description')
		jira.Issue.api.get.assert_called_with('search', { 'jql': 'more jql', 'fields': 'summary,description' })

	def test_issue_create(self):
		jira.Issue.api = mock.Mock()
		jira.Issue.api.send.return_value = MockHTTPResponse(201, '')
		issue = jira.Issue.create({ 'project': 'ZEUS' })
		jira.Issue.api.send.assert_called_with('POST', 'issue', { 'fields': { 'project': 'ZEUS' } })
		
	def test_get_comments(self):
		jira.Comment.api = mock.Mock()
		jira.Comment.api.get.return_value = MockHTTPResponse(200, '{ "comments": [] }')
		issue = jira.Comment.get_by_issue('KEY')
		jira.Comment.api.get.assert_called_with('issue/KEY/comment', { 'fields': 'body' })

if __name__ == '__main__':
	unittest.main()
