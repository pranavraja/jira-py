
# Jira-py

A lightweight python client for the [Jira REST API](http://docs.atlassian.com/jira/REST/latest/). 

# Prerequisites

You'll need python 2.7 installed.

# API

The main API is in `lib/jira.py`. You can read the [annotated source code](http://pranavraja.github.com/jira-py/docs/jira.html). Note that the API will probably change around a lot as I just started this.

# Running the tests

To run the tests, you'll need to install [mock](http://pypi.python.org/pypi/mock). Clone the repo and run:

	python test/api.py

# Try it out

Clone the repo, and run:

	./mine

This will list all the issues currently assigned to you, in order that they were last updated. If you'd rather override this with a custom query, just add it as the argument onto the script:

	./mine "assignee = currentUser() and status = Open"

Choose an issue key and run:

	./comments [issueKey]

This will list all the comments on that issue. To add a comment, use:

	./add_comment [issueKey]

Your `$EDITOR` will be opened to create the comment. If you save and close the temp file, the comment will be added. If not, the addition will be skipped.

To jump to the issue in a web browser, run:

	./jumpto [issueKey]

This will open the issue in your default browser. You might need to log in again.

There's also `edit_comment` and `delete_comment` for you to try out, they should be self-explanatory. Run them without any arguments to get usage details. Have a look at the API and you can probably easily extend it to do other things.

# Credentials

Credentials are stored in a plain-text config file in `~/.jira.cfg` with `600` permissions, so they can only be read by you (similar to the approach that the `svn` command line client takes).

If you need to change the credentials or API details, just remove the `~/.jira.cfg` file and next time you run a query you will be prompted to update it.
