-- Practice Read Committed isolation level

-- Note: Requires 2 sessions

-- Session 1: Create and populate table
CREATE TABLE TestTable (
    ID INT PRIMARY KEY,
    Value DECIMAL(10, 2)
);
INSERT INTO TestTable VALUES (1, 100.00);

-- Session 1: Set isolation level and start transaction
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
UPDATE TestTable SET Value = Value + 50 WHERE ID = 1;

-- Session 2: Set isolation level and read
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
SELECT * FROM TestTable; -- Should not see uncommitted changes

-- Session 1: Commit the transaction
COMMIT;

-- Session 2: Read again to see committed changes
SELECT * FROM TestTable;

-- Clean up
DROP TABLE TestTable;
