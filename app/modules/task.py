class Task:
    def __init__(self, name, deadline, exec_day, notes, exec_notes, status, workers):
        self.name = name
        self.deadline = deadline
        self.exec_day = exec_day
        self.notes = notes
        self.exec_notes = exec_notes
        self.status = status
        if status == 'finished':
            self.status = True
        elif status == 'not finished':
            self.status = False
        self.workers = workers

    def __iter__(self):
        for var in [self.name, self.deadline, self.exec_day, self.notes, self.exec_notes, self.status, self.workers]:
            yield var
