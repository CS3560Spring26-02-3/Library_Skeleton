import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from entities.book import Book
from entities.book_copies import BookCopies
from entities.book_return import BookReturn
from entities.checkout import Checkout
from entities.staff import Staff
from entities.student import Student
from entities.overdueBook import OverdueBook
from entities.reserveBook import ReserveBook

DEMO_FORCE_OVERDUE_RETURN = False
DEMO_OVERDUE_DAYS = 5

class LoginSignupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Login")
        self.root.geometry("400x300")

        tab_control = ttk.Notebook(root)

        self.tab_login = ttk.Frame(tab_control)
        self.tab_signup = ttk.Frame(tab_control)
        self.tab_staff = ttk.Frame(tab_control)

        tab_control.add(self.tab_login, text="Login")
        tab_control.add(self.tab_signup, text="Sign Up")
        tab_control.add(self.tab_staff, text="Staff Login")
        tab_control.pack(expand=1, fill="both")

        self.setup_login_tab()
        self.setup_signup_tab()
        self.setup_staff_tab()

    def setup_login_tab(self):
        tk.Label(self.tab_login, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_login_email = tk.Entry(self.tab_login)
        self.entry_login_email.grid(row=0, column=1)

        tk.Label(self.tab_login, text="PIN:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_login_pin = tk.Entry(self.tab_login, show="*")
        self.entry_login_pin.grid(row=1, column=1)

        tk.Button(self.tab_login, text="Login", command=self.login_student).grid(row=2, column=1, pady=20)

    def setup_signup_tab(self):
        tk.Label(self.tab_signup, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_signup_name = tk.Entry(self.tab_signup)
        self.entry_signup_name.grid(row=0, column=1)

        tk.Label(self.tab_signup, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_signup_email = tk.Entry(self.tab_signup)
        self.entry_signup_email.grid(row=1, column=1)

        tk.Label(self.tab_signup, text="PIN:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_signup_pin = tk.Entry(self.tab_signup, show="*")
        self.entry_signup_pin.grid(row=2, column=1)

        tk.Button(self.tab_signup, text="Create Account", command=self.signup_student).grid(row=3, column=1, pady=20)

    def signup_student(self):
        name = self.entry_signup_name.get().strip()
        email = self.entry_signup_email.get().strip()
        pin = self.entry_signup_pin.get().strip()

        if not name or not email or not pin:
            messagebox.showwarning("Input Error", "All sign up fields are required.")
            return

        try:
            Student.create_account(name, email, pin)
            messagebox.showinfo("Success", "Account created successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Sign up failed: {e}")

    def login_student(self):
        email = self.entry_login_email.get().strip()
        pin = self.entry_login_pin.get().strip()

        if not email or not pin:
            messagebox.showwarning("Input Error", "Email and PIN are required.")
            return

        try:
            student = Student.authenticate(email, pin)
            if student:
                messagebox.showinfo("Success", f"Welcome, {student['name']}!")
                self.root.destroy()
                main_root = tk.Tk()
                app = LibraryGUI(
                    main_root,
                    current_student_id=student["student_id"],
                    current_student_name=student["name"],
                    current_role='student',
                )
                main_root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid email or PIN.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")

    def setup_staff_tab(self):
        tk.Label(self.tab_staff, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_staff_email = tk.Entry(self.tab_staff)
        self.entry_staff_email.grid(row=0, column=1)

        tk.Label(self.tab_staff, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_staff_password = tk.Entry(self.tab_staff, show="*")
        self.entry_staff_password.grid(row=1, column=1)

        tk.Button(self.tab_staff, text="Staff Login", command=self.login_staff).grid(row=2, column=1, pady=20)

    def login_staff(self):
        email = self.entry_staff_email.get().strip()
        password = self.entry_staff_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Email and Password are required.")
            return

        try:
            staff = Staff.authenticate(email, password)
            if staff:
                messagebox.showinfo("Success", f"Welcome, {staff['name']}!")
                self.root.destroy()
                main_root = tk.Tk()
                app = LibraryGUI(main_root, current_role='staff', current_student_name=staff["name"])
                main_root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")


class LibraryGUI:
    def __init__(self, root, current_student_id=None, current_student_name=None, current_role='student'):
        self.root = root
        self.current_student_id = current_student_id
        self.current_student_name = current_student_name
        self.current_role = current_role

        self.root.title("Library Management System")
        self.root.geometry("500x400")

        tab_control = ttk.Notebook(root)

        # Search — visible to everyone
        self.tab_search = ttk.Frame(tab_control)
        tab_control.add(self.tab_search, text='Search Books')

        self.tab_checkout = ttk.Frame(tab_control)
        self.tab_return = ttk.Frame(tab_control)
        self.tab_renew = ttk.Frame(tab_control)
        self.tab_reserve = ttk.Frame(tab_control)
        tab_control.add(self.tab_checkout, text='Checkout')
        tab_control.add(self.tab_return, text='Return Book')
        tab_control.add(self.tab_renew, text='Renew Book')
        tab_control.add(self.tab_reserve, text='Reserve Book')

        # Staff only
        if current_role == 'staff':
            self.tab_add_book = ttk.Frame(tab_control)
            self.tab_add_copy = ttk.Frame(tab_control)
            self.tab_remove_book = ttk.Frame(tab_control)
            self.tab_modify_book = ttk.Frame(tab_control)
            tab_control.add(self.tab_add_book, text='Add Book (Staff)')
            tab_control.add(self.tab_add_copy, text='Add Copy (Staff)')
            tab_control.add(self.tab_remove_book, text='Remove Book (Staff)')
            tab_control.add(self.tab_modify_book, text='Modify Book (Staff)')
            self.setup_add_book_tab()
            self.setup_add_copy_tab()
            self.setup_remove_book_tab()
            self.setup_modify_book_tab()

        tab_control.pack(expand=1, fill="both")

        tk.Button(self.root, text="Logout", command=self.logout,
                  bg="#cc0000", fg="white").place(relx=0.5, rely=0.95, anchor="center")

        self.setup_search_tab()
        self.setup_checkout_tab()
        self.setup_return_tab()
        self.setup_renew_tab()
        self.setup_reserve_tab()

    def setup_add_book_tab(self):
        tk.Label(self.tab_add_book, text="Title:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_title = tk.Entry(self.tab_add_book)
        self.entry_title.grid(row=0, column=1)

        tk.Label(self.tab_add_book, text="Author:").grid(row=1, column=0, pady=10, padx=10)
        self.entry_author = tk.Entry(self.tab_add_book)
        self.entry_author.grid(row=1, column=1)

        tk.Label(self.tab_add_book, text="ISBN:").grid(row=2, column=0, pady=10, padx=10)
        self.entry_isbn = tk.Entry(self.tab_add_book)
        self.entry_isbn.grid(row=2, column=1)

        tk.Label(self.tab_add_book, text="Genre:").grid(row=3, column=0, pady=10, padx=10)
        self.entry_genre = tk.Entry(self.tab_add_book)
        self.entry_genre.grid(row=3, column=1)

        tk.Label(self.tab_add_book, text="Category:").grid(row=4, column=0, pady=10, padx=10)
        self.entry_category = tk.Entry(self.tab_add_book)
        self.entry_category.grid(row=4, column=1)

        tk.Button(self.tab_add_book, text="Add Book", command=self.submit_new_book).grid(row=5, column=1, pady=20)

    def setup_add_copy_tab(self):
        tk.Label(self.tab_add_copy, text="ISBN (Must match an existing book):").grid(row=0, column=0, pady=10, padx=10)
        self.entry_copy_isbn = tk.Entry(self.tab_add_copy)
        self.entry_copy_isbn.grid(row=0, column=1)

        tk.Label(self.tab_add_copy, text="Location (e.g., Shelf 3A):").grid(row=1, column=0, pady=10, padx=10)
        self.entry_copy_location = tk.Entry(self.tab_add_copy)
        self.entry_copy_location.grid(row=1, column=1)

        tk.Button(self.tab_add_copy, text="Add Physical Copy", command=self.submit_new_copy).grid(row=2, column=1, pady=20)

    def setup_checkout_tab(self):
        tk.Label(self.tab_checkout, text="Book ISBN:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_checkout_isbn = tk.Entry(self.tab_checkout)
        self.entry_checkout_isbn.grid(row=0, column=1)

        tk.Button(self.tab_checkout, text="Process Checkout", command=self.process_checkout).grid(row=1, column=1, pady=20)

    def setup_return_tab(self):
        tk.Label(self.tab_return, text="Book ISBN to Return:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_return_isbn = tk.Entry(self.tab_return)
        self.entry_return_isbn.grid(row=0, column=1)

        tk.Button(self.tab_return, text="Process Return", command=self.process_return).grid(row=1, column=1, pady=20)

    def setup_reserve_tab(self):
        tk.Label(self.tab_reserve, text="Book ISBN:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_reserve_isbn = tk.Entry(self.tab_reserve)
        self.entry_reserve_isbn.grid(row=0, column=1)

        tk.Button(self.tab_reserve, text="Place Reservation", command=self.place_reservation).grid(row=1, column=1, pady=10)
        tk.Button(self.tab_reserve, text="Check Queue Position", command=self.check_reservation_position).grid(row=2, column=1, pady=10)
        tk.Button(self.tab_reserve, text="Cancel Reservation", command=self.cancel_reservation).grid(row=3, column=1, pady=10)

    def setup_search_tab(self):
        tk.Label(self.tab_search, text="Search By:").grid(row=0, column=0, padx=10, pady=10)
    
        self.search_type = ttk.Combobox(self.tab_search, values=["Title", "Author", "ISBN", "Genre"],
                                     state="readonly", width=10)
        self.search_type.current(2)  # Default to ISBN
        self.search_type.grid(row=0, column=1, padx=5)

        self.entry_search = tk.Entry(self.tab_search, width=25)
        self.entry_search.grid(row=0, column=2, padx=5)

        tk.Button(self.tab_search, text="Search", command=self.search_books).grid(row=0, column=3, padx=5)

        # Results box with scrollbar
        frame = tk.Frame(self.tab_search)
        frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.search_results = tk.Listbox(frame, width=65, height=12, yscrollcommand=scrollbar.set)
        self.search_results.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.search_results.yview)
        self.search_books()

    def search_books(self):
        search_term = self.entry_search.get().strip()
        search_by = self.search_type.get()

        try:
            results = Book.search(search_by, search_term)
            self.search_results.delete(0, tk.END)
            if results:
                for book in results:
                    self.search_results.insert(
                        tk.END,
                        "ISBN: {isbn} | {title} | by {author} | Genre: {genre} | Available: {available}/{total}".format(
                            isbn=book["isbn"],
                            title=book["title"],
                            author=book["author"],
                            genre=book["genre"],
                            available=book["available"],
                            total=book["total_copies"],
                        ),
                    )
            else:
                self.search_results.insert(tk.END, "No books found.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def submit_new_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        isbn = self.entry_isbn.get().strip()
        genre = self.entry_genre.get().strip()
        category = self.entry_category.get().strip()

        if title and author and isbn:
            try:
                Book.add_new(title, author, isbn, genre, category)
                messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add book: {e}")
        else:
            messagebox.showwarning("Input Error", "Title, Author, and ISBN are required.")

    def submit_new_copy(self):
        isbn = self.entry_copy_isbn.get().strip()
        location = self.entry_copy_location.get().strip()

        if isbn and location:
            try:
                new_copy_id = BookCopies.add_copy(isbn, location)
                messagebox.showinfo("Success", f"Copy added successfully!\n\nThe new Copy ID is: {new_copy_id}")
                self.entry_copy_isbn.delete(0, tk.END)
                self.entry_copy_location.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add copy: {e}")
        else:
            messagebox.showwarning("Input Error", "Both ISBN and Location are required.")

    def process_checkout(self):
        isbn = self.entry_checkout_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            copy_id = Checkout.process(self.current_student_id, isbn)
            #Calculate a theoretical due date for the receipt
            # We assume a 14-day loan period for the visual receipt
            due_date_val = datetime.date.today() + datetime.timedelta(days=14)

            # Initialize Checkout class to use the print_receipt method
            receipt_generator = Checkout(return_date=str(due_date_val))
            receipt_text = receipt_generator.print_receipt(self.current_student_name, f"ISBN: {isbn}")
            
            # Show the formal receipt
            messagebox.showinfo("Success", f"Checkout successful!\n\nYou have checked out Copy ID: {copy_id}")
            self.entry_checkout_isbn.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Checkout Failed", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to checkout: {e}")

    def process_return(self):
        isbn = self.entry_return_isbn.get().strip()
        conn = None
        cursor = None

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            # 1. PRE-PROCESS: We need to get the due_date and title BEFORE the record is deleted
            from entities.main import create_connection
            conn = create_connection()
            if not conn:
                raise ConnectionError("Could not connect to the database.")
            cursor = conn.cursor()
            
            # Query to find the specific checkout details for this student/book
            query = """
                SELECT c.checkout_id, c.copy_id, b.title, c.checkout_date, c.due_date
                FROM Checkouts c 
                JOIN BookCopies bc ON c.copy_id = bc.copy_id 
                JOIN Books b ON bc.isbn = b.isbn
                WHERE c.student_id = %s AND b.isbn = %s
            """
            cursor.execute(query, (self.current_student_id, isbn))
            record = cursor.fetchone()

            if not record:
                messagebox.showwarning("Not Found", "You do not have this book checked out.")
                return

            checkout_id, copy_id, title, checkout_date, due_date = record
            if due_date is None:
                due_date = checkout_date + datetime.timedelta(days=Checkout.LOAN_DAYS)
            if DEMO_FORCE_OVERDUE_RETURN:
                due_date = datetime.date.today() - datetime.timedelta(days=DEMO_OVERDUE_DAYS)

            # 2. Process the return in the database (this deletes the checkout)
            BookReturn.process(self.current_student_id, isbn)
            
            # 3. INTEGRATION: Check for fines using OverdueBook
            ovd = OverdueBook(checkout_id, self.current_student_id, copy_id, due_date)
            days_late = ovd.calculate_days_overdue()

            if days_late > 0:
                # 4.  If late, show the formal bill
                billing_gen = Checkout(return_date=str(datetime.date.today()))
                bill_message = billing_gen.create_billing_summary(self.current_student_name, days_late, title)
                messagebox.showinfo("Return Processed - Fine Due", bill_message)
            else:
                # Standard success message
                messagebox.showinfo("Success", f"'{title}' returned on time! Thank you.")
            
            self.entry_return_isbn.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to return book: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def place_reservation(self):
        isbn = self.entry_reserve_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            reservation = ReserveBook(self.current_student_id, isbn)
            reservation_id = reservation.place_reservation()
            position = reservation.check_position_in_queue()
            messagebox.showinfo(
                "Reservation Placed",
                f"Reservation ID: {reservation_id}\nQueue position: {position}"
            )
            self.entry_reserve_isbn.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Reservation Failed", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to reserve book: {e}")

    def check_reservation_position(self):
        isbn = self.entry_reserve_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            reservation = ReserveBook(self.current_student_id, isbn)
            position = reservation.check_position_in_queue()
            messagebox.showinfo("Queue Position", f"Your queue position is: {position}")
        except ValueError as e:
            messagebox.showwarning("Reservation Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to check reservation: {e}")

    def cancel_reservation(self):
        isbn = self.entry_reserve_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            reservation = ReserveBook(self.current_student_id, isbn)
            reservation.cancel_reservation()
            messagebox.showinfo("Reservation Cancelled", "Your reservation has been cancelled.")
            self.entry_reserve_isbn.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Reservation Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to cancel reservation: {e}")

    def setup_remove_book_tab(self):
        tk.Label(self.tab_remove_book, text="Search by Title or ISBN:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_remove_search = tk.Entry(self.tab_remove_book, width=25)
        self.entry_remove_search.grid(row=0, column=1, padx=5)
        tk.Button(self.tab_remove_book, text="Find Book", command=self.find_book_to_remove).grid(row=0, column=2, padx=5)

        self.remove_book_info = tk.Label(self.tab_remove_book, text="", fg="gray")
        self.remove_book_info.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Button(self.tab_remove_book, text="Remove Book", command=self.remove_book,
                bg="#cc0000", fg="white").grid(row=2, column=1, pady=10)

        self.current_remove_isbn = None

    def find_book_to_remove(self):
        search_term = self.entry_remove_search.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a title or ISBN.")
            return

        try:
            book = Book.find_by_title_or_isbn(search_term)
            if book:
                self.current_remove_isbn = book["isbn"]
                self.remove_book_info.config(
                    text=f"Found: '{book['title']}' by {book['author']} | Genre: {book['genre']}\nISBN: {book['isbn']}",
                    fg="black"
                )
            else:
                self.current_remove_isbn = None
                self.remove_book_info.config(text="No book found.", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def remove_book(self):
        if not self.current_remove_isbn:
            messagebox.showwarning("No Book Selected", "Please search for a book first.")
            return

        confirm = messagebox.askyesno("Confirm Remove",
            f"Are you sure you want to remove this book?\nISBN: {self.current_remove_isbn}\n\nThis will also remove all copies!")

        if not confirm:
            return

        try:
            Book.remove_by_isbn(self.current_remove_isbn)
            messagebox.showinfo("Success", "Book and all its copies have been removed.")
            self.remove_book_info.config(text="", fg="gray")
            self.entry_remove_search.delete(0, tk.END)
            self.current_remove_isbn = None
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to remove book: {e}")


    def setup_modify_book_tab(self):
        tk.Label(self.tab_modify_book, text="Search by ISBN:").grid(row=0, column=0, padx=10, pady=10)
    
        self.entry_modify_search = tk.Entry(self.tab_modify_book, width=25)
        self.entry_modify_search.grid(row=0, column=1, padx=5)

        tk.Button(
        self.tab_modify_book,
        text="Load Book",
        command=self.load_book_for_modify
        ).grid(row=0, column=2, padx=5)

        self.modify_book_info = tk.Label(self.tab_modify_book, text="", fg="gray")
        self.modify_book_info.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(self.tab_modify_book, text="New Title:").grid(row=2, column=0)
        self.entry_mod_title = tk.Entry(self.tab_modify_book)
        self.entry_mod_title.grid(row=2, column=1)

        tk.Label(self.tab_modify_book, text="New Author:").grid(row=3, column=0)
        self.entry_mod_author = tk.Entry(self.tab_modify_book)
        self.entry_mod_author.grid(row=3, column=1)

        tk.Label(self.tab_modify_book, text="New Genre:").grid(row=4, column=0)
        self.entry_mod_genre = tk.Entry(self.tab_modify_book)
        self.entry_mod_genre.grid(row=4, column=1)

        tk.Label(self.tab_modify_book, text="New Category:").grid(row=5, column=0)
        self.entry_mod_category = tk.Entry(self.tab_modify_book) 
        self.entry_mod_category.grid(row=5, column=1)


        tk.Button(
        self.tab_modify_book,
        text="Update Book",
        command=self.modify_book
        ).grid(row=6, column=1, pady=10)

        self.current_modify_isbn = None


    def load_book_for_modify(self):
        search_term = self.entry_modify_search.get().strip()

        if not search_term:
            messagebox.showwarning("Input Error", "Please enter an ISBN.")
            return

        try:
            book = Book.find_by_title_or_isbn(search_term)

            if book:
                self.current_modify_isbn = book["isbn"]
                self.modify_book_info.config(
                    text=f"Editing: {book['title']} by {book['author']}",
                    fg="black"
                )
            else:
                self.current_modify_isbn = None
                self.modify_book_info.config(text="Book not found", fg="red")

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

        

    def modify_book(self):
        if not self.current_modify_isbn:
            messagebox.showwarning("No Book Selected", "Please load a book first.")
            return

        title = self.entry_mod_title.get().strip()
        author = self.entry_mod_author.get().strip()
        genre = self.entry_mod_genre.get().strip()
        category = self.entry_mod_category.get().strip() 

        try:
            Book.modify(
               self.current_modify_isbn,
                title if title else None,
                author if author else None,
                genre if genre else None,
                category if category else None, 

             )

            messagebox.showinfo("Success", "Book updated successfully!")

            self.modify_book_info.config(text="")
            self.entry_modify_search.delete(0, tk.END)
            self.entry_mod_title.delete(0, tk.END)
            self.entry_mod_author.delete(0, tk.END)
            self.entry_mod_genre.delete(0, tk.END)
            self.entry_mod_category.delete(0, tk.END) 

            
            self.current_modify_isbn = None

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update book: {e}")

    def setup_renew_tab(self):
        tk.Label(self.tab_renew, text="Book ISBN:").grid(row=0, column=0, padx=10, pady=10)

        self.entry_renew_isbn = tk.Entry(self.tab_renew)
        self.entry_renew_isbn.grid(row=0, column=1)

        tk.Label(self.tab_renew, text="Extra Days (optional):").grid(row=1, column=0, padx=10, pady=10)

        self.entry_renew_days = tk.Entry(self.tab_renew)
        self.entry_renew_days.insert(0, "7")  # default renew period
        self.entry_renew_days.grid(row=1, column=1)

        tk.Button(
        self.tab_renew,
        text="Renew Book",
        command=self.process_renew
        ).grid(row=2, column=1, pady=20)


    def process_renew(self):
        isbn = self.entry_renew_isbn.get().strip()
        days = self.entry_renew_days.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            extra_days = int(days) if days else 7

            new_due = Checkout.renew(self.current_student_id, isbn, extra_days)

            messagebox.showinfo(
                "Success",
                f"Book renewed successfully!\nNew due date: {new_due}"
            )

            self.entry_renew_isbn.delete(0, tk.END)

        except ValueError as e:
            messagebox.showwarning("Renew Failed", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        app = LoginSignupGUI(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupGUI(root)
    root.mainloop()
