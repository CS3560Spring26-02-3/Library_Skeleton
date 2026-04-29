from entities.main import create_connection

class Student:
    def __init__(self, telephone_number, physical_address, email_address):
        self.telephone_number = telephone_number
        self.physical_address = physical_address
        self.email_address = email_address
        self.books_checked_out = []

    @classmethod
    def create_account(cls, name, email, pin):
        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Students (name, email, pin) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, pin))
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def authenticate(cls, email, pin):
        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "SELECT student_id, name FROM Students WHERE email = %s AND pin = %s"
            cursor.execute(query, (email, pin))
            row = cursor.fetchone()
            if not row:
                return None

            return {
                "student_id": row[0],
                "name": row[1],
            }
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # Allows for adding book to check out list
    def checkout_book(self, student_id: int, copy_id: int) -> None:
        """Processes a checkout by using the Checkout class."""
        from entities.checkout import Checkout

        try:
            Checkout.process_copy(student_id, copy_id)
            print("Book successfully checked out.")
        except Exception as e:
            print(f"Error during checkout: {e}")

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
