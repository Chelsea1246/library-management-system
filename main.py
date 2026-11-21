
import database


def main():
    """Start the Library Management System."""
    database.create_tables()

    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add a book")
        print("2. View all books")
        print("3. Update a book")
        print("4. Delete a book")
        print("5. Register a member")
        print("6. View all members")
        print("7. Borrow a book")
        print("8. View borrowing records")
        print("9. Return a book")
        print("10. Search books")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            category = input("Enter category: ")
            database.add_book(title, author, category)
            print("Book added successfully!")

        elif choice == "2":
            books = database.get_books()
            for book in books:
                print(book)
            if not books:
                print("No books found.")

        elif choice == "3":
            book_id = int(input("Enter book ID to update: "))
            title = input("Enter new title: ")
            author = input("Enter new author: ")
            category = input("Enter new category: ")
            database.update_book(book_id, title, author, category)
            print("Book updated successfully!")

        elif choice == "4":
            book_id = int(input("Enter book ID to delete: "))
            result = database.delete_book(book_id)
            print("Book deleted successfully!")

        elif choice == "5":
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            result = database.add_member(name, email)
            print(result)

        elif choice == "6":
            members = database.get_members()
            for member in members:
                print(member)
            if not members:
                print("No members found.")

        elif choice == "7":
            book_id = int(input("Enter book ID: "))
            member_id = int(input("Enter member ID: "))
            loan_date = input("Enter loan date (YYYY-MM-DD): ")

            result = database.borrow_book(
                book_id, member_id, loan_date
            )
            print(result)

        elif choice == "8":
            records = database.get_loan_records()

            if records:
                for record in records:
                    print(record)
            else:
                print("No borrowing records found.")

        elif choice == "9":
            loan_id = int(input("Enter loan ID: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")

            result = database.return_book(loan_id, return_date)
            print(result)

        elif choice == "10":
            search_term = input("Enter book title to search: ")
            books = database.search_books(search_term)

            if books:
                for book in books:
                    print(book)
            else:
                print("No matching books found.")

        elif choice == "11":
            print("Thank you for using the Library Management System!")
            break


if __name__ == "__main__":
    main()


