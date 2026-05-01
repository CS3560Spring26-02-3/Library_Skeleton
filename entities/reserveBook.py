import datetime

class ReserveBook:
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    FULFILLED = "Fulfilled"

    def __init__(self, student_id, isbn, reservation_date=None, status="Pending"):
        self.student_id = student_id
        self.isbn = isbn
        self.reservation_date = reservation_date if reservation_date else datetime.date.today()
        self.status = status # 'Pending', 'Fulfilled', or 'Cancelled'

    def place_reservation(self) -> int:
        """Logic to insert the reservation into the database."""
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT isbn FROM Books WHERE isbn = %s", (self.isbn,))
            if not cursor.fetchone():
                raise ValueError("No book exists with that ISBN.")

            cursor.execute(
                """
                SELECT reservation_id
                FROM Reservations
                WHERE isbn = %s AND status = %s
                ORDER BY reservation_date, reservation_id
                LIMIT 1
                """,
                (self.isbn, self.PENDING),
            )
            first_pending = cursor.fetchone()

            cursor.execute(
                "SELECT copy_id FROM BookCopies WHERE isbn = %s AND status = 'Available' LIMIT 1",
                (self.isbn,),
            )
            if cursor.fetchone() and not first_pending:
                raise ValueError("This book is available now. Please check it out instead of reserving it.")

            cursor.execute(
                """
                SELECT c.checkout_id
                FROM Checkouts c
                JOIN BookCopies bc ON c.copy_id = bc.copy_id
                WHERE c.student_id = %s AND bc.isbn = %s
                """,
                (self.student_id, self.isbn),
            )
            if cursor.fetchone():
                raise ValueError("You already have this book checked out.")

            cursor.execute(
                """
                SELECT reservation_id FROM Reservations
                WHERE student_id = %s AND isbn = %s AND status = %s
                """,
                (self.student_id, self.isbn, self.PENDING),
            )
            if cursor.fetchone():
                raise ValueError("You already have a pending reservation for this book.")

            cursor.execute(
                """
                INSERT INTO Reservations (student_id, isbn, reservation_date, status)
                VALUES (%s, %s, %s, %s)
                """,
                (self.student_id, self.isbn, self.reservation_date, self.status),
            )
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
    def get_next_pending(cls, isbn):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT reservation_id, student_id
                FROM Reservations
                WHERE isbn = %s AND status = %s
                ORDER BY reservation_date, reservation_id
                LIMIT 1
                """,
                (isbn, cls.PENDING),
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def student_can_checkout(cls, student_id, isbn) -> bool:
        next_reservation = cls.get_next_pending(isbn)
        return next_reservation is None or next_reservation[1] == student_id

    @classmethod
    def fulfill_for_student(cls, student_id, isbn, cursor) -> None:
        cursor.execute(
            """
            UPDATE Reservations
            SET status = %s
            WHERE student_id = %s AND isbn = %s AND status = %s
            """,
            (cls.FULFILLED, student_id, isbn, cls.PENDING),
        )

    @classmethod
    def assign_returned_copy_to_next_reservation(cls, cursor, isbn, copy_id):
        cursor.execute(
            """
            SELECT reservation_id, student_id
            FROM Reservations
            WHERE isbn = %s AND status = %s
            ORDER BY reservation_date, reservation_id
            LIMIT 1
            """,
            (isbn, cls.PENDING),
        )
        next_reservation = cursor.fetchone()

        if not next_reservation:
            cursor.execute("UPDATE BookCopies SET status = 'Available' WHERE copy_id = %s", (copy_id,))
            return None

        reservation_id, next_student_id = next_reservation
        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=14)

        cursor.execute(
            """
            INSERT INTO Checkouts (student_id, copy_id, checkout_date, due_date)
            VALUES (%s, %s, %s, %s)
            """,
            (next_student_id, copy_id, today, due_date),
        )
        cursor.execute("UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s", (copy_id,))
        cursor.execute(
            "UPDATE Reservations SET status = %s WHERE reservation_id = %s",
            (cls.FULFILLED, reservation_id),
        )
        return next_student_id

    def check_position_in_queue(self) -> int:
        """Returns the user's place in line for this specific ISBN."""
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT reservation_id, student_id
                FROM Reservations
                WHERE isbn = %s AND status = %s
                ORDER BY reservation_date, reservation_id
                """,
                (self.isbn, self.PENDING),
            )

            for position, row in enumerate(cursor.fetchall(), start=1):
                if row[1] == self.student_id:
                    return position

            raise ValueError("You do not have a pending reservation for this book.")
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def cancel_reservation(self) -> None:
        """Updates the status to Cancelled."""
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Reservations
                SET status = %s
                WHERE student_id = %s AND isbn = %s AND status = %s
                """,
                (self.CANCELLED, self.student_id, self.isbn, self.PENDING),
            )

            if cursor.rowcount == 0:
                raise ValueError("No pending reservation was found for this book.")

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()
