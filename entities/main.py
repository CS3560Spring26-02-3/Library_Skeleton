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