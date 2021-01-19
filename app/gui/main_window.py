import tkinter as tk
from functools import partial
from tkinter import ttk
from tkinter.messagebox import showinfo

from app.database.db_queries import DbQueries
from app.gui.admin_view.tasks.tasks import TasksPage
from app.gui.admin_view.transactions.transactions import TransactionsPage
from app.gui.admin_view.workers.workers import WorkersPage
from app.gui.utils import center
from toplevels import AddUserWindow, ChangePasswordWindow
from worker_view.tasks import WorkersTasks


class LoginWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # login
        tk.Label(self, text="Login: ").pack()
        login = tk.StringVar()
        tk.Entry(self, textvariable=login).pack()

        # password
        tk.Label(self, text="Password: ").pack()
        password = tk.StringVar()
        tk.Entry(self, textvariable=password, show='*').pack()

        validate = partial(LoginWindow.validate, login, password)
        tk.Button(self, text="Login", command=validate).pack()

    @staticmethod
    def validate(login, password):
        exists, type_ = DbQueries.get_type_if_valid(login.get(), password.get())
        if exists:
            global logged_user
            logged_user = login.get()
            if type_ == 'a':
                _show_admin_view()
            elif type_ == 'w':
                _show_worker_view()
        else:
            showinfo('Wrong credentials', "User with given login and password doesn't exist")


class AbstractView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # account management actions
        self.acc_actions_frame = tk.Frame(self,)
        self.acc_actions_frame.pack(fill=tk.X, anchor=tk.NE)
        tk.Button(self.acc_actions_frame, text='Logout', command=_show_login).pack(side=tk.RIGHT)
        tk.Button(self.acc_actions_frame,
                  text='Change password',
                  command=lambda: ChangePasswordWindow(self)).pack(side=tk.RIGHT)
        global logged_user
        tk.Label(self.acc_actions_frame, text='User: ' + str(logged_user)).pack(side=tk.LEFT)


class AdminView(AbstractView):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Button(self.acc_actions_frame, text='Add user', command=self.add_user).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.workers_page = WorkersPage(self)
        self.add_page(self.workers_page)
        self.add_page(TasksPage(self))
        self.add_page(TransactionsPage(self))

    def add_page(self, page):
        self.notebook.add(page, text=page.title, compound=tk.RIGHT)

    def add_user(self):
        AddUserWindow(self)
        self.workers_page.table.show_workers()


class WorkerView(AbstractView):
    def __init__(self, parent):
        super().__init__(parent)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        global logged_user
        WorkersTasks(main_frame, logged_user).pack(fill=tk.BOTH, expand=True)


def _show_admin_view():
    global main_window
    main_window.pack_forget()
    main_window = AdminView(root)
    main_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def _show_worker_view():
    global main_window
    main_window.pack_forget()
    main_window = WorkerView(root)
    main_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def _show_login():
    global main_window
    main_window.pack_forget()
    main_window = LoginWindow(root)
    main_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_geometry("1000x600")
    root.title('Management')
    style = ttk.Style()
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    logged_user = None
    main_window = LoginWindow(root)
    main_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    center(root)
    root.mainloop()
