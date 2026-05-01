class BookReturn:
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
            find_checkout_query = """
                SELECT c.checkout_id, c.copy_id FROM Checkouts c
                JOIN BookCopies bc ON c.copy_id = bc.copy_id
                WHERE c.student_id = %s AND bc.isbn = %s
            """
            cursor.execute(find_checkout_query, (student_id, isbn))
            checkout_record = cursor.fetchone()

            if not checkout_record:
                raise ValueError("You don't currently have a copy of this book checked out.")

            cursor.execute("DELETE FROM Checkouts WHERE checkout_id = %s", (checkout_record[0],))
            assigned_student_id = ReserveBook.assign_returned_copy_to_next_reservation(
                cursor,
                isbn,
                checkout_record[1],
            )
            conn.commit()
            return {
                "copy_id": checkout_record[1],
                "assigned_student_id": assigned_student_id,
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()
