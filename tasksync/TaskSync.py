class TaskSync():
    def test(self):
        tasklists = self.service.tasklists().list().execute()
        for tasklist in tasklists['items']:
          print tasklist['title']

    def __init__(self, service):
        self.service = service