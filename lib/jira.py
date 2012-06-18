import httplib
import json
import urllib
import config

class JiraAPI(object):
	def __init__(self, host, api_path, username, password):
		self.host = host
		self.api_path = api_path
		self.username = username
		self.password = password

	def get(self, method, params):
		conn = httplib.HTTPSConnection(self.host)
		params.update({ 'os_username': self.username, 'os_password': self.password })
		#print '%s/%s?%s' % (self.api_path, method, urllib.urlencode(params))
		conn.request('GET', '%s/%s?%s' % (self.api_path, method, urllib.urlencode(params))) 
		return conn.getresponse()

	def send(self, method, requestType, message):
		conn = httplib.HTTPSConnection(self.host)
		conn.request(requestType, '%s/%s?os_username=%s&os_password=%s' % (self.api_path, method, self.username, self.password), json.dumps(message), { 'Content-type': 'application/json' }) 
		resp = conn.getresponse()
		return resp

	@classmethod
	def default_api(cls):
		return cls(config.get('endpoint','host'), config.get('endpoint','path'), config.get('login','username'), config.get('login','password'))

class APIOperation(object):
	def __init__(self, api):
		self.api = api

class IssueSearcher(APIOperation):
	def __init__(self, api):
		super(IssueSearcher, self).__init__(api)

	def search(self, query):
		return self.api.get('search', { 'jql': query, 'fields': 'summary,status' })

	def get_comments(self, issue):
		return self.api.get('issue/%s/comment' % issue, { 'fields': 'body' })

	def get_comment(self, issue, comment_id):
		return self.api.get('issue/%s/comment/%s' % (issue, comment_id), {})

class IssueUpdater(APIOperation):
	def __init__(self, api, issueKey):
		super(IssueUpdater, self).__init__(api)
		self.issueKey = issueKey

	def update(self, fields):
		return self.api.send('issue/%s' % self.issueKey, 'PUT', { "update": fields })

	def add_comment(self, comment):
		return self.api.send('issue/%s/comment' % self.issueKey, 'POST', { "body": comment })

	def delete_comment(self, comment_id):
		return self.api.send('issue/%s/comment/%s' % (self.issueKey, comment_id), 'DELETE', { })

	def update_comment(self, comment_id, comment):
		return self.api.send('issue/%s/comment/%s' % (self.issueKey, comment_id), 'PUT', { "body": comment })

	def get_comment(self, comment_id):
		return IssueSearcher(self.api).get_comment(self.issueKey, comment_id)

class IssueCreator(APIOperation):
	def __init__(self, api):
		super(IssueCreator, self).__init__(api)

	def create(self, fields):
		return self.api.send('issue', 'POST', { 'fields': fields })

