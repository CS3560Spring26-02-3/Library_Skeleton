import datetime


class Checkout:
    def __init__(self, return_date, books_checked_out=None):
        self.return_date = return_date
        self.books_checked_out = books_checked_out if books_checked_out is not None else []

    @classmethod
    def process_copy(cls, student_id, copy_id):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)",
                (student_id, copy_id, datetime.date.today()),
            )
            cursor.execute("UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s", (copy_id,))
            conn.commit()
            return copy_id
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def process(cls, student_id, isbn):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            check_existing_query = """
                SELECT c.checkout_id FROM Checkouts c
                JOIN BookCopies bc ON c.copy_id = bc.copy_id
                WHERE c.student_id = %s AND bc.isbn = %s
            """
            cursor.execute(check_existing_query, (student_id, isbn))
            if cursor.fetchone():
                raise ValueError("You already have a copy of this book checked out!")

            find_copy_query = "SELECT copy_id FROM BookCopies WHERE isbn = %s AND status = 'Available' LIMIT 1"
            cursor.execute(find_copy_query, (isbn,))
            available_copy = cursor.fetchone()

            if not available_copy:
                raise ValueError("Sorry, no copies of this book are currently available.")

            copy_id = available_copy[0]
            cursor.execute(
                "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)",
                (student_id, copy_id, datetime.date.today()),
            )
            cursor.execute("UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s", (copy_id,))
            conn.commit()
            return copy_id
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # Will display a checkout receipt and requires no input
    def print_receipt(self) -> None:
        pass

    # Updates the status upon checkout (overdue, borrowed, returned)
    def status_update(self, status: str) -> None:
        pass
