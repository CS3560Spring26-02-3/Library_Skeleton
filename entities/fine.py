class Fine:
    def __init__(self, paid=False):
        self.paid = paid

    def check_return_date(self, return_date):
        print(f"Checking return date: {return_date}")

    def notify_staff(self):
        print("Staff has been notified.")

    def notify_student(self):
        print("Student has been notified.")

    def send_fine(self, amount):
        print(f"Fine of ${amount} has been sent.")

    def check_if_paid(self):
        print(f"Paid: {self.paid}")

    def mark_as_paid(self):
        self.paid = True
        print("Fine has been paid.")