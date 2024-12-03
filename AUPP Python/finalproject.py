import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import date

# Database connection
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",  # Update with your MySQL username
        password="Cybery77",  # Update with your MySQL password
        database="LibrarySystem"
    )

# Main Application Class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f8f9fa")  # Light background

        # Create UI elements
        self.create_ui()

    def create_ui(self):
        # Title
        title = tk.Label(
            self.root, text="📚 Library Management System", 
            font=("Arial", 24, "bold"), bg="#343a40", fg="white", padx=20, pady=10
        )
        title.pack(fill="x")

        # Tabs
        tab_control = ttk.Notebook(self.root)
        self.add_book_tab = ttk.Frame(tab_control)
        self.view_books_tab = ttk.Frame(tab_control)
        self.loan_book_tab = ttk.Frame(tab_control)
        self.add_member_tab = ttk.Frame(tab_control)  # New tab for adding members
        
        tab_control.add(self.add_book_tab, text="📖 Add Book")
        tab_control.add(self.view_books_tab, text="📚 View Books")
        tab_control.add(self.loan_book_tab, text="🔄 Loan Book")
        tab_control.add(self.add_member_tab, text="👥 Add Member")  # Add new member tab
        
        tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Create UI elements
        self.add_book_ui()
        self.view_books_ui()
        self.loan_book_ui()
        
        # New method to create Add Member UI
        self.add_member_ui()

    def add_book_ui(self):
        # Add Book UI
        tk.Label(
            self.add_book_tab, text="Add New Book", 
            font=("Arial", 20, "bold"), fg="#343a40"
        ).pack(pady=20)

        # Input fields with labels
        frame = tk.Frame(self.add_book_tab, bg="#f8f9fa")
        frame.pack(pady=10, padx=10)

        inputs = [
            ("Title", "title_entry"),
            ("Author", "author_entry"),
            ("Genre", "genre_entry"),
            ("Available Copies", "copies_entry")
        ]
        for idx, (label, var_name) in enumerate(inputs):
            tk.Label(frame, text=f"{label}:", font=("Arial", 12), bg="#f8f9fa").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            setattr(self, var_name, tk.Entry(frame, width=30, font=("Arial", 12)))
            getattr(self, var_name).grid(row=idx, column=1, padx=10, pady=5)

        # Add Book Button
        tk.Button(
            self.add_book_tab, text="Add Book", 
            command=self.add_book, font=("Arial", 14), 
            bg="#28a745", fg="white", relief="raised", cursor="hand2"
        ).pack(pady=20)

    def add_book(self):
        # Retrieve data from input fields
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        copies = self.copies_entry.get()

        if not title or not author or not genre or not copies:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            copies = int(copies)
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Books (title, author, genre, available_copies) VALUES (%s, %s, %s, %s)", 
                (title, author, genre, copies)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_add_book_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add book: {e}")

    def clear_add_book_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.copies_entry.delete(0, tk.END)

    def view_books_ui(self):
        # View Books UI
        tk.Label(
            self.view_books_tab, text="Available Books", 
            font=("Arial", 20, "bold"), fg="#343a40"
        ).pack(pady=20)

        # Treeview to display books
        columns = ("ID", "Title", "Author", "Genre", "Copies")
        self.book_table = ttk.Treeview(
            self.view_books_tab, columns=columns, show="headings", height=15
        )
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=120)

        self.book_table.pack(fill="both", expand=True, padx=20, pady=10)

        # Refresh Button
        tk.Button(
            self.view_books_tab, text="Refresh", 
            command=self.view_books, font=("Arial", 14), 
            bg="#007bff", fg="white", relief="raised", cursor="hand2"
        ).pack(pady=20)

    def view_books(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Books")
            books = cursor.fetchall()
            db.close()

            # Clear existing data in the table
            for row in self.book_table.get_children():
                self.book_table.delete(row)

            # Insert new data
            for book in books:
                self.book_table.insert("", tk.END, values=book)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve books: {e}")

    def loan_book_ui(self):
        # Loan Book UI
        tk.Label(
            self.loan_book_tab, text="Loan a Book", 
            font=("Arial", 20, "bold"), fg="#343a40"
        ).pack(pady=20)

        # Member Search
        frame = tk.Frame(self.loan_book_tab, bg="#f8f9fa")
        frame.pack(pady=10)

        tk.Label(
            frame, text="Search Member (Name or Email):", 
            font=("Arial", 12), bg="#f8f9fa"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.search_member_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.search_member_entry.grid(row=0, column=1, padx=10, pady=5)

        search_btn = tk.Button(
            frame, text="Search", command=self.search_member, 
            font=("Arial", 12), bg="#17a2b8", fg="white", relief="raised", cursor="hand2"
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)

        # Member Info Display
        self.member_info_label = tk.Label(
            self.loan_book_tab, text="Member Info: ", 
            font=("Arial", 14), bg="#f8f9fa"
        )
        self.member_info_label.pack(pady=10)

        # Book Dropdown with Refresh Button
        tk.Label(
            self.loan_book_tab, text="Select Book:", 
            font=("Arial", 12), bg="#f8f9fa"
        ).pack(pady=10)

        book_dropdown_frame = tk.Frame(self.loan_book_tab, bg="#f8f9fa")
        book_dropdown_frame.pack(pady=5)

        self.book_dropdown = ttk.Combobox(book_dropdown_frame, state="readonly", width=40)
        self.book_dropdown.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            book_dropdown_frame, text="🔄 Refresh Books", 
            command=self.populate_books_dropdown, font=("Arial", 12), 
            bg="#007bff", fg="white", relief="raised", cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Loan Button
        tk.Button(
            self.loan_book_tab, text="Loan Book", command=self.loan_book, 
            font=("Arial", 14), bg="#28a745", fg="white", relief="raised", cursor="hand2"
        ).pack(pady=20)

    def search_member(self):
        search_term = self.search_member_entry.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a name or email to search!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT member_id, name, email FROM Members WHERE name LIKE %s OR email LIKE %s", 
                (f"%{search_term}%", f"%{search_term}%")
            )
            result = cursor.fetchone()
            db.close()

            if result:
                self.member_id = result[0]
                self.member_info_label.config(
                    text=f"Member Info: {result[1]} ({result[2]})"  # Display member name and email
                )
                self.populate_books_dropdown()  # Refresh books when a member is found
            else:
                self.member_info_label.config(text="Member Info: No matching member found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not search for member: {e}")

    def populate_books_dropdown(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT book_id, title FROM Books WHERE available_copies > 0")
            books = cursor.fetchall()
            db.close()

            self.book_dropdown["values"] = [f"{book[0]} - {book[1]}" for book in books]
            if books:
                self.book_dropdown.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve books: {e}")

    def loan_book(self):
        if not hasattr(self, "member_id"):
            messagebox.showerror("Error", "Please search for a member first!")
            return

        selected_book = self.book_dropdown.get()
        if not selected_book:
            messagebox.showerror("Error", "Please select a book to loan!")
            return

        try:
            book_id = selected_book.split(" - ")[0]
            loan_date = date.today()

            db = connect_db()
            cursor = db.cursor()

            # Insert into Loans table
            cursor.execute(
                "INSERT INTO Loans (member_id, book_id, loan_date) VALUES (%s, %s, %s)", 
                (self.member_id, book_id, loan_date)
            )

            # Decrement available copies of the book
            cursor.execute(
                "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = %s", 
                (book_id,)
            )

            db.commit()
            db.close()

            messagebox.showinfo("Success", "Book loaned successfully!")
            self.populate_books_dropdown()  # Refresh books dropdown
        except Exception as e:
            messagebox.showerror("Error", f"Could not loan book: {e}")

    def add_member_ui(self):
        # Add Member UI
        tk.Label(
            self.add_member_tab, text="Add New Member", 
            font=("Arial", 20, "bold"), fg="#343a40"
        ).pack(pady=20)

        # Input fields with labels
        frame = tk.Frame(self.add_member_tab, bg="#f8f9fa")
        frame.pack(pady=10, padx=10)

        # Member input fields
        inputs = [
            ("Name", "member_name_entry"),
            ("Email", "member_email_entry"),
            ("Phone", "member_phone_entry"),
            ("Address", "member_address_entry")
        ]
        for idx, (label, var_name) in enumerate(inputs):
            tk.Label(frame, text=f"{label}:", font=("Arial", 12), bg="#f8f9fa").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            setattr(self, var_name, tk.Entry(frame, width=30, font=("Arial", 12)))
            getattr(self, var_name).grid(row=idx, column=1, padx=10, pady=5)

        # Add Member Button
        tk.Button(
            self.add_member_tab, text="Add Member", 
            command=self.add_member, font=("Arial", 14), 
            bg="#28a745", fg="white", relief="raised", cursor="hand2"
        ).pack(pady=20)

    def add_member(self):
        # Retrieve data from input fields
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        phone = self.member_phone_entry.get()
        address = self.member_address_entry.get()

        # Validate input
        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Members (name, email, phone_number, address) VALUES (%s, %s, %s, %s)", 
                (name, email, phone, address)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Member added successfully!")
            self.clear_add_member_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add member: {e}")

    def clear_add_member_fields(self):
        # Clear all member input fields
        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)
        self.member_address_entry.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()