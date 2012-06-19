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

class APIException(Exception):
	def __init__(self, msg):
		self.message = msg

	def __str__(self):
		return self.message

class Issue(object):
	api = JiraAPI.default_api()
	def __init__(self, node):
		self.key = node['key']
		self.status = node['fields']['status']['name']
		self.summary = node['fields']['summary']
	
	@classmethod
	def create(cls, fields):
		response = cls.api.send('issue', 'POST', { 'fields': fields })
		if response.status != 201: raise APIException('could not create issue: %d %s' % (response.status, response.message))

	@classmethod
	def search(cls, query):
		response = cls.api.get('search', { 'jql': query, 'fields': 'summary,status' })
		if response.status == 200:
			return [cls(issue) for issue in json.load(response)['issues']]
		else:
			raise APIException('could not get issue: %d %s' % (response.status, response.message))

	def comments(self):
		return Comment.get_by_issue(self.key)

	def add_comment(self, body):
		Comment.add(self.key, self.body)

class Comment(object):
	api = JiraAPI.default_api()
	def __init__(self, issue_key, node):
		self.issue_key = issue_key
		self.id = node['id'] 
		self.author = node['author']['name']
		self.body = node['body']
	
	@classmethod
	def get_by_issue(cls, key):
		response = cls.api.get('issue/%s/comment' % key, { 'fields': 'body' })
		if response.status == 200:
			comments = json.load(response)['comments']
			return [cls(key, node) for node in comments]
		else:
			raise APIException('could not get comments for %s: %d %s' % (key, response.status, response.message))

	@classmethod
	def get(cls, issue_key, id):
		response = cls.api.get('issue/%s/comment/%s' % (issue_key,id), { 'fields': 'body' })
		if response.status == 200:
			return cls(issue_key, json.load(response))
		else:
			raise APIException('could not get comment %s/%s: %d %s' % (key, id, response.status, response.message))

	@classmethod
	def add(cls, issue_key, comment):
		response = cls.api.send('issue/%s/comment' % self.key, 'POST', { "body": body })
		if response.status != 201: raise APIException('could not add comment: %d %s' % (response.status, response.message))

	def update(self, body):
		response = self.api.send('issue/%s/comment/%s' % (self.issue_key, self.id), 'PUT', { "body": body })
		if response.status != 200: raise APIException('could not update comment %s/%s: %d %s' % (key, id, response.status, response.message))

	def delete(self):
		response = self.api.send('issue/%s/comment/%s' % (self.issueKey, comment_id), 'DELETE', { })
		if response.status != 200: raise APIException('could not delete comment %s/%s: %d %s' % (key, id, response.status, response.message))

