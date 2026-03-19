class Staff:
    def __init__(self, ssn: str, telephone_number: str, email_address: str, physical_address: str) -> None:
        self.ssn = ssn
        self.telephone_number = telephone_number
        self.email_address = email_address
        self.physical_address = physical_address

    def create_card(self, member_name: str) -> None:
        pass

    def delete_account(self, member_name: str) -> None:
        pass

    def view_member_account(self, member_name: str) -> dict:
        pass

    def add_book(self, book_title: str) -> None:
        pass

    # def display_info(self):
    #     print(f"SSD: {self.ssd}")
    #     print(f"Phone: {self.telephone_number}")
    #     print(f"Email: {self.email_address}")
    #     print(f"Address: {self.physical_address}")