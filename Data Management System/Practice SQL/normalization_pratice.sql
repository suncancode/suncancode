-- normalization_practice.sql
-- Practice normalizing schemas to 1NF, 2NF, 3NF, and BCNF

-- Create un-normalized table
CREATE TABLE OrderDetails (
    OrderID INT,
    CustomerID INT,
    CustomerName VARCHAR(50),
    ProductID INT,
    ProductName VARCHAR(50),
    Price DECIMAL(10, 2)
);

-- Insert sample data
INSERT INTO OrderDetails VALUES
(1, 101, 'John Doe', 1, 'Book', 10.00),
(2, 102, 'Jane Smith', 2, 'Pen', 5.00);

-- Normalize to 1NF (assuming no nested data, already in 1NF)
-- Normalize to 2NF (remove partial dependency CustomerID -> CustomerName)
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(50)
);

-- Normalize to 3NF (remove transitive dependency ProductID -> ProductName)
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(50),
    Price DECIMAL(10, 2)
);

-- Final table (Orders) after 3NF
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Migrate data
INSERT INTO Customers 
SELECT DISTINCT CustomerID, CustomerName 
FROM OrderDetails;

INSERT INTO Products 
SELECT DISTINCT ProductID, ProductName, Price
FROM OrderDetails;

INSERT INTO Orders (OrderID, CustomerID, ProductID)
SELECT OrderID, CustomerID, ProductID 
FROM OrderDetails;

-- Verify
SELECT c.CustomerName, p.ProductName, o.OrderID
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Products p ON o.ProductID = p.ProductID;

-- Cleanup
DROP TABLE Orders;
DROP TABLE Products;
DROP TABLE Customers;
DROP TABLE OrderDetails;