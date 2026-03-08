-- Practice Repeatable Read isolation level

-- Note: Requires 2 sessions

-- Session 1: Create and populate table
-- Create sample tables
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY
    Balance DECIMAL(10, 2)
)
INSERT INTO TestTable VALUES (1, 100.00);

-- Session 1: Set isolation level and start transaction
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
SELECT * FROM TestTable; -- initial read

-- Session 2: Update and commit
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
UPDATE TestTable SET Value = Value + 100 WHERE ID = 1;
COMMIT;

-- Session 1: Read again (should be same as initial read)
SELECT * FROM TestTable;

-- Session 1: Commit
COMMIT;

-- Cleanup
DROP TABLE TestTable;