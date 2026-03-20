class Fine:
    def __init__(self, paid=False):
        self.paid = paid


    #Checks if a book is overdue and the input will be a string for comparison
    def check_return_date(self, return_date: str) -> None:
        pass

    # Checks if the book is overdue or has a fine
    def check_book_status(self, book) -> bool:
        pass

    # Notifies staff if a book is overdue
    def notify_staff(self) -> None:
        pass

    # notifies a student if a book is overdue
    def notify_student(self) -> None:
        pass

    # Issues a fine to the student where the input is of float (fine)
    def send_fine(self, amount: float) -> None:
        pass

    # Checks if the fine has been paid, no input required
    def check_if_paid(self) -> bool:
        pass

    # Updates the status of checkout (overdue, borrowed, returned)
    def status_update(self, status: str) -> None:
        pass