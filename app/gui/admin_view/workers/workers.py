import tkinter as tk
from tkinter import ttk

from app.database.db_queries import DbQueries
from app.gui.admin_view.workers.toplevels import UpdateWindow
from app.gui.utils import sort_column
from app.modules.worker import Worker


class WorkersPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # label
        self.title = 'Workers'
        tk.Label(self, text=self.title).pack(fill=tk.X)

        # table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # table
        self.table = WorkersTable(table_frame)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # buttons frame
        btns_frame = tk.Frame(self)
        btns_frame.pack(fill=tk.BOTH, expand=True)

        # delete button
        delete_btn = tk.Button(btns_frame, text='Delete', command=self.delete_worker)
        delete_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # update button
        update_btn = tk.Button(btns_frame, text='Update', command=self.update_worker)
        update_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # print workers in table
        self.table.show_workers()

    def delete_worker(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        self.table.delete(selected)
        _, login = DbQueries.get_account_assignment_by_id(item['text'])
        DbQueries.delete_account_assignment(item['text'])
        DbQueries.delete_account(login)
        DbQueries.delete_assignments_by_worker(item['text'])
        DbQueries.delete_worker(item['text'])

    def update_worker(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        UpdateWindow(self, Worker(*item['values']), item['text'])
        self.table.show_workers()


class WorkersTable(ttk.Treeview):
    cols = ('Name', 'Surname', 'Tel')

    def __init__(self, parent):
        super().__init__(parent, columns=WorkersTable.cols, show='headings')
        for col in WorkersTable.cols:
            self.heading(col, text=col, command=lambda _col=col: sort_column(self, _col, False))

    def show_workers(self):
        workers = DbQueries.get_workers()
        self.delete(*(self.get_children()))
        for id_, (name, surname, tel) in workers.items():
            self.insert('', 'end', values=(name, surname, tel), text=id_)

