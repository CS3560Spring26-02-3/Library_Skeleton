import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import cv2
from entities.main import add_new_book, create_connection

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

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO Students (name, email, pin) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, pin))
                conn.commit()
                messagebox.showinfo("Success", "Account created successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Sign up failed: {e}")
            finally:
                cursor.close()
                conn.close()

    def login_student(self):
        email = self.entry_login_email.get().strip()
        pin = self.entry_login_pin.get().strip()

        if not email or not pin:
            messagebox.showwarning("Input Error", "Email and PIN are required.")
            return

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT student_id, name FROM Students WHERE email = %s AND pin = %s"
                cursor.execute(query, (email, pin))
                student = cursor.fetchone()

                if student:
                    messagebox.showinfo("Success", f"Welcome, {student[1]}!")
                    self.root.destroy()
                    main_root = tk.Tk()
                    app = LibraryGUI(main_root, current_student_id=student[0], current_student_name=student[1], current_role='student')
                    main_root.mainloop()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or PIN.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Login failed: {e}")
            finally:
                cursor.close()
                conn.close()

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

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT staff_id, name FROM Staff WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                staff = cursor.fetchone()

                if staff:
                    messagebox.showinfo("Success", f"Welcome, {staff[1]}!")
                    self.root.destroy()
                    main_root = tk.Tk()
                    app = LibraryGUI(main_root, current_role='staff', current_student_name=staff[1])
                    main_root.mainloop()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Login failed: {e}")
            finally:
                cursor.close()
                conn.close()


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
        self.search_type.current(0)  # Default to Title
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

    def search_books(self):
        search_term = self.entry_search.get().strip()
        search_by = self.search_type.get()

        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
        return

        # Map dropdown choice to actual DB column
        column_map = {
            "Title": "b.title",
            "Author": "b.author",
            "ISBN": "b.isbn",
            "Genre": "b.genre"
        }
        column = column_map[search_by]

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"""
                    SELECT b.isbn, b.title, b.author, b.genre, b.category,
                        COUNT(bc.copy_id) as total_copies,
                        SUM(CASE WHEN bc.status = 'Available' THEN 1 ELSE 0 END) as available
                    FROM Books b
                    LEFT JOIN BookCopies bc ON b.isbn = bc.isbn
                    WHERE {column} LIKE %s
                    GROUP BY b.isbn, b.title, b.author, b.genre, b.category
                """
                cursor.execute(query, (f"%{search_term}%",))
                results = cursor.fetchall()

                self.search_results.delete(0, tk.END)
                if results:
                    for r in results:
                        available = r[6] if r[6] else 0
                        self.search_results.insert(tk.END,
                            f"{r[1]} | by {r[2]} | ISBN: {r[0]} | Genre: {r[3]} | Available: {available}/{r[5]}")
                else:
                    self.search_results.insert(tk.END, "No books found.")
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {e}")
            finally:
                cursor.close()
                conn.close()

    def submit_new_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        isbn = self.entry_isbn.get()
        genre = self.entry_genre.get()
        category = self.entry_category.get()

        if title and author and isbn:
            add_new_book(title, author, isbn, genre, category)
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        else:
            messagebox.showwarning("Input Error", "Title, Author, and ISBN are required.")

    def submit_new_copy(self):
        isbn = self.entry_copy_isbn.get().strip()
        location = self.entry_copy_location.get().strip()

        if isbn and location:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    query = "INSERT INTO BookCopies (isbn, location, status) VALUES (%s, %s, %s)"
                    cursor.execute(query, (isbn, location, "Available"))
                    conn.commit()
                    new_copy_id = cursor.lastrowid
                    messagebox.showinfo("Success", f"Copy added successfully!\n\nThe new Copy ID is: {new_copy_id}")
                    self.entry_copy_isbn.delete(0, tk.END)
                    self.entry_copy_location.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to add copy: {e}")
                finally:
                    cursor.close()
                    conn.close()
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

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                check_existing_query = """
                    SELECT c.checkout_id FROM Checkouts c
                    JOIN BookCopies bc ON c.copy_id = bc.copy_id
                    WHERE c.student_id = %s AND bc.isbn = %s
                """
                cursor.execute(check_existing_query, (self.current_student_id, isbn))
                if cursor.fetchone():
                    messagebox.showwarning("Limit Reached", "You already have a copy of this book checked out!")
                    return

                find_copy_query = "SELECT copy_id FROM BookCopies WHERE isbn = %s AND status = 'Available' LIMIT 1"
                cursor.execute(find_copy_query, (isbn,))
                available_copy = cursor.fetchone()

                if available_copy:
                    copy_id = available_copy[0]
                    cursor.execute("INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)",
                                   (self.current_student_id, copy_id, datetime.date.today()))
                    cursor.execute("UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s", (copy_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Checkout successful!\n\nYou have checked out Copy ID: {copy_id}")
                    self.entry_checkout_isbn.delete(0, tk.END)
                else:
                    messagebox.showwarning("Unavailable", "Sorry, no copies of this book are currently available.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Database Error", f"Failed to checkout: {e}")
            finally:
                cursor.close()
                conn.close()

    def process_return(self):
        isbn = self.entry_return_isbn.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if not isbn:
            messagebox.showwarning("Input Error", "ISBN is required.")
            return

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                find_checkout_query = """
                    SELECT c.checkout_id, c.copy_id FROM Checkouts c
                    JOIN BookCopies bc ON c.copy_id = bc.copy_id
                    WHERE c.student_id = %s AND bc.isbn = %s
                """
                cursor.execute(find_checkout_query, (self.current_student_id, isbn))
                checkout_record = cursor.fetchone()

                if checkout_record:
                    cursor.execute("DELETE FROM Checkouts WHERE checkout_id = %s", (checkout_record[0],))
                    cursor.execute("UPDATE BookCopies SET status = 'Available' WHERE copy_id = %s", (checkout_record[1],))
                    conn.commit()
                    messagebox.showinfo("Success", "Book returned successfully! Thank you.")
                    self.entry_return_isbn.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "You don't currently have a copy of this book checked out.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Database Error", f"Failed to return book: {e}")
            finally:
                cursor.close()
                conn.close()

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

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT isbn, title, author, genre FROM Books WHERE isbn = %s OR title LIKE %s"
                cursor.execute(query, (search_term, f"%{search_term}%"))
                book = cursor.fetchone()

                if book:
                    self.current_remove_isbn = book[0]
                    self.remove_book_info.config(
                        text=f"Found: '{book[1]}' by {book[2]} | Genre: {book[3]}\nISBN: {book[0]}",
                        fg="black"
                    )
                else:
                    self.current_remove_isbn = None
                    self.remove_book_info.config(text="No book found.", fg="red")
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {e}")
            finally:
                cursor.close()
                conn.close()

    def remove_book(self):
        if not self.current_remove_isbn:
            messagebox.showwarning("No Book Selected", "Please search for a book first.")
            return

        confirm = messagebox.askyesno("Confirm Remove",
            f"Are you sure you want to remove this book?\nISBN: {self.current_remove_isbn}\n\nThis will also remove all copies!")

        if not confirm:
            return

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Books WHERE isbn = %s", (self.current_remove_isbn,))
                conn.commit()
                messagebox.showinfo("Success", "Book and all its copies have been removed.")
                self.remove_book_info.config(text="", fg="gray")
                self.entry_remove_search.delete(0, tk.END)
                self.current_remove_isbn = None
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Database Error", f"Failed to remove book: {e}")
            finally:
                cursor.close()
                conn.close()

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        app = LoginSignupGUI(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupGUI(root)
    root.mainloop()