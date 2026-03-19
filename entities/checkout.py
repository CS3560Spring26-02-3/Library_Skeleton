class Checkout:
    def __init__(self, return_date, books_checked_out=None):
        self.return_date = return_date
        self.books_checked_out = books_checked_out if books_checked_out is not None else []

    def print_receipt(self) -> None:
        pass