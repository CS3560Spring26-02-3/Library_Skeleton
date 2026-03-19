class BookCopies:
    def __init__(self, total_copies_of_books, location, book_list=None):
        self.total_copies_of_books = total_copies_of_books
        self.location = location
        self.book_list = book_list if book_list is not None else []

    def status_update(self, change: int) -> None:
        pass

    def list_books(self) -> list:
        pass

    def add_book(self, book) -> None:
        pass