import tkinter as tk

from app.database.db_queries import DbQueries
from app.gui.utils import center
from app.modules.task import Task


def _workers_display(workers_ids):
    workers = DbQueries.get_workers_by_ids(workers_ids)
    names = []
    for worker in workers.values():
        names.append(worker.name + " " + worker.surname)
    return ', '.join(names)


class DetailsWindow(tk.Toplevel):
    def __init__(self, parent, task_id):
        super().__init__(parent)
        self.title('Details')

        task = DbQueries.get_task(task_id)

        tk.Label(self, text='Name: ' + task.name, anchor='w').pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text='Deadline: ' + task.deadline.strftime('%Y-%m-%d'), anchor='w').pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text='Execution day: ' + task.exec_day.strftime('%Y-%m-%d'), anchor='w').pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text='Notes: ' + task.notes, anchor='w').pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text='Execution notes: ' + task.exec_notes, anchor='w').pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text='Workers: ' + _workers_display(task.workers), anchor='w').pack(side=tk.TOP, fill=tk.X)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)


class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, updated_task, chosen_task_id):
        super().__init__(parent)
        self.title('Update')

        self.task_id = chosen_task_id
        self.updated_task = updated_task

        tk.Label(self, text='Name: ' + updated_task.name).pack(anchor=tk.W)

        tk.Label(self, text='Deadline: ' + updated_task.deadline).pack(anchor=tk.W)

        tk.Label(self, text='Execution day: ' + updated_task.exec_day).pack(anchor=tk.W)

        tk.Label(self, text='Notes: ' + updated_task.notes).pack(anchor=tk.W)

        exec_notes_frame = tk.Frame(self)
        exec_notes_frame.pack(anchor=tk.W)
        tk.Label(exec_notes_frame, text='Execution notes:').pack(side=tk.LEFT)
        self.exec_notes_entry = tk.Entry(exec_notes_frame)
        self.exec_notes_entry.insert(0, updated_task.exec_notes)
        self.exec_notes_entry.pack(side=tk.LEFT)

        status_frame = tk.Frame(self)
        status_frame.pack(anchor=tk.W)
        self.status = tk.BooleanVar()
        self.status.set(updated_task.status)
        tk.Label(status_frame, text='Status: ').pack(side=tk.LEFT)
        tk.Checkbutton(status_frame, variable=self.status).pack(side=tk.LEFT)

        self.workers_text = tk.Label(self, text='Workers: ')
        self.workers_text.pack(anchor=tk.W)

        tk.Button(self, text='Update', command=self.submit).pack(side=tk.BOTTOM)

        assignments = DbQueries.get_assignments()
        self.workers_ids = []
        for task_id, worker_id in assignments:
            if task_id == self.task_id:
                self.workers_ids.append(worker_id)
        self.display_workers(self.workers_ids)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        name = self.updated_task.name
        deadline = self.updated_task.deadline
        exec_day = self.updated_task.exec_day
        notes = self.updated_task.notes
        exec_notes = self.exec_notes_entry.get()
        status = self.status.get()

        DbQueries.update_task(self.task_id, Task(name, deadline, exec_day, notes, exec_notes, status, []))

        self.grab_release()
        self.destroy()

    def display_workers(self, workers_ids):
        self.workers_text['text'] = 'Workers: ' + _workers_display(workers_ids)
