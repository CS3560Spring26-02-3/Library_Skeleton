class BookCopies:
    def __init__(self, total_copies_of_books, location, book_list=None):
        self.total_copies_of_books = total_copies_of_books
        self.location = location
        self.book_list = book_list if book_list is not None else []

    def status_update(self, change):
        self.total_copies_of_books += change
        print(f"Updated total copies: {self.total_copies_of_books}")

    def list_books(self):
        print("Books in this location:")
        for book in self.book_list:
            print(f"- {book}")

    def add_book(self, book):
        self.book_list.append(book)
        self.total_copies_of_books += 1