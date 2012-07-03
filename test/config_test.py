
import unittest
import tempfile
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

class ConfigurationTest(unittest.TestCase):
	def test_config_create(self):
		f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
		f.write('[jira_default]\nusername=username\npassword=password\nhost=host\npath=path')
		f.flush()
		c = config.Configuration(f.name)
		self.assertEqual(c.get('jira_default', 'username'), 'username')
		self.assertEqual(c.get('jira_default', 'password'), 'password')
		self.assertEqual(c.get('jira_default', 'host'), 'host')
		self.assertEqual(c.get('jira_default', 'path'), 'path')
		os.unlink(f.name)

if __name__ == '__main__':
	unittest.main()
