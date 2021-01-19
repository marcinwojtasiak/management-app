import tkinter as tk
import tkinter.ttk as ttk
from datetime import date

from tkcalendar import DateEntry

from app.database.db_queries import DbQueries
from app.gui.utils import sort_column
from app.gui.worker_view.toplevels import UpdateWindow, DetailsWindow
from app.modules.task import Task


class WorkersTasks(tk.Frame):
    def __init__(self, parent, logged_worker):
        super().__init__(parent)

        self.logged_worker = logged_worker

        # filtering frame
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X)

        # exec_day filter
        tk.Label(filter_frame, text='Planned for:').pack(side=tk.LEFT)
        self.exec_day_filter = DateEntry(filter_frame, date_pattern='y-mm-dd')
        self.exec_day_filter.delete(0, tk.END)
        self.exec_day_filter.configure(state='readonly')
        self.exec_day_filter.bind("<<DateEntrySelected>>", self.show_tasks)
        self.exec_day_filter.bind("<FocusOut>", self.show_tasks)
        self.exec_day_filter.configure(validate='none')
        self.exec_day_filter.pack(side=tk.LEFT)
        tk.Button(filter_frame, text='Clear', command=self.clear_date_filter).pack(side=tk.LEFT)

        # table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # table
        cols = ('Name', 'Deadline', 'Execution day', 'Notes', 'Execution notes', 'Status', 'Assigned workers')
        self.table = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.table.heading(col, text=col, command=lambda _col=col: sort_column(self.table, _col, False))
        self.table.column('Deadline', width=80)
        self.table.column('Execution day', width=100)
        self.table.column('Status', width=80)
        self.table.tag_configure('red', background='firebrick1')
        self.table.tag_configure('orange', background='orange')
        self.table.tag_configure('yellow', background='yellow')
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # buttons frame
        btns_frame = tk.Frame(self)
        btns_frame.pack(fill=tk.BOTH, expand=True)

        # details button
        details_btn = tk.Button(btns_frame, text='Details', command=self.detail_task)
        details_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # update button
        update_btn = tk.Button(btns_frame, text='Update', command=self.update_task)
        update_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # print workers in table
        self.show_tasks()

    def clear_date_filter(self):
        self.exec_day_filter.configure(state='normal')
        self.exec_day_filter.delete(0, tk.END)
        self.exec_day_filter.configure(state='readonly')
        self.show_tasks()

    def show_tasks(self, event=None):
        tasks = DbQueries.get_tasks()
        self.table.delete(*self.table.get_children())
        for id_, task in tasks.items():
            if self.exec_day_filter.get() != '' and task.exec_day != self.exec_day_filter.get_date():
                continue
            if task.status and task.exec_day < date.today():
                continue  # if task is finished and it's execution day passed then skip it
            worker_id, _ = DbQueries.get_account_assignment_by_login(self.logged_worker)
            if worker_id not in task.workers:
                continue
            color = None
            if (task.deadline - date.today()).days <= 1:
                color = 'red'
            elif (task.deadline - date.today()).days <= 2:
                color = 'orange'
            elif (task.deadline - date.today()).days <= 3:
                color = 'yellow'

            self.table.insert('', 'end',
                              values=(task.name,
                                      task.deadline,
                                      task.exec_day,
                                      task.notes,
                                      task.exec_notes,
                                      'finished' if task.status else 'not finished',
                                      WorkersTasks.get_workers_display(task.workers)),
                              text=id_,
                              tags=(color,))

    @staticmethod
    def get_workers_display(workers_ids):
        workers = DbQueries.get_workers_by_ids(workers_ids)
        names = []
        for worker in workers.values():
            names.append(worker.name + " " + worker.surname)
        return ', '.join(names)

    def update_task(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        UpdateWindow(self, Task(*item['values']), item['text'])
        self.show_tasks()

    def detail_task(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        DetailsWindow(self, item['text'])
