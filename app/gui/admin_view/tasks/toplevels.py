import tkinter as tk
from tkinter.messagebox import showerror

from tkcalendar import DateEntry

from app.database.db_queries import DbQueries
from app.gui.admin_view.workers.workers import WorkersTable
from app.gui.utils import center
from app.modules.task import Task


def _validate_name(name):
    if len(name) == 0:
        showerror('Invalid input', 'Please enter a name')
        return False
    return True


def _workers_display(workers_ids):
    workers = DbQueries.get_workers_by_ids(workers_ids)
    names = []
    for worker in workers.values():
        names.append(worker.name + " " + worker.surname)
    return ', '.join(names)


class CreationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add')

        tk.Label(self, text='Name:').grid(column=0, row=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(column=1, row=0)

        tk.Label(self, text='Deadline:').grid(column=0, row=1)
        self.deadline_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.deadline_entry.grid(column=1, row=1)

        tk.Label(self, text='Execution day:').grid(column=0, row=2)
        self.exec_day_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.exec_day_entry.grid(column=1, row=2)

        tk.Label(self, text='Notes:').grid(column=0, row=3)
        self.notes_entry = tk.Entry(self)
        self.notes_entry.grid(column=1, row=3)

        tk.Label(self, text='Workers:').grid(column=0, row=4)
        self.workers_text = tk.Label(self, text='')
        self.workers_text.grid(column=1, row=4)
        tk.Button(self, text='Assign workers', command=self.assign_workers).grid(column=3, row=4)
        self.workers_ids = []

        tk.Button(self, text='Add', command=self.submit).grid(column=1, row=5)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        name = self.name_entry.get()
        deadline = self.deadline_entry.get_date()
        exec_day = self.exec_day_entry.get_date()
        notes = self.notes_entry.get()

        if not _validate_name(name):
            return

        DbQueries.insert_task(Task(name, deadline, exec_day, notes, '', False, []))
        task_id = DbQueries.get_next_task_id()
        for worker_id in self.workers_ids:
            DbQueries.insert_assignment(task_id, worker_id)

        self.grab_release()
        self.destroy()

    def assign_workers(self):
        ChooseWorkers(self)
        self.workers_ids = ChooseWorkers.chosen
        self.workers_text['text'] = _workers_display(self.workers_ids)


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

        tk.Label(self, text='Name:').grid(column=0, row=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, updated_task.name)
        self.name_entry.grid(column=1, row=0)

        tk.Label(self, text='Deadline:').grid(column=0, row=1)
        self.deadline_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.deadline_entry.set_date(updated_task.deadline)
        self.deadline_entry.grid(column=1, row=1)

        tk.Label(self, text='Execution day:').grid(column=0, row=2)
        self.exec_day_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.exec_day_entry.set_date(updated_task.exec_day)
        self.exec_day_entry.grid(column=1, row=2)

        tk.Label(self, text='Notes:').grid(column=0, row=3)
        self.notes_entry = tk.Entry(self)
        self.notes_entry.insert(0, updated_task.notes)
        self.notes_entry.grid(column=1, row=3)

        tk.Label(self, text='Execution notes:').grid(column=0, row=4)
        self.exec_notes_entry = tk.Entry(self)
        self.exec_notes_entry.insert(0, updated_task.exec_notes)
        self.exec_notes_entry.grid(column=1, row=4)

        tk.Label(self, text='Status:').grid(column=0, row=5)
        self.status = tk.BooleanVar()
        status_checkbox = tk.Checkbutton(self, variable=self.status)
        self.status.set(updated_task.status)
        status_checkbox.grid(column=1, row=5)

        tk.Label(self, text='Workers:').grid(column=0, row=6)
        self.workers_text = tk.Label(self, text='')
        self.workers_text.grid(column=1, row=6)
        tk.Button(self, text='Assign workers', command=self.assign_workers).grid(column=3, row=6)

        tk.Button(self, text='Update', command=self.submit).grid(column=1, row=7)

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

    def assign_workers(self):
        ChooseWorkers(self)
        self.workers_ids = ChooseWorkers.chosen
        self.display_workers(self.workers_ids)

    def submit(self):
        name = self.name_entry.get()
        deadline = self.deadline_entry.get_date()
        exec_day = self.exec_day_entry.get_date()
        notes = self.notes_entry.get()
        exec_notes = self.exec_notes_entry.get()
        status = self.status.get()

        if not _validate_name(name):
            return

        DbQueries.update_task(self.task_id, Task(name, deadline, exec_day, notes, exec_notes, status, []))
        DbQueries.delete_assignments_by_task(self.task_id)
        for worker_id in self.workers_ids:
            DbQueries.insert_assignment(self.task_id, worker_id)

        self.grab_release()
        self.destroy()

    def display_workers(self, workers_ids):
        self.workers_text['text'] = _workers_display(workers_ids)


class ChooseWorkers(tk.Toplevel):
    chosen = []

    def __init__(self, parent):
        super().__init__(parent)
        self.title('Choose workers')

        tk.Label(self, text="Hold 'Ctrl' to select multiple rows").pack()

        self.table = WorkersTable(self)
        self.table.pack()

        tk.Button(self, text='Confirm', command=self.submit).pack()

        self.table.show_workers()

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        selected = self.table.selection()
        if selected == '':
            return

        chosen = []
        for selection in selected:
            chosen.append(self.table.item(selection)['text'])

        ChooseWorkers.chosen = chosen

        self.grab_release()
        self.destroy()
