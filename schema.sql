-- Schema LibrarySystem
CREATE DATABASE IF NOT EXISTS LibrarySystem;
USE LibrarySystem;

-- 1. Books (1:N with BookCopies)
CREATE TABLE IF NOT EXISTS Books (
    isbn VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    genre VARCHAR(50),
    category VARCHAR(50)
);

-- 2. BookCopies (N:1 with Books)
CREATE TABLE IF NOT EXISTS BookCopies (
    copy_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20),
    status VARCHAR(50) DEFAULT 'Available',
    location VARCHAR(100),
    FOREIGN KEY (isbn) REFERENCES Books(isbn) ON DELETE CASCADE
);

-- 3. Students
CREATE TABLE IF NOT EXISTS Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    pin VARCHAR(10)
);

-- 4. Checkouts
CREATE TABLE IF NOT EXISTS Checkouts (
    checkout_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    copy_id INT,
    checkout_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (copy_id) REFERENCES BookCopies(copy_id)
);

-- 5. Staff table for separate staff login
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

-- Default staff account
INSERT INTO Staff (name, email, password) VALUES ('Admin', 'admin@library.com', 'admin123');