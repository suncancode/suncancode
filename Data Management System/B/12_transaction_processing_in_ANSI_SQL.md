# Transaction Processing in ANSI SQL - Summary

---

## 1. Transaction Overview
- **Definition**: A transaction is a logical unit of work consisting of one or more SQL operations (INSERT, UPDATE, DELETE, SELECT) that must be executed entirely or not at all.
- **ACID Properties**:
  - **Atomicity**: All operations are completed or rolled back.
  - **Consistency**: Maintains database integrity.
  - **Isolation**: Protects transactions from interference until completion.
  - **Durability**: Ensures changes persist after commit.
- **Commands**:
  - `BEGIN TRANSACTION`: Starts a transaction.
  - `COMMIT`: Saves changes.
  - `ROLLBACK`: Undoes changes.

---

## 2. Isolation Levels in ANSI SQL
- **Read Uncommitted**: Allows reading uncommitted data (dirty reads possible, lowest isolation).
- **Read Committed**: Prevents dirty reads, but allows non-repeatable reads and phantom reads.
- **Repeatable Read**: Ensures consistent reads within a transaction, prevents non-repeatable reads.
- **Serializable**: Highest isolation, prevents all anomalies (dirty reads, non-repeatable reads, phantom reads).
- **Setting Isolation**:
  - Use `SET TRANSACTION ISOLATION LEVEL {level}` (e.g., `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;`).

---

## 3. Transaction Anomalies
- **Dirty Read**: Reading uncommitted data that may be rolled back.
- **Non-Repeatable Read**: Data changes between reads in the same transaction.
- **Phantom Read**: New rows appear in the result set due to other transactions.

---

## 4. Practical Applications
- Choose isolation levels based on application needs (e.g., Serializable for critical data, Read Committed for performance).
