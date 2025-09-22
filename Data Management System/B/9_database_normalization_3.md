<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Normalization Practice - Lecture 9</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #2c3e50; }
        pre { background: #f4f4f4; padding: 10px; border-left: 4px solid #3498db; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #3498db; color: white; }
    </style>
</head>
<body>
    <h1>Database Normalization Practice - Lecture 9</h1>
    <p>This HTML file provides SQL practice exercises for normalizing relational schemas, based on CSIT882: Data Management Systems Lecture 9. Run these queries in a SQL environment like MySQL Workbench.</p>

    <h2>1. Review of Normal Forms</h2>
    <p>Practice converting a table to 1NF, 2NF, 3NF, and BCNF.</p>
    <pre>
-- Create and populate a non-normalized table
CREATE TABLE Order_Details (
    order_id INT,
    product_id INT,
    items VARCHAR(100), -- Non-atomic, not in 1NF
    price DECIMAL(10, 2)
);

INSERT INTO Order_Details VALUES
(1, 101, 'Book,Pen', 50.00),
(2, 102, 'Laptop', 1000.00);

-- Normalize to 1NF (split items into a new table)
CREATE TABLE Order_Items (
    order_id INT,
    product_id INT,
    item VARCHAR(50),
    price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id, item),
    FOREIGN KEY (order_id, product_id) REFERENCES Order_Details(order_id, product_id)
);

INSERT INTO Order_Items
SELECT order_id, product_id,
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(items, ',', n.n), ',', -1)) as item,
    price
FROM Order_Details
CROSS JOIN (SELECT 1 AS n UNION SELECT 2) n
WHERE n.n <= 1 + (LENGTH(items) - LENGTH(REPLACE(items, ',', '')));

-- Cleanup
DROP TABLE Order_Items, Order_Details;
    </pre>
    <p><strong>Expected Result:</strong> Order_Items table with atomic 'item' values (e.g., 'Book', 'Pen' for order_id 1).</p>

    <h2>2. Normalization Process Example: Student_Course</h2>
    <p>Normalize the Student_Course schema to 2NF and 3NF.</p>
    <pre>
-- Create original table (not in 2NF)
CREATE TABLE Student_Course (
    student_id INT,
    course_id INT,
    instructor VARCHAR(50),
    room VARCHAR(50),
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO Student_Course VALUES
(1, 101, 'Prof A', 'Room 1', 'B'),
(2, 102, 'Prof A', 'Room 1', 'A');

-- Decompose to 2NF
CREATE TABLE Enrollment (
    student_id INT,
    course_id INT,
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE Schedule (
    instructor VARCHAR(50),
    room VARCHAR(50),
    course_id INT,
    PRIMARY KEY (instructor, room),
    FOREIGN KEY (course_id) REFERENCES Enrollment(course_id)
);

INSERT INTO Enrollment SELECT student_id, course_id, grade FROM Student_Course;
INSERT INTO Schedule SELECT instructor, room, course_id FROM Student_Course;

-- Cleanup
DROP TABLE Enrollment, Schedule, Student_Course;
    </pre>
    <p><strong>Expected Result:</strong> Separated tables eliminating partial dependency.</p>

    <h2>3. Normalization to BCNF: Project_Team</h2>
    <p>Normalize the Project_Team schema to BCNF.</p>
    <pre>
-- Create original table (not in BCNF)
CREATE TABLE Project_Team (
    project_id INT,
    team_id INT,
    manager VARCHAR(50),
    location VARCHAR(50),
    PRIMARY KEY (project_id, team_id)
);

INSERT INTO Project_Team VALUES
(1, 101, 'Manager X', 'Sydney'),
(2, 101, 'Manager Y', 'Sydney');

-- Decompose to BCNF
CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    manager VARCHAR(50)
);

CREATE TABLE Team (
    team_id INT PRIMARY KEY,
    location VARCHAR(50)
);

CREATE TABLE Assignment (
    project_id INT,
    team_id INT,
    PRIMARY KEY (project_id, team_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

INSERT INTO Project SELECT DISTINCT project_id, manager FROM Project_Team;
INSERT INTO Team SELECT DISTINCT team_id, location FROM Project_Team;
INSERT INTO Assignment SELECT project_id, team_id FROM Project_Team;

-- Verify
SELECT p.project_id, p.manager, t.team_id, t.location
FROM Project p
JOIN Assignment a ON p.project_id = a.project_id
JOIN Team t ON a.team_id = t.team_id;

-- Cleanup
DROP TABLE Assignment, Team, Project, Project_Team;
    </pre>
    <p><strong>Expected Result:</strong> Tables with no transitive or non-superkey dependencies.</p>

    <h2>4. Practical Considerations</h2>
    <p>Explore trade-offs with a denormalized example.</p>
    <pre>
-- Create denormalized table for performance
CREATE TABLE Denormalized_Sales (
    sale_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    store_location VARCHAR(50),
    sale_amount DECIMAL(10, 2)
);

INSERT INTO Denormalized_Sales VALUES
(1, 'Book', 'Sydney', 50.00),
(2, 'Book', 'Melbourne', 50.00); -- Redundancy for speed

-- Query for total sales (faster due to no join)
SELECT store_location, SUM(sale_amount) as total
FROM Denormalized_Sales
GROUP BY store_location;

-- Cleanup
DROP TABLE Denormalized_Sales;
    </pre>
    <p><strong>Expected Result:</strong> Faster aggregation but data redundancy.</p>

    <h2>Summary</h2>
    <p>These exercises cover normalizing schemas from 1NF to BCNF, with examples of decomposition and practical trade-offs. Test each step and adjust as needed!</p>
</body>
</html>