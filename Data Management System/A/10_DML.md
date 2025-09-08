# SQL - Data Manipulation Language (DML): A Simple Guide

---

## Introduction to DML
### What It Does
DML is the part of SQL for manipulating data in existing tables (unlike DDL, which defines structures).

### Example
- **Scenario:** A school database with `student` (student_id, name, age) and `enrollment` (student_id, course, grade).
- **Usage Note:** DML commands are declarative—you specify what, not how. Always end with `;`.

---

## INSERT Statement
### What It Does
Adds new rows to a table.

### Example
- **SQL Command:**
  ```sql
  INSERT INTO student (student_id, name, age)
  VALUES (1, 'John Doe', 20);
  ```
- **Usage Note:** List columns if not inserting all. For multiple rows: `VALUES (2, 'Jane Smith', 22), (3, 'Bob Johnson', 19);`. Ensure no duplicate PRIMARY KEY.

### Additional Example
- **Insert with Default Values:** If age defaults to 18: `INSERT INTO student (student_id, name) VALUES (4, 'Alice');`.

---

## UPDATE Statement
### What It Does
Modifies existing data.

### Example
- **SQL Command:**
  ```sql
  UPDATE student
  SET age = 21
  WHERE student_id = 1;
  ```
- **Usage Note:** Use `WHERE` to target rows. Update multiple columns: `SET name = 'Johnny Doe', age = 21 WHERE student_id = 1;`.

### Additional Example
- **Update Based on Condition:** `SET grade = 'A' WHERE age > 20;` in `enrollment`.

---

## DELETE Statement
### What It Does
Removes rows from a table.

### Example
- **SQL Command:**
  ```sql
  DELETE FROM student
  WHERE student_id = 1;
  ```
- **Usage Note:** Omit `WHERE` to delete all (dangerous!). Check FOREIGN KEY constraints first.

### Additional Example
- **Delete with Subquery:** `DELETE FROM enrollment WHERE student_id IN (SELECT student_id FROM student WHERE age < 18);`.

---

## SELECT Statement
### What It Does
Retrieves data from tables.

### Example
- **SQL Command:**
  ```sql
  SELECT name, age
  FROM student
  WHERE age > 20
  ORDER BY name ASC;
  ```
- **Usage Note:** Use `*` for all columns. Add `JOIN` for multiple tables: `FROM student s JOIN enrollment e ON s.student_id = e.student_id;`.

### Additional Example
- **Aggregate Query:** `SELECT AVG(age) FROM student GROUP BY department;`.
