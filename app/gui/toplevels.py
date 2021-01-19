import tkinter as tk
from tkinter.messagebox import showerror, showinfo

from app.database.db_queries import DbQueries
from app.modules.worker import Worker
from utils import center


def _validate_login(login):
    if len(login) == 0:
        showerror('Invalid login', 'Please enter a login')
        return False
    return True


def _validate_password(password):
    if len(password) < 6:
        showerror('Invalid password', 'Password has to be at least 6 characters long')
        return False
    return True


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


class AddUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add user')

        self.parent = parent

        tk.Label(self, text='Login: ').grid(column=0, row=0)
        self.login_entry = tk.Entry(self)
        self.login_entry.grid(column=1, row=0)

        tk.Label(self, text='Password: ').grid(column=0, row=1)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.grid(column=1, row=1)

        tk.Label(self, text='Account type: ').grid(column=0, row=2)
        self.type = tk.StringVar()
        tk.OptionMenu(self, self.type, 'Administrator', 'Worker', command=self.change_extra_entries)\
            .grid(column=1, row=2)
        self.type.set('Worker')

        self.name_label = tk.Label(self, text='Name: ')
        self.name_label.grid(column=0, row=3)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(column=1, row=3)

        self.surname_label = tk.Label(self, text='Surname: ')
        self.surname_label.grid(column=0, row=4)
        self.surname_entry = tk.Entry(self)
        self.surname_entry.grid(column=1, row=4)

        self.tel_label = tk.Label(self, text='Phone number: ')
        self.tel_label.grid(column=0, row=5)
        self.tel_entry = tk.Entry(self)
        self.tel_entry.grid(column=1, row=5)

        tk.Button(self, text='Add', command=self.submit).grid(column=0, row=6)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        type_ = self.type.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        tel = self.tel_entry.get()

        if not _validate_login(login) or not _validate_password(password):
            return

        if type_ == 'Worker':
            type_ = 'w'
            if not _validate_name(name) or not _validate_surname(surname) or not _validate_tel(tel):
                return
        elif type_ == 'Administrator':
            type_ = 'a'

        if DbQueries.login_exists(login):
            showerror('Invalid login', 'This login is already in use, please choose another')
            return

        DbQueries.add_account(login, password, type_)
        if type_ == 'w':
            DbQueries.insert_worker(Worker(name, surname, tel))
            worker_id = DbQueries.get_next_worker_id()
            DbQueries.add_account_assignment(worker_id, login)

        showinfo('Success', 'New user added')

        self.grab_release()
        self.destroy()

    def change_extra_entries(self, variable):
        if variable == 'Administrator':
            self.name_label.grid_forget()
            self.name_entry.grid_forget()
            self.surname_label.grid_forget()
            self.surname_entry.grid_forget()
            self.tel_label.grid_forget()
            self.tel_entry.grid_forget()
        elif variable == 'Worker':
            self.name_label.grid(column=0, row=3)
            self.name_entry.grid(column=1, row=3)
            self.surname_label.grid(column=0, row=4)
            self.surname_entry.grid(column=1, row=4)
            self.tel_label.grid(column=0, row=5)
            self.tel_entry.grid(column=1, row=5)


class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Change password')

        tk.Label(self, text='Login: ').grid(column=0, row=0)
        self.login_entry = tk.Entry(self)
        self.login_entry.grid(column=1, row=0)

        tk.Label(self, text='Old password: ').grid(column=0, row=1)
        self.old_password_entry = tk.Entry(self, show='*')
        self.old_password_entry.grid(column=1, row=1)

        tk.Label(self, text='New password: ').grid(column=0, row=2)
        self.new_password_entry = tk.Entry(self, show='*')
        self.new_password_entry.grid(column=1, row=2)

        tk.Label(self, text='Type new password again: ').grid(column=0, row=3)
        self.new_password_rep_entry = tk.Entry(self, show='*')
        self.new_password_rep_entry.grid(column=1, row=3)

        tk.Button(self, text='Add', command=self.submit).grid(column=0, row=4)

        self.transient(parent)
        self.grab_set()
        center(self)
        parent.wait_window(self)

    def submit(self):
        login = self.login_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        new_password_rep = self.new_password_rep_entry.get()

        if not DbQueries.get_type_if_valid(login, old_password)[0]:
            showerror('Invalid credentials', 'There is no user with given login and password')
            return

        if not _validate_login(login) or not _validate_password(new_password):
            return

        if new_password != new_password_rep:
            showerror('Invalid input', 'New password has to be the same in both entries')
            return

        DbQueries.change_password(login, new_password)

        showinfo('Success', 'Password changed')

        self.grab_release()
        self.destroy()
