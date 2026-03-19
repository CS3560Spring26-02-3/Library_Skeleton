class BookCopies:
    def __init__(self, total_copies_of_books, location, book_list=None):
        self.total_copies_of_books = total_copies_of_books
        self.location = location
        self.book_list = book_list if book_list is not None else []

    # Will update the number of books whether user adds or removes
    def status_update(self, change: int) -> None:
        pass

    # Will return a list of all the books
    def list_books(self) -> list:
        pass

    # Will add a new book to the collection and the input will be of string data type
    def add_book(self, book) -> None:
        pass