class Book:
    SEARCH_COLUMNS = {
        "Title": "b.title",
        "Author": "b.author",
        "ISBN": "b.isbn",
        "Genre": "b.genre",
    }

    def __init__(self, title, author, category, isbn, genre):
        self.title = title
        self.author = author
        self.category = category
        self.isbn = isbn
        self.genre = genre

    @classmethod
    def add_new(cls, title, author, isbn, genre, category):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Books (title, author, isbn, genre, category) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (title, author, isbn, genre, category))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def search(cls, search_by="ISBN", search_term=""):
        from entities.main import create_connection

        if search_by not in cls.SEARCH_COLUMNS:
            raise ValueError(f"Unsupported search type: {search_by}")

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = """
                SELECT b.isbn, b.title, b.author, b.genre, b.category,
                    COUNT(bc.copy_id) as total_copies,
                    COALESCE(SUM(CASE WHEN bc.status = 'Available' THEN 1 ELSE 0 END), 0) as available
                FROM Books b
                LEFT JOIN BookCopies bc ON b.isbn = bc.isbn
            """
            values = ()

            if search_term:
                query += f" WHERE {cls.SEARCH_COLUMNS[search_by]} LIKE %s"
                values = (f"%{search_term}%",)

            query += """
                GROUP BY b.isbn, b.title, b.author, b.genre, b.category
                ORDER BY b.isbn
            """
            cursor.execute(query, values)
            return [
                {
                    "isbn": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3],
                    "category": row[4],
                    "total_copies": row[5],
                    "available": row[6] if row[6] else 0,
                }
                for row in cursor.fetchall()
            ]
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def find_by_title_or_isbn(cls, search_term):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "SELECT isbn, title, author, genre FROM Books WHERE isbn = %s OR title LIKE %s"
            cursor.execute(query, (search_term, f"%{search_term}%"))
            row = cursor.fetchone()
            if not row:
                return None

            return {
                "isbn": row[0],
                "title": row[1],
                "author": row[2],
                "genre": row[3],
            }
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @classmethod
    def remove_by_isbn(cls, isbn):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Books WHERE isbn = %s", (isbn,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # def display_info(self):
    #     print(f"Title: {self.title}")
    #     print(f"Author: {self.author}")
    #     print(f"Category: {self.category}")
    #     print(f"ISBN: {self.isbn}")
    #     print(f"Genre: {self.genre}")
