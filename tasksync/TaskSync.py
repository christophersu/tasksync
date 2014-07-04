import json

class TaskSync():
    def test(self):
        tasklists = self.service.tasklists().list().execute()
        for tasklist in tasklists['items']:
            print json.dumps(tasklist)

    def sync(self, google_tasklist, tasks_to_sync=None, done_tasks=None):
        # eventually: sync(self, json, tasklist)
        # assume you receive data in the following format
        tasks_to_sync = [
            {
                "_id": "41911c31f5629ad3c6ec7aa504000c40",
                "name": "Write report",
                "due": "2012-03-01T12:00:00Z"
            }
        ]

        # get these by either looking at the last 100 events or getting all tasks from done
        done_tasks = [
            "41911c31f5629ad3c6ec7aa504000c40"
        ]

        # get tasks that are already there
        existing = self.service.tasks().list(tasklist=google_tasklist).execute()

        # check for duplicates
        for task in existing['items']:
            for i in range(0, len(tasks_to_sync)):
                cur_id = tasks_to_sync[i]['_id']
                if 'notes' in task.keys():
                    if task['notes'] == cur_id :
                        # print 'found duplicate'
                        if cur_id in done_tasks:
                            task['status'] = 'completed'
                            result = self.service.tasks().update(tasklist=google_tasklist, task=task['id'], body=task).execute()
                            # print result['completed']
                        tasks_to_sync.pop(i)

        # clear completed tasks (cleared tasks will be hidden and not displayed in the calendar)
        # self.service.tasks().clear(tasklist=google_tasklist).execute()
        # alternatively, just set the `hidden` attribute of specific tasks to true:
        # task['hidden'] = True
        # result = self.service.tasks().update(tasklist=google_tasklist, task=task['id'], body=task).execute()

        # add new tasks
        for task in tasks_to_sync:
            result = self.service.tasks().insert(tasklist=google_tasklist, body={
                'title': task['name'],
                'notes': task['_id'],
                'due': task['due']
            }).execute()
            print result['id']

    def __init__(self, service):
        self.service = service