import tkinter as tk
from tkinter.messagebox import showerror

from tkcalendar import DateEntry

from app.database.db_queries import DbQueries
from app.gui.utils import center
from app.modules.transaction import Transaction


def _validate_value(value):
    try:
        float(value)
        return True
    except ValueError:
        showerror('Invalid input', 'Please enter a transaction value which is a number')
        return False


def _validate_item(item):
    if len(item) == 0:
        showerror('Invalid input', 'Please enter a transaction item')
        return False
    return True


class CreationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add')

        tk.Label(self, text='Value').grid(column=0, row=0)
        self.value_entry = tk.Entry(self)
        self.value_entry.grid(column=1, row=0)

        tk.Label(self, text='Date').grid(column=0, row=1)
        self.date_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.date_entry.grid(column=1, row=1)

        tk.Label(self, text='Item').grid(column=0, row=2)
        self.item_entry = tk.Entry(self)
        self.item_entry.grid(column=1, row=2)

        tk.Button(self, text='Add', command=self.submit).grid(column=0, row=3)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        value = self.value_entry.get()
        date = self.date_entry.get()
        item = self.item_entry.get()

        if not _validate_value(value) or not _validate_item(item):
            return

        DbQueries.insert_transaction(Transaction(value, date, item))

        self.grab_release()
        self.destroy()


class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, updated_transaction, transaction_id):
        super().__init__(parent)
        self.title('Update')

        self.transaction_id = transaction_id

        tk.Label(self, text='Value').grid(column=0, row=0)
        self.value_entry = tk.Entry(self)
        self.value_entry.insert(0, updated_transaction.value)
        self.value_entry.grid(column=1, row=0)

        tk.Label(self, text='Date').grid(column=0, row=1)
        self.date_entry = DateEntry(self, date_pattern='y-mm-dd')
        self.date_entry.set_date(updated_transaction.date)
        self.date_entry.grid(column=1, row=1)

        tk.Label(self, text='Item').grid(column=0, row=2)
        self.item_entry = tk.Entry(self)
        self.item_entry.insert(0, updated_transaction.item)
        self.item_entry.grid(column=1, row=2)

        tk.Button(self, text='Update', command=self.submit).grid(column=0, row=3)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        value = self.value_entry.get()
        date = self.date_entry.get()
        item = self.item_entry.get()

        if not _validate_value(value) or not _validate_item(item):
            return

        DbQueries.update_transaction(self.transaction_id, Transaction(value, date, item))

        self.grab_release()
        self.destroy()
