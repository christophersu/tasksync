import json

class TaskSync():
    def test(self):
        tasklists = self.service.tasklists().list().execute()
        for tasklist in tasklists['items']:
            print json.dumps(tasklist)

    def sync(self, tasklist):
        # eventually: sync(self, json, tasklist)
        # assume you receive data in the following format
        tasks_to_sync = [
            {
                "_id": "41911c31f5629ad3c6ec7aa504000c40",
                "name": "Write report",
                "due": "2012-03-01T12:00:00Z"
            }
        ]

        # get tasks that are already there
        existing = self.service.tasks().list(tasklist=tasklist).execute()

        # check for duplicates
        for task in existing['items']:
            for i in range(0, len(tasks_to_sync)):
                if 'notes' in task.keys():
                    if task['notes'] == tasks_to_sync[i]['_id']:
                        print 'found duplicate'
                        # check to see if already imported tasks have changed in state
                        tasks_to_sync.pop(i)

        # add new tasks
        for task in tasks_to_sync:
            result = self.service.tasks().insert(tasklist=tasklist, body={
                'title': task['name'],
                'notes': task['_id'],
                'due': task['due']
            }).execute()
            print result['id']

    def __init__(self, service):
        self.service = service