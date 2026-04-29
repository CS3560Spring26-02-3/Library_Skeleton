class Staff:

    def __init__(self, ssn: str, telephone_number: str, email_address: str, physical_address: str) -> None:
        self.ssn = ssn
        self.telephone_number = telephone_number
        self.email_address = email_address
        self.physical_address = physical_address

    @classmethod
    def authenticate(cls, email, password):
        from entities.main import create_connection

        conn = create_connection()
        if not conn:
            raise ConnectionError("Could not connect to the database.")

        cursor = None
        try:
            cursor = conn.cursor()
            query = "SELECT staff_id, name FROM Staff WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            row = cursor.fetchone()
            if not row:
                return None

            return {
                "staff_id": row[0],
                "name": row[1],
            }
        finally:
            if cursor:
                cursor.close()
            conn.close()

    #Creates a library card and will return a string
    def create_card(self, member_name: str) -> None:
        pass

    #Deletes the account and will return a string
    def delete_account(self, member_name: str) -> None:
        pass

    #will return a string of the member account
    def view_member_account(self, member_name: str) -> dict:
        pass

    #adds a string in the form of the name of a book
    def add_book(self, book_title: str) -> None:
        pass

    # def display_info(self):
    #     print(f"SSD: {self.ssd}")
    #     print(f"Phone: {self.telephone_number}")
    #     print(f"Email: {self.email_address}")
    #     print(f"Address: {self.physical_address}")
