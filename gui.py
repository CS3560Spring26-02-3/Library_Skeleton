import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import cv2
# Importing your existing database connection and method
from entities.main import add_new_book, create_connection

class LoginSignupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Login")
        self.root.geometry("400x300")

        # image = Image.open(r"C:\Users\Abel\Downloads\book-library-with-open-textbook (1).jpg")
        # image = image.resize((400, 300))
        # self.login_bg_image = ImageTk.PhotoImage(image)
        #
        # bg_label = tk.Label(self.root, image=self.login_bg_image)
        # bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tab_control = ttk.Notebook(root)

        self.tab_login = ttk.Frame(tab_control)
        self.tab_signup = ttk.Frame(tab_control)

        tab_control.add(self.tab_login, text="Login")
        tab_control.add(self.tab_signup, text="Sign Up")
        tab_control.pack(expand=1, fill="both")

        self.setup_login_tab()
        self.setup_signup_tab()



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
                    app = LibraryGUI(main_root, current_student_id=student[0], current_student_name=student[1])
                    main_root.mainloop()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or PIN.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Login failed: {e}")
            finally:
                cursor.close()
                conn.close()

class LibraryGUI:
    def __init__(self, root, current_student_id=None, current_student_name=None):
        self.root = root
        self.current_student_id = current_student_id
        self.current_student_name = current_student_name

        self.root.title("Library Management System")
        self.root.geometry("500x400")

        # Create tabs for different Use Cases
        tab_control = ttk.Notebook(root)
        self.tab_add_book = ttk.Frame(tab_control)
        self.tab_add_copy = ttk.Frame(tab_control)
        self.tab_checkout = ttk.Frame(tab_control)

        tab_control.add(self.tab_add_book, text='Add New Book (Staff)')
        tab_control.add(self.tab_add_copy, text='Add Book Copy (Staff)')
        tab_control.add(self.tab_checkout, text='Checkout Book (Student)')
        tab_control.pack(expand=1, fill="both")

        tk.Button(self.root, text="Logout", command=self.logout, bg="#cc0000", fg="white").place(relx=0.5, rely=0.95, anchor="center")

        self.setup_add_book_tab()
        self.setup_add_copy_tab()
        self.setup_checkout_tab()

    def setup_add_book_tab(self):
        # UI Elements for Adding a Book
        # tk.Label(self.tab_add_book, text="Title:").grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self.tab_add_book, text="Title:", bg="white").grid(row=0, column=0, pady=10, padx=10)
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

    def setup_checkout_tab(self):
        # Changed "Copy ID" to "ISBN"
        tk.Label(self.tab_checkout, text="Book ISBN:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_checkout_isbn = tk.Entry(self.tab_checkout) 
        self.entry_checkout_isbn.grid(row=0, column=1)

        tk.Button(self.tab_checkout, text="Process Checkout", command=self.process_checkout).grid(row=1, column=1, pady=20)

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

    def process_checkout(self):
        # Get the ISBN from the new entry box
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
                
                # STEP 1: Find ONE available copy of this specific book
                find_copy_query = "SELECT copy_id FROM BookCopies WHERE isbn = %s AND status = 'Available' LIMIT 1"
                cursor.execute(find_copy_query, (isbn,))
                available_copy = cursor.fetchone()

                # If a copy was found...
                if available_copy:
                    copy_id = available_copy[0] # Extract the ID from the tuple
                    
                    # STEP 2: Create the checkout record
                    checkout_query = "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)"
                    cursor.execute(checkout_query, (self.current_student_id, copy_id, datetime.date.today()))
                    
                    # STEP 3: Mark the physical copy as 'Checked Out' so it can't be taken again
                    update_status_query = "UPDATE BookCopies SET status = 'Checked Out' WHERE copy_id = %s"
                    cursor.execute(update_status_query, (copy_id,))
                    
                    # Commit both changes to the database at the same time
                    conn.commit()
                    
                    messagebox.showinfo("Success", f"Checkout successful!\n\nYou have checked out Copy ID: {copy_id}")
                    self.entry_checkout_isbn.delete(0, tk.END) # Clear the box
                    
                # If no copy was found (either doesn't exist, or all are checked out)...
                else:
                    messagebox.showwarning("Unavailable", "Sorry, no copies of this book are currently available.")

            except Exception as e:
                conn.rollback() # Cancels the transaction if something breaks halfway through
                messagebox.showerror("Database Error", f"Failed to checkout: {e}")
            finally:
                cursor.close()
                conn.close()

    def logout(self):
        self.root.destroy()

        login_root = tk.Tk()
        app = LoginSignupGUI(login_root)
        login_root.mainloop()

    def setup_add_copy_tab(self):
        # UI Elements for Adding a Physical Copy
        tk.Label(self.tab_add_copy, text="ISBN (Must match an existing book):").grid(row=0, column=0, pady=10, padx=10)
        self.entry_copy_isbn = tk.Entry(self.tab_add_copy)
        self.entry_copy_isbn.grid(row=0, column=1)

        tk.Label(self.tab_add_copy, text="Location (e.g., Shelf 3A):").grid(row=1, column=0, pady=10, padx=10)
        self.entry_copy_location = tk.Entry(self.tab_add_copy)
        self.entry_copy_location.grid(row=1, column=1)

        tk.Button(self.tab_add_copy, text="Add Physical Copy", command=self.submit_new_copy).grid(row=2, column=1, pady=20)

    def submit_new_copy(self):
        isbn = self.entry_copy_isbn.get().strip()
        location = self.entry_copy_location.get().strip()

        if isbn and location:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Status is 'Available' by default based on your schema
                    query = "INSERT INTO BookCopies (isbn, location, status) VALUES (%s, %s, %s)"
                    values = (isbn, location, "Available")
                    
                    cursor.execute(query, values)
                    conn.commit()
                    
                    # Fetch the auto-incremented ID to show the user
                    new_copy_id = cursor.lastrowid 
                    messagebox.showinfo("Success", f"Copy added successfully!\n\nThe new Copy ID is: {new_copy_id}")
                    
                    # Clear the input fields after successful entry
                    self.entry_copy_isbn.delete(0, tk.END)
                    self.entry_copy_location.delete(0, tk.END)
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to add copy: {e}\n(Make sure the ISBN exists in the Books tab first!)")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "Both ISBN and Location are required.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupGUI(root)
    root.mainloop()