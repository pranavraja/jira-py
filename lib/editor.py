import tempfile
import subprocess
import os

def get_input(message):
	message_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
	message_file.write('%s\n' % message)
	fname = message_file.name
	message_file.close()
	editor = os.environ.get('EDITOR') or 'nano'
	subprocess.call([editor, fname])
	with open(fname) as f: 
		return ''.join(f.readlines()[1:]).strip()

if __name__ == '__main__':
	print get_input()
