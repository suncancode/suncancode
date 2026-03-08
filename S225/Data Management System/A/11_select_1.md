# SELECT Statement (1)

---

## Outline
- Functionality and Syntax
- Projection Queries
- Queries with Row Functions
- Queries with Group Functions
- Special Queries

---

## Functionality and Syntax
### What It Does
SELECT gets data from tables and can filter or join them.

### Example
- **Basic:** `SELECT * FROM Students;`
  - **Output:**
    | id  | name   | age |
    |-----|--------|-----|
    | 1   | Alice  | 20  |
    | 2   | Bob    | 22  |
    | 3   | Charlie| 19  |
- **With WHERE:** `SELECT name FROM Students WHERE age > 20;`
  - **Output:**
    | name |
    |------|
    | Bob  |
- **Simple JOIN:** `SELECT Students.name, Classes.class_name FROM Students JOIN Classes ON Students.id = Classes.student_id;`
  - **Output:**
    | name   | class_name |
    |--------|------------|
    | Alice  | Math       |
    | Alice  | History    |
    | Bob    | Science    |

---

## Projection Queries
### What It Does
Selects columns without filtering rows.

### Example
- **All Columns:** `SELECT * FROM Students;`
  - **Output:**
    | id  | name   | age |
    |-----|--------|-----|
    | 1   | Alice  | 20  |
    | 2   | Bob    | 22  |
    | 3   | Charlie| 19  |
- **Some Columns:** `SELECT name FROM Students;`
  - **Output:**
    | name   |
    |--------|
    | Alice  |
    | Bob    |
    | Charlie|
- **Remove Duplicates:** `SELECT DISTINCT class_name FROM Classes;`
  - **Output:**
    | class_name |
    |------------|
    | Math       |
    | Science    |
    | History    |

### Usage Note
Use DISTINCT to show unique values.

---

## Queries with Row Functions
### What It Does
Applies simple functions to each row.

### Example
- **Uppercase Names:** `SELECT UPPER(name) FROM Students;`
  - **Output:**
    | UPPER(name) |
    |-------------|
    | ALICE       |
    | BOB         |
    | CHARLIE     |
- **First Letter:** `SELECT SUBSTR(name, 1, 1) FROM Students;`
  - **Output:**
    | SUBSTR(name, 1, 1) |
    |--------------------|
    | A                  |
    | B                  |
    | C                  |
- **Add 1 to Age:** `SELECT name, age + 1 FROM Students;`
  - **Output:**
    | name   | age + 1 |
    |--------|---------|
    | Alice  | 21      |
    | Bob    | 23      |
    | Charlie| 20      |

### Usage Note
Functions like UPPER (uppercase), SUBSTR (substring), or basic math (+).

---

## Queries with Group Functions
### What It Does
Calculates values for all rows.

### Example
- **Count Students:** `SELECT COUNT(*) FROM Students;`
  - **Output:**
    | COUNT(*) |
    |----------|
    | 3        |
- **Average Age:** `SELECT AVG(age) FROM Students;`
  - **Output:**
    | AVG(age) |
    |----------|
    | 20.33    |
- **Oldest Age:** `SELECT MAX(age) FROM Students;`
  - **Output:**
    | MAX(age) |
    |----------|
    | 22       |

### Usage Note
Use COUNT (count), AVG (average), MAX (maximum).

---

## Special Queries
### What It Does
Does math or simple tasks with a dummy table.

### Example
- **Simple Math:** `SELECT 5 * 2 FROM DUAL;`
  - **Output:**
    | 5 * 2 |
    |-------|
    | 10    |
- **Current Date:** `SELECT SYSDATE() FROM DUAL;`
  - **Output:**
    | SYSDATE()         |
    |-------------------|
    | 2025-09-08 09:32  |
- **Add Days:** `SELECT SYSDATE() + 1 FROM DUAL;`
  - **Output:**
    | SYSDATE() + 1     |
    |-------------------|
    | 2025-09-09 09:32  |
- **Hello Message:** `SELECT 'Hello!' FROM DUAL;`
  - **Output:**
    | 'Hello!' |
    |----------|
    | Hello!   |

### Usage Note
Use DUAL for calculations. Functions like SYSDATE() show current date.

## Summary
- **Functionality:** Basic querying with WHERE and JOIN.
- **Projection:** Select columns, use DISTINCT.
- **Row Functions:** Simple per-row changes (UPPER, SUBSTR).
- **Group Functions:** Overall stats (COUNT, AVG).
- **Special:** Math and dates with DUAL.