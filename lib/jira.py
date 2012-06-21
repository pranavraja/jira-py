# A minimal JIRA REST API client.
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

	def __str__(self):
		return 'Jira API at %s' % self.host

# Sends a GET request to the jira API, and returns the file handle for the response.
#
# 	response = get('issue/JRA-1/comment', 
#		{ 'maxResults': 20 })
# 	print response.status, response.reason
# 	=> 200 OK
	def get(self, path, params):
		conn = httplib.HTTPSConnection(self.host)
		params.update({ 'os_username': self.username, 'os_password': self.password })
		conn.request('GET', '%s/%s?%s' % (self.api_path, path, urllib.urlencode(params))) 
		return conn.getresponse()

# Sends a request with HTTP method `method` and `message` json-encoded in the body. Returns the file handle for the response.
#
# 	response = send('POST', 'issue', { 'fields': {} })
#  	print response.status, response.reason
#  	=> 201 Created
	def send(self, method, path, message):
		conn = httplib.HTTPSConnection(self.host)
		conn.request(method, '%s/%s?os_username=%s&os_password=%s' % (self.api_path, path, self.username, self.password), json.dumps(message), { 'Content-type': 'application/json' }) 
		resp = conn.getresponse()
		return resp

# Instantiates a default API class from the configuration
#
# 	JiraAPI.default_api()
# 	=> <lib.jira.JiraAPI object at 0x10e7d5890>
# 	print JiraAPI.default_api()
# 	=> Jira API at jira.atlassian.com
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

	def __str__(self):
		return self.key

# Transitions an issue to `state`.
# 
# 	Issue.transition('JRA-1', 'Resolved')
# 
	@classmethod
	def transition_issue(cls, key, state):
		response = cls.api.get('issue/%s/transitions' % key, { 'fields': 'name' })
		if response.status != 200:
			raise APIException('could not get transitions for issue: %d %s' % (response.status, response.reason))
		available_transitions = json.load(response)['transitions']
		transition = [t for t in available_transitions if t['to']['name'].lower() ==  state.lower()]
		if not transition:
			available_states = ','.join(t['to']['name'] for t in available_transitions)
			raise APIException("no transitions found to '%s'. Choose from: %s" % (state, available_states))
		response = cls.api.send('POST', 'issue/%s/transitions' % key, { 'transition': { 'id': transition[0]['id'] } })
		if response.status != 204:
			raise APIException('could not transition issue to %s: %d %s' % (state, response.status, response.reason))

# Updates an issue with `fields`.
# `fields` is a `dict` and the values that you need to pass are specific to your jira instance. See the [Atlassian docs](http://docs.atlassian.com/jira/REST/latest/#id161551)
# 
# 	Issue.update('JRA-1', { 'summary': 
# 		{ 'set': 'Bug in business logic' }})
#
	@classmethod
	def update_issue(cls, key, fields):
		response = cls.api.send('PUT', 'issue/%s' % key, { 'update': fields })
		if response.status != 200:
			raise APIException('could not update issue: %d %s' (response.status, response.reason))

# Creates an issue with json representation in `fields`.
#
# 	Issue.create({ 'project' { 'id': 100 }, 
# 	'summary': 'buggy', 'issuetype': { 'id': 1 }, 
# 	'reporter': { 'name': 'pranavraja' }, ...)
#
	@classmethod
	def create(cls, fields):
		response = cls.api.send('POST', 'issue', { 'fields': fields })
		if response.status != 201: 
			raise APIException('could not create issue: %d %s' % (response.status, response.reason))

# Searches for issues given a JQL `query`, selecting `fields` in the response. Returns a list of `Issue` objects.
#
# 	Issue.search('assignee = pranavraja')
# 	=> [<lib.Jira.Issue object at 0x107e25850>,
# 		<lib.jira.Issue object at 0x107e25851>]
# 	print Issue.search('assignee = pranavraja')[0]
# 	=> JRA-1
	@classmethod
	def search(cls, query, fields='summary,status'):
		response = cls.api.get('search', { 'jql': query, 'fields': fields })
		if response.status == 200:
			return [cls(issue) for issue in json.load(response)['issues']]
		else:
			raise APIException('could not get issue: %d %s' % (response.status, response.reason))

# Gets a list of comments for this issue. Returns a list of `Comment` objects.
#
# 	issue.comments()
# 	=> [<lib.jira.Comment object at 0x107e25910>]
# 	print issue.comments()[0]
# 	=> On hold right now.
#
	def comments(self):
		return Comment.get_by_issue(self.key)

# Adds the comment with raw text `body` to the issue. The raw text may be passed through Jira's wiki markup processor when displayed online.
#
# 	issue.add_comment('test comment')
#
	def add_comment(self, body):
		Comment.add(self.key, self.body)

# Updates this issue with `fields`.
# 
# 	issue.update({ 'summary': { 'set': 'New summary' } })
# 
	def update(self, fields):
		Issue.update_issue(self.key, fields)

# Transitions this issue to `state`.
# 
# 	issue.transition('Resolved')
# 
	def transition(self, state):
		Issue.transition_issue(self.key, state)

class Comment(object):
	api = JiraAPI.default_api()
	def __init__(self, issue_key, node):
		self.issue_key = issue_key
		self.id = node['id'] 
		self.author = node['author']['name']
		self.body = node['body']
	
	def __str__(self):
		return self.body

# Gets comments by issue with issue key `key`. Returns a list of comments.
#
# 	Comment.get_by_issue('JRA-1')
# 	=> [<lib.jira.Comment object at 0x107e25910>]
# 	print Comment.get_by_issue('JRA-1')[0]
# 	=> Comment body
#
	@classmethod
	def get_by_issue(cls, key):
		response = cls.api.get('issue/%s/comment' % key, { 'fields': 'body' })
		if response.status == 200:
			comments = json.load(response)['comments']
			return [cls(key, node) for node in comments]
		else:
			raise APIException('could not get comments for %s: %d %s' % (key, response.status, response.reason))

# Gets a comment with id `id` under issue key `key`. Returns an instance of `Comment`.
#
# 	print Comment.get('JRA-1', '10191')
# 	=> Comment body
#
	@classmethod
	def get(cls, issue_key, id):
		response = cls.api.get('issue/%s/comment/%s' % (issue_key,id), { 'fields': 'body' })
		if response.status == 200:
			return cls(issue_key, json.load(response))
		else:
			raise APIException('could not get comment %s/%s: %d %s' % (key, id, response.status, response.reason))

# Adds a comment `comment` for issue with key `issue_key`.
#
# 	Comment.add('JRA-1', 'Comment body')
#
	@classmethod
	def add(cls, issue_key, comment):
		response = cls.api.send('POST', 'issue/%s/comment' % issue_key, { "body": comment })
		if response.status != 201: raise APIException('could not add comment: %d %s' % (response.status, response.reason))

# Updates this comment with a new body `body`. Note that the entire comment is replaced in the update.
#
# 	comment.update('new comment text')
#
	def update(self, body):
		response = self.api.send('PUT', 'issue/%s/comment/%s' % (self.issue_key, self.id), { "body": body })
		if response.status != 200: raise APIException('could not update comment %s/%s: %d %s' % (key, id, response.status, response.reason))

# Delete this comment.
#
# 	comment.delete()
#
	def delete(self):
		response = self.api.send('DELETE', 'issue/%s/comment/%s' % (self.issue_key, self.id), { })
		if response.status != 200: raise APIException('could not delete comment %s/%s: %d %s' % (key, id, response.status, response.reason))

