-- select_practice.sql
-- Practice SELECT queries including subqueries, joins, and window functions

-- Create sample tables
CREATE TABLE Employees (
    EmpID INT PRIMARY KEY,
    EmpName VARCHAR(50),
    DeptID INT,
    Salary DECIMAL(10, 2)
);

CREATE TABLE Departments (
    DeptID INT PRIMARY KEY,
    DeptName VARCHAR(50)
);

-- Insert sample data
INSERT INTO Departments VALUES 
(1, 'Engineer'),
(2, 'HR');

INSERT INTO Employees VALUES
(101, 'Sun', 1, 1000000),
(102, 'Khoi', 2, 50000),
(103, 'Tra', 1, 1500000);

-- Basic SELECT with JOIN
SELECT e.EmpName, d.Departments
FROM Employees e
JOIN Departments d ON e.DeptID = d.DeptID;

-- SELECT with Subquery
SELECT EmpName, Salary
FROM Employees
WHERE DeptID = (SELECT DeptID FROM Departments WHERE DeptName = 'Engineer');

-- SELECT with window function
SELECT EmpName, Salary,
    RANK() OVER (PARTITION BY DeptID ORDER BY Salary DESC) as SalaryRank
FROM Employees;

-- SELECT with Correlated Subquery
SELECT EmpName, Salary
FROM Employees e1
WHERE Salary > (SELECT AVG(Salary) FROM Employees e2 WHERE e2.DeptID = e1.DeptID);

-- Verify
SELECT * FROM Employees;
SELECT * FROM Departments;

-- Cleanup
DROP TABLE Employees;
DROP TABLE Departments;