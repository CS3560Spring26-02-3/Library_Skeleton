class BookCopies:
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"

    def __init__(self, total_copies_of_books, location, book_list=None):
        self.total_copies_of_books = total_copies_of_books
        self.location = location
        self.book_list = book_list if book_list is not None else []

    @classmethod
    def add_copy(cls, isbn, location, status=AVAILABLE):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO BookCopies (isbn, location, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (isbn, location, status))
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # Will update the number of books whether user adds or removes
    def status_update(self, change: int) -> None:
        pass

    # Will return a list of all the books
    def list_books(self) -> list:
        pass

    # Will add a new book to the collection and the input will be of string data type
    def add_book(self, book) -> None:
        pass
