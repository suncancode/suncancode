# Database Auditing

---

## Outline
- Introduction to Database Auditing
- Types of Auditing
- Audit Mechanisms in SQL
- Practical Implementation

---

## Introduction to Database Auditing
Tracks, records, and analyzes database activities to detect issues and ensure compliance.

### Explanation
Auditing helps identify unauthorized access, monitor user actions, and support security audits.

---

## Types of Auditing
- **System Auditing:** Monitors system-level events (e.g., logins).
- **Object Auditing:** Tracks actions on specific objects (e.g., tables).

### Explanation
System auditing covers overall usage; object auditing focuses on data changes.

---

## Audit Mechanisms in SQL
### What It Does
Uses triggers, logs, and audit commands to record activities.

### Example
- **Trigger for Updates:** 
  ```sql
  CREATE TABLE Audit_Log (
      audit_id INT AUTO_INCREMENT PRIMARY KEY,
      table_name VARCHAR(50),
      action VARCHAR(50),
      user VARCHAR(50),
      change_date DATETIME
  );

  CREATE TRIGGER log_student_update
  AFTER UPDATE ON Students
  FOR EACH ROW
  BEGIN
      INSERT INTO Audit_Log (table_name, action, user, change_date)
      VALUES ('Students', 'UPDATE', USER(), NOW());
  END;
  ```
  - **Explanation:** Logs every update on Students with user and timestamp.

- **Enable General Log in MySQL:** 
  ```sql
  SET GLOBAL general_log = 'ON';
  SET GLOBAL log_output = 'TABLE';
  ```
  - **Explanation:** Records all queries in mysql.general_log table.

- **Audit SELECT in Oracle (Simulated):** 
  ```sql
  AUDIT SELECT ON Students BY ACCESS;
  ```
  - **Explanation:** Logs all SELECT queries on Students (Oracle-specific).

---

## Practical Implementation
Applies auditing in real scenarios like tracking changes.

### Example 1: Track Age Changes
- **Trigger with Old/New Values:** 
  ```sql
  CREATE TRIGGER log_age_update
  AFTER UPDATE ON Students
  FOR EACH ROW
  BEGIN
      INSERT INTO Audit_Log (table_name, action, user, change_date, old_value, new_value)
      VALUES ('Students', 'UPDATE', USER(), NOW(), OLD.age, NEW.age);
  END;
  ```
  - **Explanation:** Records old and new age values for tracking changes.
- **Check Log:** 
  ```sql
  SELECT * FROM Audit_Log WHERE table_name = 'Students';
  ```
  - **Explanation:** Views the audit history for Students.

### Example 2: Monitor Excessive Access
- **Log Analysis:** 
  ```sql
  SET GLOBAL general_log = 'ON';
  SELECT user_host, count(*) as access_count
  FROM mysql.general_log
  WHERE command_type = 'Query'
  GROUP BY user_host
  HAVING count(*) > 100;
  ```
  - **Explanation:** Counts queries per user; flags excessive access (>100).

---

## Summary
- **Auditing:** Monitors and records activities.
- **Types:** System and object.
- **Mechanisms:** Triggers, logs, audit commands.
- **Implementation:** Track changes and detect anomalies.