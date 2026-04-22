import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Importing your existing database connection and method
from entities.main import add_new_book, create_connection

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("500x400")

        # Create tabs for different Use Cases
        tab_control = ttk.Notebook(root)
        self.tab_add_book = ttk.Frame(tab_control)
        self.tab_checkout = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_add_book, text='Add New Book (Staff)')
        tab_control.add(self.tab_checkout, text='Checkout Book (Student)')
        tab_control.pack(expand=1, fill="both")

        self.setup_add_book_tab()
        self.setup_checkout_tab()

    def setup_add_book_tab(self):
        # UI Elements for Adding a Book
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

    def setup_checkout_tab(self):
        # UI Elements for Checking out a Book
        tk.Label(self.tab_checkout, text="Student ID:").grid(row=0, column=0, pady=10, padx=10)
        self.entry_student_id = tk.Entry(self.tab_checkout)
        self.entry_student_id.grid(row=0, column=1)

        tk.Label(self.tab_checkout, text="Copy ID:").grid(row=1, column=0, pady=10, padx=10)
        self.entry_copy_id = tk.Entry(self.tab_checkout)
        self.entry_copy_id.grid(row=1, column=1)

        tk.Button(self.tab_checkout, text="Process Checkout", command=self.process_checkout).grid(row=2, column=1, pady=20)

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
        student_id = self.entry_student_id.get()
        copy_id = self.entry_copy_id.get()

        if student_id and copy_id:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Maps to Checkouts table in schema.sql
                    query = "INSERT INTO Checkouts (student_id, copy_id, checkout_date) VALUES (%s, %s, %s)"
                    values = (student_id, copy_id, datetime.date.today())
                    cursor.execute(query, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Checkout processed successfully!")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Failed to checkout: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
             messagebox.showwarning("Input Error", "Both Student ID and Copy ID are required.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()