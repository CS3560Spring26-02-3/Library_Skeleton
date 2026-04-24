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
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO Books (title, author, isbn, genre, category) VALUES (%s, %s, %s, %s, %s)"
        values = (title, author, isbn, genre, category)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            print("Book added successfully!")
        except Error as e:
            print(f"Failed to add book: {e}")
        finally:
            cursor.close()
            conn.close()

# Method to add a physical copy of a book
def add_book_copy(isbn, location, status="Available"):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # copy_id is AUTO_INCREMENT, so we only need to provide isbn, status, and location
        query = "INSERT INTO BookCopies (isbn, status, location) VALUES (%s, %s, %s)"
        values = (isbn, status, location)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            
            # cursor.lastrowid fetches the auto-incremented copy_id that MySQL just generated
            new_copy_id = cursor.lastrowid 
            print(f"Copy added successfully! The new copy_id is: {new_copy_id}")
            
            return new_copy_id
            
        except Error as e:
            print(f"Failed to add book copy: {e}")
            return None
        finally:
            cursor.close()
            conn.close()