📚 Library Management System
A user-friendly Library Management System built using Python and Tkinter. This application allows library administrators to manage books, members, and book loans with ease. It integrates with a MySQL database to store and retrieve data efficiently.

🚀 Features
1/. Add Books: Add new books to the library's collection with details like title, author, genre, and the number of available copies.
2/. View Books: Display a list of all available books in a user-friendly table format.
3/. Add Members: Add new library members with their name, email, and phone number.
4/. Loan Books: Allow members to borrow books, track loans, and manage available copies dynamically.
5/. Search Members: Search for library members by name or email.

🛠️ Technologies Used
. Programming Language: Python
. GUI Framework: Tkinter
. Database: MySQL (using pymysql library for database connectivity)

📋 Prerequisites
Before running this project, ensure you have the following installed:
1. Python 3.8 or above
2. MySQL Server
3. Python packages:
- pymysql
- tkinter (built into Python)

  ⚙️ Setup Instructions
1. Clone the Repository:
   
git clone https://github.com/HarryVuthy/My-final-project.git

cd library-management-system

2. Set Up the MySQL Database:
- Create a database called LibrarySystem in MySQL

CREATE DATABASE LibrarySystem;

CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(50),
    available_copies INT NOT NULL
);

CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL
);

CREATE TABLE Loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    loan_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);

3. Install Required Python Libraries:

  pip install mysql

4.Update Database Credentials: Open the finalproject.py file and update the connect_db function with your MySQL credentials:
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="your-mysql-username",
        password="your-mysql-password",
        database="LibrarySystem"
    )
5. Run the application:
python finalproject.py




