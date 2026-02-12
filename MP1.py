#-------------------- LIBRARY MANAGEMENT-----------------------
import sqlite3
from datetime import datetime

# ================== DATABASE CONNECTION ==================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# ================== TABLE CREATION ==================

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    return_status TEXT DEFAULT 'Not Returned',
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (book_id) REFERENCES admin(admin_id)
)
""")

conn.commit()

# ================== ADMIN FUNCTIONS (3) ==================

def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    quantity = int(input("Enter Quantity: "))

    cursor.execute(
        "INSERT INTO admin (book_title, author, quantity) VALUES (?, ?, ?)",
        (title, author, quantity)
    )
    conn.commit()
    print("Book Added Successfully!\n")


def update_book():
    book_id = int(input("Enter Book ID to Update: "))
    quantity = int(input("Enter New Quantity: "))

    cursor.execute(
        "UPDATE admin SET quantity=? WHERE admin_id=?",
        (quantity, book_id)
    )
    conn.commit()
    print("Book Updated Successfully!\n")


def delete_book():
    book_id = int(input("Enter Book ID to Delete: "))

    cursor.execute("DELETE FROM admin WHERE admin_id=?", (book_id,))
    conn.commit()
    print("Book Deleted Successfully!\n")


# ================== USER FUNCTIONS (3) ==================

def register_user():
    name = input("Enter Name: ")
    email = input("Enter Email: ")

    try:
        cursor.execute(
            "INSERT INTO user (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        print("User Registered Successfully!\n")
    except:
        print("Email already exists!\n")


def search_book():
    keyword = input("Enter Book Title to Search: ")

    cursor.execute("""
        SELECT * FROM admin
        WHERE book_title LIKE ?
    """, ('%' + keyword + '%',))

    books = cursor.fetchall()

    if books:
        print("\nSearch Results:")
        for book in books:
            print(book)
    else:
        print("No Book Found!")
    print()


def view_profile():
    user_id = int(input("Enter Your User ID: "))

    cursor.execute("SELECT * FROM user WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        print("User Details:", user)
    else:
        print("User Not Found!")
    print()


# ================== ISSUED BOOK FUNCTIONS (3) ==================

def issue_book():
    user_id = int(input("Enter User ID: "))
    book_id = int(input("Enter Book ID: "))

    cursor.execute("SELECT quantity FROM admin WHERE admin_id=?", (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        issue_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO issued_books (user_id, book_id, issue_date)
            VALUES (?, ?, ?)
        """, (user_id, book_id, issue_date))

        cursor.execute("""
            UPDATE admin SET quantity = quantity - 1
            WHERE admin_id=?
        """, (book_id,))

        conn.commit()
        print("Book Issued Successfully!\n")
    else:
        print("Book Not Available!\n")


def view_issued_books():
    cursor.execute("SELECT * FROM issued_books")
    records = cursor.fetchall()

    print("\nIssued Books:")
    for record in records:
        print(record)
    print()


def return_book():
    issue_id = int(input("Enter Issue ID to Return: "))

    cursor.execute("""
        SELECT book_id FROM issued_books
        WHERE issue_id=? AND return_status='Not Returned'
    """, (issue_id,))
    result = cursor.fetchone()

    if result:
        book_id = result[0]

        cursor.execute("""
            UPDATE issued_books
            SET return_status='Returned'
            WHERE issue_id=?
        """, (issue_id,))

        cursor.execute("""
            UPDATE admin
            SET quantity = quantity + 1
            WHERE admin_id=?
        """, (book_id,))

        conn.commit()
        print("Book Returned Successfully!\n")
    else:
        print("Invalid Issue ID or Already Returned!\n")


# ================== MAIN MENU ==================

while True:
    print("===== Library Management System =====")
    print("1. Admin")
    print("2. User")
    print("3. Issued Books")
    print("4. Exit")

    choice = input("Select Option: ")

    # -------- ADMIN MENU --------
    if choice == "1":
        print("\n--- Admin Menu ---")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")

        admin_choice = input("Select Option: ")

        if admin_choice == "1":
            add_book()
        elif admin_choice == "2":
            update_book()
        elif admin_choice == "3":
            delete_book()
        else:
            print("Invalid Choice!\n")

    # -------- USER MENU --------
    elif choice == "2":
        print("\n--- User Menu ---")
        print("1. Register User")
        print("2. Search Book")
        print("3. View Profile")

        user_choice = input("Select Option: ")

        if user_choice == "1":
            register_user()
        elif user_choice == "2":
            search_book()
        elif user_choice == "3":
            view_profile()
        else:
            print("Invalid Choice!\n")

    # -------- ISSUED BOOK MENU --------
    elif choice == "3":
        print("\n--- Issued Books Menu ---")
        print("1. Issue Book")
        print("2. View Issued Books")
        print("3. Return Book")

        issue_choice = input("Select Option: ")

        if issue_choice == "1":
            issue_book()
        elif issue_choice == "2":
            view_issued_books()
        elif issue_choice == "3":
            return_book()
        else:
            print("Invalid Choice!\n")

    elif choice == "4":
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice!\n")

conn.close()
