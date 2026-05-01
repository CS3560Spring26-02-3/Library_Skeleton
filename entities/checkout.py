import datetime


class Checkout:
    LOAN_DAYS = 14

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
            today = datetime.date.today()
            due_date = today + datetime.timedelta(days=cls.LOAN_DAYS)
            cursor.execute(
                "INSERT INTO Checkouts (student_id, copy_id, checkout_date, due_date) VALUES (%s, %s, %s, %s)",
                (student_id, copy_id, today, due_date),
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
        from entities.reserveBook import ReserveBook

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

            next_reservation = ReserveBook.get_next_pending(isbn)
            if next_reservation and next_reservation[1] != student_id:
                raise ValueError("This book is reserved for another student.")

            find_copy_query = "SELECT copy_id FROM BookCopies WHERE isbn = %s AND status = 'Available' LIMIT 1"
            cursor.execute(find_copy_query, (isbn,))
            available_copy = cursor.fetchone()

            if not available_copy:
                raise ValueError("Sorry, no copies of this book are currently available.")

            copy_id = available_copy[0]
            today = datetime.date.today()
            due_date = today + datetime.timedelta(days=cls.LOAN_DAYS)
            cursor.execute(
                "INSERT INTO Checkouts (student_id, copy_id, checkout_date, due_date) VALUES (%s, %s, %s, %s)",
                (student_id, copy_id, today, due_date),
            )
            cursor.execute("UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s", (copy_id,))
            ReserveBook.fulfill_for_student(student_id, isbn, cursor)
            conn.commit()
            return copy_id
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # Receipt and Billing logic
    def print_receipt(self, student_name: str, book_title: str) -> str:
        receipt = (
            f"--- CHECKOUT RECIEPT ---\n"
            f"STUDENT: {student_name}\n"
            f"ITEM: {book_title}\n"
            f"DUE DATE: {self.return_date}\n"
            f"------------------------\n"
            f"Thank you for using the library!"
        )
        return receipt
    def create_billing_summary(self, student_name: str, days_late: int, book_title: str) -> str:
        """Generates a formal bill for overdue books."""
        daily_rate = 0.50
        total_fine = float(max(0, days_late) * daily_rate)
        
        bill_text = (
            f"--- OFFICIAL LIBRARY BILL ---\n"
            f"DATE: {datetime.date.today()}\n"
            f"STUDENT: {student_name}\n"
            f"ITEM: {book_title}\n"
            f"STATUS: {days_late} Days Overdue\n"
            f"-----------------------------\n"
            f"TOTAL FINE DUE: ${total_fine:.2f}\n"
            f"Please settle this at the front desk."
        )
        return bill_text


    @classmethod
    def renew(cls, student_id, isbn, extra_days=7):
        from entities.main import create_connection
        import datetime

        if extra_days <= 0:
            raise ValueError("Renewal days must be a positive number.")

        if extra_days > 14:
            raise ValueError("You cannot extend more than 14 days at a time.")

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to database.")

        cursor = None
        try:
            cursor = conn.cursor()

            query = """
                SELECT c.checkout_id, c.due_date FROM Checkouts c JOIN BookCopies bc ON c.copy_id = bc.copy_id
                WHERE c.student_id = %s AND bc.isbn = %s
            """
            cursor.execute(query, (student_id, isbn))
            row = cursor.fetchone()

            if not row:
                raise ValueError("No active checkout found for this book.")

            checkout_id, current_due = row

            if current_due is None:
                current_due = datetime.date.today()

            new_due = current_due + datetime.timedelta(days=extra_days)

            update_query = """
                UPDATE Checkouts SET due_date = %s WHERE checkout_id = %s """
            
            cursor.execute(update_query, (new_due, checkout_id))
            conn.commit()

            return new_due

        finally:
            if cursor:
                cursor.close()
            conn.close()



    # Updates the status upon checkout (overdue, borrowed, returned)
    def status_update(self, status: str) -> str:
        """Returns a string describing the current status update."""
        return f"System Alert: Transaction status updated to '{status}'."
