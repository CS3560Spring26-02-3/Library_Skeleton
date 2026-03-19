class StaffAccount:
    def __init__(self, employee_id, employee_password, contact_info, ssd_on_record):
        self.employee_id = employee_id
        self.employee_password = employee_password
        self.contact_info = contact_info
        self.ssd_on_record = ssd_on_record

    def login(self, password: str) -> bool:
        pass

    def update_contact_info(self, new_contact_info: str) -> None:
        pass

    # def display_info(self):
    #     print(f"Employee ID: {self.employee_id}")
    #     print(f"Contact Info: {self.contact_info}")
    #     print(f"SSD on Record: {self.ssd_on_record}")