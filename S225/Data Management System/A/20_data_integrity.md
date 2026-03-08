# Data Integrity

---

## Outline
- Introduction to Data Integrity
- Types of Data Integrity
- Constraints in SQL
- Maintaining Data Integrity

---

## Introduction to Data Integrity
Ensures data is accurate, consistent, and reliable throughout its lifecycle.

### Explanation
Data integrity prevents corruption or invalid entries, ensuring the database reflects reality.

---

## Types of Data Integrity
- **Entity Integrity:** Each row is unique (via primary key).
- **Referential Integrity:** Maintains relationships (via foreign keys).
- **Domain Integrity:** Ensures data fits defined rules (e.g., age range).

---

## Constraints in SQL
Uses SQL constraints to enforce data integrity.

### Example
- **Create Table with Constraints:** 
  ```sql
  CREATE TABLE Students (
      id INT PRIMARY KEY,
      name VARCHAR(50) NOT NULL,
      age INT CHECK (age BETWEEN 18 AND 25),
      class_id INT,
      FOREIGN KEY (class_id) REFERENCES Classes(class_id) ON DELETE SET NULL
  );
  ```
  - **Explanation:** PRIMARY KEY ensures unique IDs, NOT NULL requires names, CHECK limits age, FOREIGN KEY links to Classes with ON DELETE SET NULL for safety.

- **Add Unique Constraint:** 
  ```sql
  ALTER TABLE Students
  ADD email VARCHAR(100) UNIQUE;
  ```
  - **Explanation:** Adds an email column where each value must be unique.

---

## Maintaining Data Integrity
Uses triggers, transactions, and backups to protect data.

### Example
- **Trigger for Age Check:** 
  ```sql
  CREATE TRIGGER check_age
  BEFORE INSERT ON Students

  FOR EACH ROW
  BEGIN
      IF NEW.age < 18 OR NEW.age > 25 THEN
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Age must be between 18 and 25';
      END IF;
  END;
  ```
  - **Explanation:** Checks age before insertion; rejects if outside 18-25.

- **Transaction for Consistency:** 
  ```sql
  START TRANSACTION;
  INSERT INTO Students (id, name, age, class_id) VALUES (4, 'Emma', 21, 101);
  UPDATE Classes SET student_count = student_count + 1 WHERE class_id = 101;
  COMMIT;
  ```
  - **Explanation:** Adds a student and updates class count together; rolls back if one fails.

- **Backup Command:** 
  - **Command:** `mysqldump -u user -p database > backup.sql`
  - **Explanation:** Creates a backup file to restore data if lost.

---

## Summary
- **Data Integrity:** Keeps data valid.
- **Types:** Entity, referential, domain.

- **Constraints:** Enforce rules in SQL.
- **Maintenance:** Use triggers, transactions, backups.
