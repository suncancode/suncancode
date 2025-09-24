-- dml_practice.sql
-- Practice DML (Data Manipulation Language) including basic and advanced operations

-- Create sample tables
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(50),
    Status VARCHAR(50)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    Amount DECIMAL(10, 2),
    FOREIGN KEY CustomerID REFERENCES Customers(CustomerID)
);

-- Insert basic data
INSERT INTO Customers VALUES
(1, 'Sun', 'Active'),
(2, 'Khoi', 'Inactive');

INSERT INTO Orders VALUES
(101, 1, '2025-09-01', 100.00),
(102, 2, '2025-09-02', 100000.00);

-- Basic UPDATE
UPDATE Orders
SET Amount = Amount * 1.1
WHERE OrderID = 101;

-- Advanced UPADTE with JOIN
UPDATE Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
SET o.Amount = o.Amount + 50
WHERE c.Status = 'Active';

-- Advanced INSERT with SELECT
INSERT INTO Orders (OrderID, CustomerID, OrderDate, Amount)
SELECT 103, CustomerID, '2025-09-03', 300.00
FROM Customers
WHERE Status = 'Active';

-- Advanced DELETE with Subquery
DELETE FROM Orders
WHERE CustomerID IN (SELECT CustomerID FROM Customers WHERE Status = 'Inactive');

-- Verify
SELECT * FROM Customers;
SELECT * FROM Orders;

-- Clean up 
DROP TABLE Orders;
DROP TABLE Customers;