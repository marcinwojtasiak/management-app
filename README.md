# Management Support App
## Introduction
This is a simple desktop application, which helps to manage a small company. It has been made as a university project for learning Python and Tkinter.
The app stores data about workers and allows to assign them tasks. It also stores data about company's transactions.

The system consists of a desktop app with a GUI written in Python and a MySQL database.
## Presentation
### User accounts
Every user has either an admin or a worker account, which they use to login to the system.

<img src="./images/login.png">

Each user can change their password.

<img src="./images/pass_change.png">

### Admin view
Administrator has access to following functionalities:

Adding new users to the system.

<img src="./images/add_user.png">

Performing CRUD operations on workers data.

<img src="./images/admin_workers.png">

Performing CRUD operations on tasks data and assign workers to them.

<img src="./images/admin_tasks.png">

Performing CRUD operations on transactions data.

<img src="./images/admin_trans.png">
### Worker view
A worker can see tasks that have been assigned to them and update theirs status and add notes to them.

<img src="./images/worker_view.png">
<img src="./images/task_update.png">