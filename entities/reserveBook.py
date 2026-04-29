import datetime

class ReserveBook:
    def __init__(self, student_id, isbn, reservation_date=None, status="Pending"):
        self.student_id = student_id
        self.isbn = isbn
        self.reservation_date = reservation_date if reservation_date else datetime.date.today()
        self.status = status # 'Pending', 'Fulfilled', or 'Cancelled'

    def place_reservation(self) -> None:
        """Logic to insert the reservation into the database."""
        pass

    def check_position_in_queue(self) -> int:
        """Returns the user's place in line for this specific ISBN."""
        pass

    def cancel_reservation(self) -> None:
        """Updates the status to Cancelled."""
        pass