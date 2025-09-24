-- keys_practice.sql
-- Practice identifying and applying different types of keys

-- Create a table with multiple candidate keys
CREATE TABLE Students (
    StudentID INT,
    Email VARCHAR(50),
    Name VARCHAR(50),
    Phone VARCHAR(15),
    PRIMARY KEY (StudentID),
    UNIQUE (Email),
    UNIQUE (Phone)
);

-- Insert sample data
INSERT INTO Students VALUES
(1, 'alice@email.com', 'Alice', '123-456-7890'),
(2, 'bob@email.com', 'Bob', '098-765-4321');

-- Create a related table with foreign key
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- Insert data into Enrollments
INSERT INTO Enrollments VALUES
(101, 1, 1),
(102, 2, 2);

-- Verify (Super Keys include {StudentID}, {Email}, {Phone}, etc.)
SELECT * FROM Students;
SELECT * FROM Enrollments;

-- Test uniqueness (Candidate Keys: StudentID, Email, Phone)
INSERT INTO Students VALUES (3, 'alice@email.com', 'Charlie', '111-222-3333'); -- Should fail due to UNIQUE constraint on Email

-- Cleanup
DROP TABLE Enrollments;
DROP TABLE Students;