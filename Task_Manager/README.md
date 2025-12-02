# 🗂 Task Manager Application

A command-line based Task Management System built with Python. This application allows users to manage tasks, track completion, and handle user administration with role-based access, including admin features. Designed to reinforce file handling, control structures, data validation, and modular programming.

---

## 🚀 Features

- ✅ Secure user login with password verification
- 🔒 Admin-only access to user registration and account editing
- 📝 Task creation, editing, and automatic task number assignment
- 📅 Due date entry with leap year and format validation
- 🧾 Task overview in both block format and tabulated display using `tabulate`
- ❌ Filtering of incomplete tasks only (for personal task view)
- 🔁 Reassignment of tasks when users are deleted
- 🎨 Enhanced terminal display using `colorama`

---

## 📁 Files

- `main.py` – Core application logic
- `user.txt` – Stores username/password data
- `tasks.txt` – Stores task data in a comma-separated format

---

## 📦 Tech Stack

- **Python 3**
- [`tabulate`](https://pypi.org/project/tabulate/) – Pretty-printed tables
- [`colorama`](https://pypi.org/project/colorama/) – Terminal text styling


---

## 🧠 Key Concepts Practised

- File I/O (reading/writing to `.txt` files)
- Input validation and exception handling
- Functions and modular coding
- Data formatting and conditional logic
- User role management (admin vs standard user)
- Data persistence without a database

---

## 🔧 Installation & Usage

1. Clone the repo:

   ```bash
   git clone https://github.com/TEHill1910/task-manager.git
   cd task-manager
