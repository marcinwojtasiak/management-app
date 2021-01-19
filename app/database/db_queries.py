import sys
import os
from tkinter.messagebox import showerror

import mysql.connector
from mysql.connector.errors import InterfaceError

from app.modules.task import Task
from app.modules.transaction import Transaction
from app.modules.worker import Worker


# this class manages connection with database and provides methods to execute queries on database
class DbQueries:
    _connection = None
    _cursor = None

    _host = None
    _user = None
    _password = None
    _db = None

    dir_name = os.path.dirname(__file__)
    filename = os.path.join(dir_name, 'db_config.txt')
    with open(filename, 'r') as db_config:
        for line in db_config.readlines():
            split_line = line.split('=')
            if len(split_line) != 2:
                continue
            label = split_line[0].strip()
            value = split_line[1].strip()
            if label == 'host':
                _host = value
            elif label == 'user':
                _user = value
            elif label == 'password':
                _password = value
            elif label == 'db':
                _db = value
        print(_host, _user, _password, _db)
        if _host is None or _user is None or _password is None or _db is None:
            showerror('Database error', "Invalid database connection configuration file")
            sys.exit(0)

    @staticmethod
    def _execute_dml(query, parameters=None):
        DbQueries._connect()
        if parameters is not None:
            DbQueries._cursor.execute(query, parameters)
        else:
            DbQueries._cursor.execute(query)
        DbQueries._connection.commit()
        DbQueries._disconnect()

    @staticmethod
    def _connect():
        try:
            DbQueries._connection = mysql.connector.connect(host=DbQueries._host, user=DbQueries._user,
                                                            password=DbQueries._password, db=DbQueries._db)
            DbQueries._cursor = DbQueries._connection.cursor(buffered=True)
        except InterfaceError:
            showerror('Database error', "Couldn't connect with database")
            sys.exit(0)

    @staticmethod
    def _disconnect():
        DbQueries._connection.close()

    # workers
    @staticmethod
    def get_workers():
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM workers')
        rows = DbQueries._cursor.fetchall()
        workers = {}
        for row in rows:
            workers[row[0]] = Worker(row[1], row[2], row[3])
        DbQueries._disconnect()
        return workers

    @staticmethod
    def get_workers_by_ids(ids):
        DbQueries._connect()
        if (ids is None) or (ids == []):
            return {}
        format_strings = ','.join(['%s'] * len(ids))
        DbQueries._cursor.execute('SELECT * FROM workers WHERE id IN (%s)' % format_strings, tuple(ids))
        rows = DbQueries._cursor.fetchall()
        workers = {}
        for row in rows:
            workers[row[0]] = Worker(row[1], row[2], row[3])
        DbQueries._disconnect()
        return workers

    @staticmethod
    def insert_worker(worker):
        DbQueries._execute_dml('INSERT INTO workers (name, surname, tel) VALUES (%s, %s, %s)', tuple(worker))

    @staticmethod
    def delete_worker(id_):
        DbQueries._execute_dml('DELETE FROM workers WHERE id=%s', (id_,))

    @staticmethod
    def update_worker(id_, worker):
        DbQueries._execute_dml('UPDATE workers SET name=%s, surname=%s, tel=%s WHERE id=%s', (*worker, id_))

    @staticmethod
    def get_next_worker_id():
        DbQueries._connect()
        DbQueries._cursor.execute("SELECT IFNULL(MAX(id), 0) FROM workers")
        DbQueries._disconnect()
        return DbQueries._cursor.fetchall()[0][0]

    # tasks
    @staticmethod
    def get_tasks():
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM tasks')
        rows = DbQueries._cursor.fetchall()
        tasks = {}
        for row in rows:
            DbQueries._cursor.execute('SELECT worker_id FROM task_assign WHERE task_id=%s', (row[0],))
            assigned_workers = list(map(lambda worker: worker[0], DbQueries._cursor.fetchall()))
            tasks[row[0]] = Task(row[1], row[2], row[3], row[4], row[5], row[6], assigned_workers)
        DbQueries._disconnect()
        return tasks

    @staticmethod
    def get_task(id_):
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM tasks WHERE id=%s', (id_,))
        row = DbQueries._cursor.fetchone()
        if not row:
            return None
        DbQueries._cursor.execute('SELECT worker_id FROM task_assign WHERE task_id=%s', (row[0],))
        assigned_workers = list(map(lambda worker: worker[0], DbQueries._cursor.fetchall()))
        DbQueries._disconnect()
        return Task(row[1], row[2], row[3], row[4], row[5], row[6], assigned_workers)

    @staticmethod
    def insert_task(task):
        DbQueries._execute_dml(
            'INSERT INTO tasks (name, deadline, exec_day, notes, exec_notes, status) VALUES (%s, %s, %s, %s, %s, %s)',
            (task.name, task.deadline, task.exec_day, task.notes, task.exec_notes, task.status))

    @staticmethod
    def delete_task(id_):
        DbQueries.delete_assignments_by_task(id_)
        DbQueries._execute_dml('DELETE FROM tasks WHERE id=%s', (id_,))

    @staticmethod
    def update_task(id_, task):
        DbQueries._execute_dml(
            'UPDATE tasks SET name=%s, deadline=%s, exec_day=%s, notes=%s, exec_notes=%s, status=%s WHERE id=%s',
            (task.name, task.deadline, task.exec_day, task.notes, task.exec_notes, task.status, id_))

    @staticmethod
    def get_next_task_id():
        DbQueries._connect()
        DbQueries._cursor.execute("SELECT IFNULL(MAX(id), 0) FROM tasks")
        DbQueries._disconnect()
        return DbQueries._cursor.fetchall()[0][0]

    # tasks assignments
    @staticmethod
    def get_assignments():
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM task_assign')
        rows = DbQueries._cursor.fetchall()
        assignments = []
        for row in rows:
            assignments.append((row[0], row[1]))
        DbQueries._disconnect()
        return assignments

    @staticmethod
    def insert_assignment(task_id, worker_id):
        DbQueries._execute_dml('INSERT INTO task_assign (task_id, worker_id) VALUES (%s, %s)', (task_id, worker_id))

    @staticmethod
    def delete_assignment(task_id, worker_id):
        DbQueries._execute_dml('DELETE FROM task_assign WHERE task_id=%s AND worker_id=%s', (task_id, worker_id))

    @staticmethod
    def delete_assignments_by_task(task_id):
        DbQueries._execute_dml('DELETE FROM task_assign WHERE task_id=%s', (task_id,))

    @staticmethod
    def delete_assignments_by_worker(worker_id):
        DbQueries._execute_dml('DELETE FROM task_assign WHERE worker_id=%s', (worker_id,))

    # transactions
    @staticmethod
    def get_transactions():
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM transactions')
        rows = DbQueries._cursor.fetchall()
        transactions = {}
        for row in rows:
            transactions[row[0]] = Transaction(row[1], row[2], row[3])
        DbQueries._disconnect()
        return transactions

    @staticmethod
    def insert_transaction(transaction):
        DbQueries._execute_dml('INSERT INTO transactions (value, date, item) VALUES (%s, %s, %s)', tuple(transaction))

    @staticmethod
    def delete_transaction(id_):
        DbQueries._execute_dml('DELETE FROM transactions WHERE id=%s', (id_,))

    @staticmethod
    def update_transaction(id_, transaction):
        DbQueries._execute_dml('UPDATE transactions SET value=%s, date=%s, item=%s WHERE id=%s', (*transaction, id_))

    # user accounts
    @staticmethod
    def get_type_if_valid(login, password):
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT EXISTS(SELECT * FROM accounts WHERE login=%s AND password=%s), '
                                  '(SELECT type FROM accounts WHERE login=%s AND password=%s)',
                                  (login, password, login, password))
        exists, type_ = DbQueries._cursor.fetchone()
        DbQueries._disconnect()
        return exists == 1, type_

    @staticmethod
    def login_exists(login):
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT EXISTS(SELECT * FROM accounts WHERE login=%s)', (login,))
        exists = DbQueries._cursor.fetchone()[0]
        DbQueries._disconnect()
        return exists == 1

    @staticmethod
    def add_account(login, password, type_):
        DbQueries._execute_dml('INSERT INTO accounts (login, password, type) VALUES (%s, %s, %s)',
                               (login, password, type_))

    @staticmethod
    def delete_account(login):
        DbQueries._execute_dml('DELETE FROM accounts WHERE login=%s', (login,))

    @staticmethod
    def change_password(login, new_password):
        DbQueries._execute_dml('UPDATE accounts SET password=%s WHERE login=%s', (new_password, login))

    # worker-account assignments
    @staticmethod
    def add_account_assignment(worker_id, login):
        DbQueries._execute_dml('INSERT INTO worker_account (worker_id, account_login) VALUES (%s, %s)',
                               (worker_id, login))

    @staticmethod
    def get_account_assignment_by_id(worker_id):
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM worker_account WHERE worker_id=%s', (worker_id,))
        result = DbQueries._cursor.fetchone()
        DbQueries._disconnect()
        return result

    @staticmethod
    def get_account_assignment_by_login(login):
        DbQueries._connect()
        DbQueries._cursor.execute('SELECT * FROM worker_account WHERE account_login=%s', (login,))
        result = DbQueries._cursor.fetchone()
        DbQueries._disconnect()
        return result

    @staticmethod
    def delete_account_assignment(worker_id):
        DbQueries._execute_dml('DELETE FROM worker_account WHERE worker_id=%s', (worker_id,))
