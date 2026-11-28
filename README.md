
# Library Management System

## Overview
The Library Management System is a Python application
that uses an SQLite relational database to manage
books, library members, and borrowing transactions.

## Features
- Add new books
- View all books
- Update book information
- Delete books
- Register library members
- View registered members
- Borrow books
- Return borrowed books
- Search for books by title
- View borrowing records using SQL JOIN

## Technologies Used
- Python
- SQLite
- Visual Studio Code
- Git and GitHub

## Database Design
The application uses three relational tables:

1. Books: Stores book information.
2. Members: Stores member information.
3. Loans: Stores borrowing and return records.

The Loans table uses foreign keys to connect books
and members.

## SQL Concepts Demonstrated
- CREATE TABLE
- INSERT
- SELECT
- UPDATE
- DELETE
- JOIN
- Primary keys
- Foreign keys

## How to Run
1. Install Python.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Run the following command:

   python main.py

The SQLite database is created automatically.

## Author
Chelsea Afriyie Opoku


## Development Environment
- Operating System: Windows
- Code Editor: Visual Studio Code
- Programming Language: Python
- Database: SQLite

## Useful Websites
- Python: https://www.python.org/
- SQLite: https://www.sqlite.org/
- W3Schools SQL Tutorial: https://www.w3schools.com/sql/

## Future Improvements
- Add a graphical user interface.
- Add due dates and overdue-book tracking.
- Add member login functionality.

## Software Demo
Demo video: https://youtu.be/PRsrstvOB5Y
