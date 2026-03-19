class Student:
    def __init__(self, telephone_number, physical_address, email_address):
        self.telephone_number = telephone_number
        self.physical_address = physical_address
        self.email_address = email_address
        self.books_checked_out = []

    # Allows for adding book to check out list and takes in a string
    def checkout_book(self, book) -> None:
        pass

    # Allows to send a request for library card
    def request_library_card(self) -> None:
        pass

    # Allows to request deleltion of the account
    def request_deletion(self) -> None:
        pass

    # Will process payment with the input of a float data type
    def pay_fine(self, amount: float) -> None:
        pass

    # def display_info(self):
    #     print(f"Telephone Number: {self.telephone_number}")
    #     print(f"Physical Address: {self.physical_address}")
    #     print(f"Email Address: {self.email_address}")
    #     print(f"Books Checked Out: {self.books_checked_out}")