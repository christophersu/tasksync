"""Command-line skeleton application for Tasks API.
Usage:
  $ python sync.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sync.py --help

"""

import argparse
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import file
from oauth2client import tools
from oauth2client import client
from tasksync.TaskSync import TaskSync

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/tasks',
      'https://www.googleapis.com/auth/tasks.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  storage = file.Storage('store.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = discovery.build('tasks', 'v1', http=http)

  try:
    sync = TaskSync(service)
    sync.sync('MTY1ODY1NTcwNjczNzI4MzI0MTg6Mzk5ODEzMTU5OjA')

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)
