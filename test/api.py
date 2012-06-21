
import unittest
import mock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.jira import *
import json

class MockHTTPResponse(object):
	def __init__(self, status, body):
		self.status = status
		self.body = body
		
	def read(self):
		return self.body

class APITests(unittest.TestCase):
	def test_issue_search(self):
		Issue.api = mock.Mock()
		Issue.api.get.return_value = MockHTTPResponse(200, '{ "issues": []}')
		issue = Issue.search('jql')
		Issue.api.get.assert_called_with('search', { 'jql': 'jql', 'fields': 'summary,status' })
		issue = Issue.search('more jql', 'summary,description')
		Issue.api.get.assert_called_with('search', { 'jql': 'more jql', 'fields': 'summary,description' })

	def test_issue_create(self):
		Issue.api = mock.Mock()
		Issue.api.send.return_value = MockHTTPResponse(201, '')
		issue = Issue.create({ 'project': 'ZEUS' })
		Issue.api.send.assert_called_with('POST', 'issue', { 'fields': { 'project': 'ZEUS' } })
		
	def test_issue_update(self):
		Issue.api = mock.Mock()
		Issue.api.send.return_value = MockHTTPResponse(200, '')
		issue = Issue.update_issue('ZEUS-1', { 'project': { 'set': 'ZEUS' } })
		Issue.api.send.assert_called_with('PUT', 'issue/ZEUS-1', { 'update': { 'project': { 'set': 'ZEUS' } } })

	def test_issue_transition(self):
		Issue.api = mock.Mock()
		Issue.api.get.return_value = MockHTTPResponse(200, json.dumps({ 
			'transitions': 
			[ 
				{ 
					'id':1, 
					'to': 
					{ 
						'id': 5, 
						'name':'In Progress' 
					} 
				}
			] 
		})) 
		Issue.api.send.return_value = MockHTTPResponse(204, '')
		issue = Issue.transition_issue('ZEUS-1', 'In Progress')
		Issue.api.get.assert_called_with('issue/ZEUS-1/transitions', { 'fields': 'name' })
		Issue.api.send.assert_called_with('POST', 'issue/ZEUS-1/transitions', { 'transition': { 'id': 1 } })
		
	def test_get_comments(self):
		Comment.api = mock.Mock()
		Comment.api.get.return_value = MockHTTPResponse(200, '{ "comments": [] }')
		issue = Comment.get_by_issue('KEY')
		Comment.api.get.assert_called_with('issue/KEY/comment', { 'fields': 'body' })

	def test_add_comment(self):
		Comment.api = mock.Mock()
		Comment.api.send.return_value = MockHTTPResponse(201, '')
		Comment.add('KEY', 'comment')
		Comment.api.send.assert_called_with('POST', 'issue/KEY/comment', { "body": 'comment' })

	def test_update_comment(self):
		Comment.api = mock.Mock()
		Comment.api.get.return_value = MockHTTPResponse(200, '{ "id": 23, "author": { "name": "pranavraja" }, "body": "hello"  }')
		Comment.api.send.return_value = MockHTTPResponse(200, '')
		comment = Comment.get('JRA-1', '23')
		self.assertEqual(comment.body, 'hello')
		comment.update('hola')
		Comment.api.get.assert_called_with('issue/JRA-1/comment/23', { 'fields': 'body' })
		Comment.api.send.assert_called_with('PUT', 'issue/JRA-1/comment/23', { 'body': 'hola' }) 

	def test_delete_comment(self):
		Comment.api = mock.Mock()
		Comment.api.get.return_value = MockHTTPResponse(200, '{ "id": 23, "author": { "name": "pranavraja" }, "body": "hello"  }')
		Comment.api.send.return_value = MockHTTPResponse(200, '')
		comment = Comment.get('JRA-1', '23')
		self.assertEqual(comment.body, 'hello')
		comment.delete()
		Comment.api.get.assert_called_with('issue/JRA-1/comment/23', { 'fields': 'body' })
		Comment.api.send.assert_called_with('DELETE', 'issue/JRA-1/comment/23', {  }) 

if __name__ == '__main__':
	unittest.main()
