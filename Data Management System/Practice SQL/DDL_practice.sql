-- ddl_practice.sql
-- Practice DDL (Data Definition Language) including basic and advanced operations

-- Create a table with primary key and constraint
CREATE TABLE Departments (
    DeptID INT PRIMARY KEY,
    DeptName VARCHAR(50) NOT NULL,
    Location VARCHAR(100),
    CHECK (DeptID > 0)
);

-- Create a linked table with foreign key
CREATE TABLE Employees (
    EmpID INT PRIMARY KEY,
    EmpName VARCHAR(50) NOT NULL,
    DeptID INT
    Salary DECIMAL(10, 2),
    FOREIGN KEY (DeptID) REFERENCES Departments(DeptID)
);

-- Add a CHECK constraint (Advanced DDL)
ALTER TABLE Employees
ADD CONSTRAINT chk_salary CHECK (Salary >= 100000);

-- Modify a column (Advanced DDL)
ALTER TABLE Employees
MODIFY Salary DECIMAL(10, 2) NOT NULL;

-- Drop a constraint (Advanced DDL)
ALTER TABLE Employees
DROP CONSTRAINT chk_salary;

-- Insert sample data to test
INSERT INTO Departments VALUES (1, 'HR', 'Sydney');
INSERT INTO Employees VALUES (101, 'Alice', 1, 50000, CURRENT_DATE);

-- Verify
SELECT * FROM Departments;
SELECT * FROM Employees;

-- Drop tables with CASCADE (Advanced DDL)
DROP TABLE Employees CASCADE;
DROP TABLE Departments;
