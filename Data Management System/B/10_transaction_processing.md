# Transaction Processing: 

---

## Outline
- What is a Transaction?
- ACID Properties
- Concurrency Control
- Serializability
- Recovery

## What is a Transaction?
### What It Does
A transaction is a logical unit of work in a database, consisting of one or more operations (e.g., reads, writes) that must be executed as a whole or not at all. It ensures that database operations are reliable, even in the face of failures or concurrent access. Think of a transaction as an "all-or-nothing" bundle—either the entire set of changes happens, or none do, maintaining the database in a consistent state.

### Detailed Explanation
Transactions are essential in multi-user environments where multiple operations might interfere with each other. They group related SQL statements (like INSERT, UPDATE, DELETE) into a single atomic unit. In SQL, transactions are managed with commands like `BEGIN TRANSACTION`, `COMMIT` (to save changes), and `ROLLBACK` (to undo changes if something goes wrong).

### Example
- **Scenario:** Transferring $100 from Account A (balance $200) to Account B (balance $50).
  - Steps:
    1. Read balance of A ($200).
    2. Subtract $100 from A (new balance $100).
    3. Write updated balance to A.
    4. Read balance of B ($50).
    5. Add $100 to B (new balance $150).
    6. Write updated balance to B.
  - If the system crashes after step 3, without transactions, A would be $100 short, but B unchanged (inconsistent). With a transaction, if it fails, ROLLBACK restores A to $200.
  - **SQL Code:**
    ```sql
    BEGIN TRANSACTION;
    UPDATE Accounts SET balance = balance - 100 WHERE account_id = 'A';
    UPDATE Accounts SET balance = balance + 100 WHERE account_id = 'B';
    COMMIT;
    ```
  - **If Error:** Use ROLLBACK to undo.

---

## ACID Properties
### What It Means
ACID is the acronym for the four key properties that guarantee transaction reliability in databases. These properties ensure that transactions are processed reliably.

### Detailed Explanation
- **Atomicity:** The transaction is treated as a single unit. If any part fails, the entire transaction is aborted, and the database is left unchanged. This is handled by the DBMS using logging.
- **Consistency:** The transaction must leave the database in a valid state, following all rules (e.g., constraints, triggers). If it violates rules, it's rolled back.
- **Isolation:** Transactions run as if they are the only one, even concurrently. Isolation levels (e.g., READ COMMITTED, SERIALIZABLE) control visibility of changes.
- **Durability:** Once committed, changes are permanent, even if the system crashes (achieved via write-ahead logging).

### Example
- **Atomicity:** In the money transfer, if subtracting from A succeeds but adding to B fails (e.g., network error), atomicity rolls back both, so no money is lost.
- **Consistency:** If a rule says balances can't be negative, a transfer causing A to go negative is rejected.
- **Isolation:** Two transfers from A ($200 to B and $150 to C) concurrently—without isolation, one might see intermediate balances; with isolation, they run as sequential.
- **Durability:** After commit, the $100 transfer is saved on disk; a power outage won't erase it.

---

## Concurrency Control
### What It Does
Manages simultaneous transactions to prevent conflicts, ensuring isolation.

### Detailed Explanation
Concurrency allows multiple transactions to run at the same time for efficiency, but can cause issues like lost updates or dirty reads. Control methods include locking (pessimistic) or multi-version concurrency (optimistic).

### Example
- **Lost Update:** Transaction 1 reads balance $200, adds $50 ($250). Transaction 2 reads $200, adds $30 ($230). If T2 commits first, T1 overwrites to $250, losing $30. Concurrency control locks the row.
- **Dirty Read:** T1 updates balance to $150 but rolls back. T2 reads $150 (dirty) and uses it—control uses isolation to prevent.

---

## Serializability
### What It Means
Ensures concurrent transactions produce the same result as if executed serially (one after another).

### Detailed Explanation
A schedule (sequence of operations) is serializable if equivalent to a serial schedule. Tested with precedence graphs (cycles mean non-serializable). Types: Conflict serializable (based on read/write conflicts), View serializable (based on views).

### Example
- **Non-Serializable Schedule:** T1: Read A, Write A. T2: Read A (after T1 write), Write A. If conflicts overlap wrongly, result differs from serial order.
- **Serializable:** Lock T1 until commit, T2 waits—equivalent to T1 then T2.

---

## Recovery
### What It Does
Restores database after failures using logs.

### Detailed Explanation
Recovery ensures durability and atomicity. Methods: Deferred update (log changes, apply on commit), Immediate update (apply and log for undo).

### Example
- **Deferred Update:** Log "transfer $100" but don't apply until commit; rollback discards log.
- **Immediate Update:** Apply transfer, log old/new values; rollback uses log to undo.

