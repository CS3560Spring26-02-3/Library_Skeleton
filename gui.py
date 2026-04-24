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

        self.add_login_background(self.tab_login)
        self.add_login_background(self.tab_signup)

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

    def add_login_background(self, parent):
        image = Image.open(r"C:\Users\Abel\Downloads\book-library-with-open-textbook (1).jpg")
        image = image.resize((400, 300))
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(parent, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        return bg_label

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

        # ===== BACKGROUND IMAGE START =====
        # image = Image.open(r"C:\Users\Abel\Downloads\book-library-with-open-textbook.jpg")
        # image = image.resize((500, 400))
        # self.bg_image = ImageTk.PhotoImage(image)
        #
        # bg_label = tk.Label(self.root, image=self.bg_image)
        # bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # ===== BACKGROUND IMAGE END =====

        # Create tabs for different Use Cases
        tab_control = ttk.Notebook(root)
        self.tab_add_book = ttk.Frame(tab_control)
        self.tab_checkout = ttk.Frame(tab_control)

        tab_control.add(self.tab_add_book, text='Add New Book (Staff)')
        tab_control.add(self.tab_checkout, text='Checkout Book (Student)')
        tab_control.pack(expand=1, fill="both")

        # tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

        # tk.Button(self.root, text="Logout", command=self.logout, bg="#cc0000", fg="white").place(relx=0.95, rely=0.02, anchor="ne")

        tk.Button(self.root, text="Logout", command=self.logout, bg="#cc0000", fg="white").place(relx=0.5, rely=0.95, anchor="center")

        self.add_background(self.tab_add_book)
        self.add_background(self.tab_checkout)

        self.setup_add_book_tab()
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

    # def setup_checkout_tab(self):
    #     # UI Elements for Checking out a Book
    #     tk.Label(self.tab_checkout, text="Student ID:").grid(row=0, column=0, pady=10, padx=10)
    #     self.entry_student_id = tk.Entry(self.tab_checkout)
    #     self.entry_student_id.grid(row=0, column=1)
    #
    #     tk.Label(self.tab_checkout, text="Copy ID:").grid(row=1, column=0, pady=10, padx=10)
    #     self.entry_copy_id = tk.Entry(self.tab_checkout)
    #     self.entry_copy_id.grid(row=1, column=1)
    #
    #     tk.Button(self.tab_checkout, text="Process Checkout", command=self.process_checkout).grid(row=2, column=1, pady=20)

    def setup_checkout_tab(self):
        tk.Label(self.tab_checkout, text="Copy ID:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_copy_id = tk.Entry(self.tab_checkout)
        self.entry_copy_id.grid(row=0, column=1)

        tk.Button(self.tab_checkout, text="Process Checkout", command=self.process_checkout).grid(row=1, column=1,
                                                                                                  pady=20)
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

    # def process_checkout(self):
    #     student_id = self.entry_student_id.get()
    #     copy_id = self.entry_copy_id.get()
    #
    #     if student_id and copy_id:
    #         conn = create_connection()
    #         if conn:
    #             try:
    #                 cursor = conn.cursor()
    #                 # Maps to Checkouts table in schema.sql
    #                 query = "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)"
    #                 values = (student_id, copy_id, datetime.date.today())
    #                 cursor.execute(query, values)
    #                 conn.commit()
    #                 messagebox.showinfo("Success", "Checkout processed successfully!")
    #             except Exception as e:
    #                 messagebox.showerror("Database Error", f"Failed to checkout: {e}")
    #             finally:
    #                 cursor.close()
    #                 conn.close()
    #     else:
    #          messagebox.showwarning("Input Error", "Both Student ID and Copy ID are required.")

    def add_background(self, parent):
        image = Image.open(r"C:\Users\Abel\Downloads\book-library-with-open-textbook.jpg")
        image = image.resize((500, 400))
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(parent, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        return bg_label

    def process_checkout(self):
        copy_id = self.entry_copy_id.get().strip()

        if not self.current_student_id:
            messagebox.showwarning("Login Required", "No student is logged in.")
            return

        if copy_id:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    query = "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)"
                    values = (self.current_student_id, copy_id, datetime.date.today())
                    cursor.execute(query, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Checkout processed successfully!")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to checkout: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "Copy ID is required.")
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LibraryGUI(root)
#     root.mainloop()

    def logout(self):
        self.root.destroy()

        login_root = tk.Tk()
        app = LoginSignupGUI(login_root)
        login_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupGUI(root)
    root.mainloop()