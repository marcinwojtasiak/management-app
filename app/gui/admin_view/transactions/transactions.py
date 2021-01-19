import tkinter as tk
import tkinter.ttk as ttk
from calendar import month_name

from app.database.db_queries import DbQueries
from app.gui.admin_view.transactions.toplevels import CreationWindow, UpdateWindow
from app.gui.utils import sort_column
from app.modules.transaction import Transaction


class TransactionsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # label
        self.title = 'Transactions'
        tk.Label(self, text=self.title).pack(fill=tk.X)

        # filtering frame
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X)

        # year filter
        tk.Label(filter_frame, text='Year:').pack(side=tk.LEFT)
        self.year = tk.StringVar(filter_frame)
        year_filter = tk.Entry(filter_frame, textvariable=self.year)
        year_filter.bind("<FocusOut>", self.show_transactions)
        year_filter.pack(side=tk.LEFT)

        # month filter
        tk.Label(filter_frame, text='Month:').pack(side=tk.LEFT)
        self.month = tk.StringVar(filter_frame)
        month_filter = tk.OptionMenu(filter_frame, self.month, *month_name, command=self.show_transactions)
        month_filter.pack(side=tk.LEFT)

        # table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # table
        cols = ('Value', 'Date', 'Item')
        self.table = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.table.heading(col, text=col, command=lambda _col=col: sort_column(self.table, _col, False))
        self.table.tag_configure('+', background='lime green')
        self.table.tag_configure('-', background='firebrick1')
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # summary frame
        summary_frame = tk.Frame(self)
        summary_frame.pack(anchor=tk.NW)

        self.gross_inc = tk.Label(summary_frame)
        self.gross_inc.pack(side=tk.TOP, anchor=tk.W)
        self.outcome = tk.Label(summary_frame)
        self.outcome.pack(side=tk.TOP, anchor=tk.W)
        self.net_inc = tk.Label(summary_frame)
        self.net_inc.pack(side=tk.TOP, anchor=tk.W)

        # buttons frame
        btns_frame = tk.Frame(self)
        btns_frame.pack(fill=tk.BOTH, expand=True)

        # create button
        create_btn = tk.Button(btns_frame, text='Add', command=self.create_transaction)
        create_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # delete button
        delete_btn = tk.Button(btns_frame, text='Delete', command=self.delete_transaction)
        delete_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # update button
        update_btn = tk.Button(btns_frame, text='Update', command=self.update_transaction)
        update_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # print workers in table
        self.show_transactions()

    def show_transactions(self, event=None):
        gross_inc = 0
        out = 0

        transactions = DbQueries.get_transactions()
        self.table.delete(*self.table.get_children())
        for id_, transaction in transactions.items():
            if self.year.get() != '' and str(transaction.date.year) != self.year.get():
                continue
            if self.month.get() != '' and month_name[transaction.date.month] != self.month.get():
                continue
            tag = None
            if transaction.value >= 0:
                tag = '+'
                gross_inc += transaction.value
            elif transaction.value < 0:
                tag = '-'
                out -= transaction.value

            self.table.insert('', 'end',
                              values=(transaction.value, transaction.date, transaction.item),
                              text=id_,
                              tags=(tag,))
        net_inc = gross_inc - out

        self.gross_inc['text'] = 'Total gross income: ' + str(gross_inc)
        self.outcome['text'] = 'Total expenses: ' + str(out)
        self.net_inc['text'] = 'Total net income: ' + str(net_inc)

    def create_transaction(self):
        CreationWindow(self)
        self.show_transactions()

    def delete_transaction(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        self.table.delete(selected)
        DbQueries.delete_transaction(item['text'])

    def update_transaction(self):
        selected = self.table.focus()
        if selected == '':
            return
        item = self.table.item(selected)

        UpdateWindow(self, Transaction(*item['values']), item['text'])
        self.show_transactions()
