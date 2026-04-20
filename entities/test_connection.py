import mysql.connector
from mysql.connector import Error

def test_db_connection():
    connection = None
    try:
        # Attempt to connect to the local MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='lib_admin',
            password='LibraryPass123!',
            database='LibrarySystem'
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You connected to database: {record[0]}")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        # Close the connection
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    test_db_connection()