-- Practice Read Uncommitted isolation level

-- Note: Requires 2 sessions

-- Session 1: Create and populate table
CREATE TABLE TestTable (
    ID INT PRIMARY KEY,
    Value DECIMAL(10, 2)
);
INSERT INTO TestTable VALUES (1, 100.00);

-- Session 1: Set isolation level and start transation
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION;
UPDATE TestTable SET Value = Value - 50 WHERE ID = 1;

-- Session 2: Try to read uncommitted data
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRANSACTION; 
SELECT * FROM TestTable; -- Should see uncommitted change (dirty read)

-- Session 1: Rollback to demonstrate dirty read effect
ROLLBACK;

-- Session 2: Verify data after rollback
SELECT * FROM TestTable;

-- Clean up
DROP TABLE TestTable;
