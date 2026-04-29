import datetime

class OverdueBook:
    def __init__(self, checkout_id, student_id, copy_id, due_date, fine_rate=0.50):
        self.checkout_id = checkout_id
        self.student_id = student_id
        self.copy_id = copy_id
        self.due_date = due_date
        self.fine_rate = fine_rate # e.g., $0.50 per day late

    def calculate_days_overdue(self) -> int:
        """Calculates the number of days past the due date."""
        today = datetime.date.today()
        if today > self.due_date:
            delta = today - self.due_date
            return delta.days
        return 0

    def calculate_fine(self) -> float:
        """Calculates the total fine based on days overdue."""
        days_late = self.calculate_days_overdue()
        return days_late * self.fine_rate

    def send_overdue_notice(self) -> None:
        """Logic to notify the student (e.g., via email)."""
        pass