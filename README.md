# Library-Management-
Library Management System (Python + SQLite3)

Project Description
This is a Library Management System developed using Python and SQLite3 in a single-file implementation.
The system allows:
Admin to manage books (Add, Update, Delete)
Users to register and search books
Book issue and return management
Automatic quantity update during issue/return
This project demonstrates database integration, foreign key relationships, and CRUD operations using SQLite.


🛠 Technologies Used
Python 3
SQLite3 (Built-in Python module)
Datetime module
Command Line Interface (CLI)

1️⃣ Admin Table (Stores Books)
| Column     | Type         | Description      |
| ---------- | ------------ | ---------------- |
| admin_id   | INTEGER (PK) | Book ID          |
| book_title | TEXT         | Book title       |
| author     | TEXT         | Author name      |
| quantity   | INTEGER      | Available copies |

2️⃣ User Table
| Column        | Type         | Description                |
| ------------- | ------------ | -------------------------- |
| issue_id      | INTEGER (PK) | Issue record ID            |
| user_id       | INTEGER (FK) | References user(user_id)   |
| book_id       | INTEGER (FK) | References admin(admin_id) |
| issue_date    | TEXT         | Date of issue              |
| return_status | TEXT         | Returned / Not Returned    |


🔄 System Functionalities
👨‍💼 Admin Operations
Add new book
Update book quantity
Delete book

👤 User Operations
Register new user
Search books
View user profile

📕 Book Issue System
Issue book (if quantity > 0)
View issued books
Return book
Automatic stock update

🔁 Workflow
Admin adds books
User registers
Book can be issued
Quantity decreases
On return, quantity increases
