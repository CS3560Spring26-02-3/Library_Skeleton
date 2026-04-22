import datetime
from entities.main import create_connection

class Student:
    def __init__(self, telephone_number, physical_address, email_address):
        self.telephone_number = telephone_number
        self.physical_address = physical_address
        self.email_address = email_address
        self.books_checked_out = []

    # Allows for adding book to check out list
    def checkout_book(self, student_id: int, copy_id: int) -> None:
        """ Processes a checkout by inserting a record into the Checkouts table. """
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Use current date for the checkout date
                current_date = datetime.date.today()
                
                query = "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)"
                values = (student_id, copy_id, current_date)
                
                cursor.execute(query, values)
                
                # Update the BookCopies status to 'Checked Out'
                update_query = "UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s"
                cursor.execute(update_query, (copy_id,))
                
                conn.commit()
                print("Book successfully checked out.")
            except Exception as e:
                print(f"Error during checkout: {e}")
            finally:
                cursor.close()
                conn.close()

    # Allows to send a request for library card
    def request_library_card(self) -> None:
        pass

    # Allows to request deleltion of the account
    def request_deletion(self) -> None:
        pass

    # Will process payment with the input of a float data type
    def pay_fine(self, amount: float) -> None:
        pass

    # def display_info(self):
    #     print(f"Telephone Number: {self.telephone_number}")
    #     print(f"Physical Address: {self.physical_address}")
    #     print(f"Email Address: {self.email_address}")
    #     print(f"Books Checked Out: {self.books_checked_out}")