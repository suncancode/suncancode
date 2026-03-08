-- Practice basic transation management in ANSI SQL

-- Create sample tables
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY
    Balance DECIMAL(10, 2)
);

-- Insert initial data
INSERT INTO Accounts VALUE (1, 1000.00), (2, 500.00);

-- Start a transaction
BEGIN TRANSACTION;

-- Perform operations
UPDATE Accounts SET Balance = Balance - 200 WHERE AccountID = 1;
UPDATE Accounts SET Balance = Balance + 200 WHERE AccountID = 2;

-- Commit the transaction
COMMIT;

-- Verify 
SELECT * FROM Accounts;

-- Start another transaction and rollback
BEGIN TRANSACTION;
UPDATE Accounts SET Balance = Balance - 500 WHERE AccountID = 1;
ROLLBACK;

-- Verify rollback
SELECT * FROM Accounts;

-- Clean up
DROP TABLE Accounts;