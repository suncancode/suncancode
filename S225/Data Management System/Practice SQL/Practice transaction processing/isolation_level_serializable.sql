-- Practice Serializable isolation level

-- Note: Requires 2 sessions

-- Session 1: Create and populate table
CREATE TABLE TestTable (
    ID INT PRIMARY KEY,
    Value DECIMAL(10, 2)
);
INSERT INTO TestTable VALUES (1, 100.00);

-- Session 1: Set isolation level and start transaction
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
SELECT * FROM TestTable WHERE Value > 50;

-- Session 2: Try to insert a conflicting row
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
INSERT INTO TestTable VALUES (2, 200.00); -- May be blocked or cause deadlock

-- Session 1: Commit
COMMIT;

-- Session 2: Commit
COMMIT;

-- Verify 
SELECT * FROM TestTable;

-- Cleanup
DROP TABLE TestTable;