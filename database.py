
import sqlite3

DATABASE_NAME = "library.db"


def create_connection():
    """Connect to the library database and enable foreign keys."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    """Create the tables needed for the library system."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            loan_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    connection.commit()
    connection.close()


def add_book(title, author, category):
    """Add a new book to the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books (title, author, category) VALUES (?, ?, ?)",
        (title, author, category)
    )

    connection.commit()
    connection.close()


def get_books():
    """Retrieve all books from the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    connection.close()
    return books


def update_book(book_id, title, author, category):
    """Update the details of an existing book."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ?, author = ?, category = ?
        WHERE book_id = ?
    """, (title, author, category, book_id))

    connection.commit()
    connection.close()



def delete_book(book_id):
    """Delete a book if it has no loan history."""
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM books WHERE book_id = ?",
            (book_id,)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return "Book not found."

        return "Book deleted successfully!"

    except sqlite3.IntegrityError:
        return "Cannot delete a book with loan records."

    finally:
        connection.close()




def add_member(name, email):
    """Register a new library member."""
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO members (name, email) VALUES (?, ?)",
            (name, email)
        )
        connection.commit()
        return "Member registered successfully!"

    except sqlite3.IntegrityError:
        return "This email is already registered."

    finally:
        connection.close()


def get_members():
    """Retrieve all registered library members."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    connection.close()
    return members


def borrow_book(book_id, member_id, loan_date):
    """Record a book borrowing transaction."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT available FROM books WHERE book_id = ?",
        (book_id,)
    )
    book = cursor.fetchone()

    if book is None:
        connection.close()
        return "Book not found."

    if book[0] == 0:
        connection.close()
        return "This book is already borrowed."

    cursor.execute(
        "SELECT member_id FROM members WHERE member_id = ?",
        (member_id,)
    )
    member = cursor.fetchone()

    if member is None:
        connection.close()
        return "Member not found."

    cursor.execute("""
        INSERT INTO loans (book_id, member_id, loan_date)
        VALUES (?, ?, ?)
    """, (book_id, member_id, loan_date))

    cursor.execute(
        "UPDATE books SET available = 0 WHERE book_id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    return "Book borrowed successfully!"


def get_loan_records():
    """Retrieve loan records using an SQL JOIN."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT loans.loan_id, books.title, members.name,
               loans.loan_date, loans.return_date
        FROM loans
        JOIN books ON loans.book_id = books.book_id
        JOIN members ON loans.member_id = members.member_id
    """)

    records = cursor.fetchall()
    connection.close()
    return records


def return_book(loan_id, return_date):
    """Record a returned book and make it available again."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT book_id
        FROM loans
        WHERE loan_id = ? AND return_date IS NULL
    """, (loan_id,))

    loan = cursor.fetchone()

    if loan is None:
        connection.close()
        return "Active loan not found."

    book_id = loan[0]

    cursor.execute("""
        UPDATE loans
        SET return_date = ?
        WHERE loan_id = ?
    """, (return_date, loan_id))

    cursor.execute("""
        UPDATE books
        SET available = 1
        WHERE book_id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    return "Book returned successfully!"


def search_books(search_term):
    """Search for books by title."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ?
    """, ('%' + search_term + '%',))

    books = cursor.fetchall()
    connection.close()

    return books
