-- views_practice.sql
-- Practice creating and using views

-- Create base tables
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
INSERT INTO Departments VALUES (1, 'HR'), (2, 'IT');
INSERT INTO Employees VALUES
(101, 'Alice', 1, 50000),
(102, 'Bob', 2, 60000);

-- Create a simple view
CREATE VIEW ActiveEmployees AS
SELECT EmpID, EmpName, DeptID
FROM Employees
WHERE Salary > 0;

-- Create a complex view with JOIN and aggregation
CREATE VIEW DeptSummary AS
SELECT d.DeptName, COUNT(e.EmpID) as EmployeeCount, AVG(e.Salary) as AvgSalary
FROM Employees e
JOIN Departments d ON e.DeptID = d.DeptID
GROUP BY d.DeptName;

-- Query the views
SELECT * FROM ActiveEmployees;
SELECT * FROM DeptSummary;

-- Attempt an update on the view (may fail due to complexity)
UPDATE ActiveEmployees
SET DeptID = 2
WHERE EmpID = 101;

-- Drop the views
DROP VIEW ActiveEmployees;
DROP VIEW DeptSummary;

-- Cleanup
DROP TABLE Employees;
DROP TABLE Departments;