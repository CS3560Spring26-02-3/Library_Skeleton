class Student:
    def __init__(self, telephone_number, physical_address, email_address):
        self.telephone_number = telephone_number
        self.physical_address = physical_address
        self.email_address = email_address
        self.books_checked_out = []

    def checkout_book(self, book) -> None:
        pass

    def request_library_card(self) -> None:
        pass

    def request_deletion(self) -> None:
        pass

    def pay_fine(self, amount: float) -> None:
        pass

    # def display_info(self):
    #     print(f"Telephone Number: {self.telephone_number}")
    #     print(f"Physical Address: {self.physical_address}")
    #     print(f"Email Address: {self.email_address}")
    #     print(f"Books Checked Out: {self.books_checked_out}")