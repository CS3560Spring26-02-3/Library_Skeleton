import tkinter as tk
from tkinter import ttk, messagebox

from entities.book import Book
from entities.book_copies import BookCopies
from entities.book_return import BookReturn
from entities.checkout import Checkout
from entities.staff import Staff
from entities.student import Student

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
        tab_control.add(self.tab_checkout, text='Checkout')
        tab_control.add(self.tab_return, text='Return Book')

        # Staff only
        if current_role == 'staff':
            self.tab_add_book = ttk.Frame(tab_control)
            self.tab_add_copy = ttk.Frame(tab_control)
            self.tab_remove_book = ttk.Frame(tab_control)
            tab_control.add(self.tab_add_book, text='Add Book (Staff)')
            tab_control.add(self.tab_add_copy, text='Add Copy (Staff)')
            tab_control.add(self.tab_remove_book, text='Remove Book (Staff)')
            self.setup_add_book_tab()
            self.setup_add_copy_tab()
            self.setup_remove_book_tab()

        tab_control.pack(expand=1, fill="both")

        tk.Button(self.root, text="Logout", command=self.logout,
                  bg="#cc0000", fg="white").place(relx=0.5, rely=0.95, anchor="center")

        self.setup_search_tab()
        self.setup_checkout_tab()
        self.setup_return_tab()

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
            messagebox.showinfo("Success", f"Checkout successful!\n\nYou have checked out Copy ID: {copy_id}")
            self.entry_checkout_isbn.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Checkout Failed", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to checkout: {e}")

    def process_return(self):
        isbn = self.entry_return_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        try:
            BookReturn.process(self.current_student_id, isbn)
            messagebox.showinfo("Success", "Book returned successfully! Thank you.")
            self.entry_return_isbn.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Return Failed", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to return book: {e}")

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

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        app = LoginSignupGUI(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupGUI(root)
    root.mainloop()
