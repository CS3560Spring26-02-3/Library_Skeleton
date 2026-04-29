import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Establish connection to the MySQL database """
    try:
        # Connect to the local MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='lib_admin',
            password='LibraryPass123!',
            database='LibrarySystem'
        )
        if connection.is_connected():
            print("/connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Method to add a book
def add_new_book(title, author, isbn, genre, category):
    from entities.book import Book

    try:
        Book.add_new(title, author, isbn, genre, category)
        print("Book added successfully!")
    except Exception as e:
        print(f"Failed to add book: {e}")

# Method to add a physical copy of a book
def add_book_copy(isbn, location, status="Available"):
    from entities.book_copies import BookCopies

    try:
        new_copy_id = BookCopies.add_copy(isbn, location, status)
        print(f"Copy added successfully! The new copy_id is: {new_copy_id}")
        return new_copy_id
    except Exception as e:
        print(f"Failed to add book copy: {e}")
        return None
