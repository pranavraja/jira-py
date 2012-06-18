
# Jira

A lightweight python client for the [Jira REST API](http://docs.atlassian.com/jira/REST/latest/). 

# Prerequisites

You'll need python 2.7 installed.

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

There's also `edit_comment` and `delete_comment` for you to try out. Have a look at the API and you can probably easily extend it to do other things.

# Credentials

Credentials are stored in a plain-text config file in $HOME/.jira.cfg with `600` permissions, so they can only be read by you (similar to the approach that the `svn` command line client takes).
