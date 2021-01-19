import tkinter as tk
from tkinter.messagebox import showerror

from app.database.db_queries import DbQueries
from app.gui.utils import center
from app.modules.worker import Worker


def _validate_name(name):
    if len(name) == 0:
        showerror('Invalid input', 'Please enter a name')
        return False
    return True


def _validate_surname(surname):
    if len(surname) == 0:
        showerror('Invalid input', 'Please enter a surname')
        return False
    return True


def _validate_tel(tel):
    if len(tel) == 0 or (len(tel) == 9 and str(tel).isdigit()):
        return True
    showerror('Invalid input', 'Please enter a valid phone number (9 digits)')
    return False


class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, updated_worker, worker_id):
        super().__init__(parent)
        self.title('Update')

        self.worker_id = worker_id

        tk.Label(self, text='Name').grid(column=0, row=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, updated_worker.name)
        self.name_entry.grid(column=1, row=0)

        tk.Label(self, text='Surname').grid(column=0, row=1)
        self.surname_entry = tk.Entry(self)
        self.surname_entry.insert(0, updated_worker.surname)
        self.surname_entry.grid(column=1, row=1)

        tk.Label(self, text='Telephone').grid(column=0, row=2)
        self.tel_entry = tk.Entry(self)
        self.tel_entry.insert(0, updated_worker.tel)
        self.tel_entry.grid(column=1, row=2)

        tk.Button(self, text='Update', command=self.submit).grid(column=0, row=3)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        tel = self.tel_entry.get()

        if not _validate_name(name) or not _validate_surname(surname) or not _validate_tel(tel):
            return

        DbQueries.update_worker(self.worker_id, Worker(name, surname, tel))

        self.grab_release()
        self.destroy()
