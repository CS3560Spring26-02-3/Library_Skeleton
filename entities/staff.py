class Staff:
    def __init__(self, ssd, telephone_number, email_address, physical_address):
        self.ssd = ssd
        self.telephone_number = telephone_number
        self.email_address = email_address
        self.physical_address = physical_address

    # --- Methods from diagram ---

    def create_card(self, member_name):
        print(f"Library card created for {member_name}")

    def delete_account(self, member_name):
        print(f"Account for {member_name} has been deleted")

    def view_member_account(self, member_name):
        print(f"Viewing account details for {member_name}")

    def add_book(self, book_title):
        print(f"Book '{book_title}' has been added to the system")

    # def display_info(self):
    #     print(f"SSD: {self.ssd}")
    #     print(f"Phone: {self.telephone_number}")
    #     print(f"Email: {self.email_address}")
    #     print(f"Address: {self.physical_address}")