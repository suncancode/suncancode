# SELECT Statement (3): A Simple Guide

---

## Outline
- GROUP BY and HAVING
- Aggregate Functions with GROUP BY
- Nested Aggregation
- Common Table Expressions (CTEs)

---

## GROUP BY and HAVING
### What It Does
Groups rows and filters groups.

### Example
- **Count by Age:** `SELECT age, COUNT(*) as student_count FROM Students GROUP BY age;`
  - **Output:**
    | age | student_count |
    |-----|---------------|
    | 19  | 1             |
    | 20  | 1             |
    | 22  | 1             |
- **Filter Groups:** `SELECT age, COUNT(*) as student_count FROM Students GROUP BY age HAVING COUNT(*) > 1;`
  - **Output:** (None with current data, needs more data)
    | age | student_count |
    |-----|---------------|

### Usage Note
Columns in SELECT must be in GROUP BY or an aggregate (e.g., COUNT).

---

## Aggregate Functions with GROUP BY
### What It Does
Calculates values for each group.

### Example
- **Average Age per Age:** `SELECT age, AVG(age) as avg_age FROM Students GROUP BY age;`
  - **Output:**
    | age | avg_age |
    |-----|---------|
    | 19  | 19.0    |
    | 20  | 20.0    |
    | 22  | 22.0    |
- **Class Count per Student:** `SELECT s.name, COUNT(c.class_id) as class_count FROM Students s LEFT JOIN Classes c ON s.id = c.student_id GROUP BY s.name;`
  - **Output:**
    | name   | class_count |
    |--------|-------------|
    | Alice  | 2           |
    | Bob    | 1           |
    | Charlie| 0           |

---

## Nested Aggregation
### What It Does
Nests aggregates for complex calculations.

### Example
- **Avg of Ages > Avg:** `SELECT AVG(age) as overall_avg FROM Students WHERE age > (SELECT AVG(age) FROM Students);`
  - **Output:**
    | overall_avg |
    |-------------|
    | 22.0        |
- **Avg Classes for >1 Class:** `SELECT AVG(class_count) as avg_classes FROM (SELECT COUNT(c.class_id) as class_count FROM Students s LEFT JOIN Classes c ON s.id = c.student_id GROUP BY s.id HAVING COUNT(c.class_id) > 1) as sub;`
  - **Output:**
    | avg_classes |
    |-------------|
    | 2.0         |

### Usage Note
Use subqueries or CTEs for clarity.

---

## Common Table Expressions (CTEs)
### What It Does
Defines temporary tables for queries.

### Example
- **Students with Classes:** 
  ```sql
  WITH StudentClasses AS (
      SELECT s.name, COUNT(c.class_id) as class_count
      FROM Students s
      LEFT JOIN Classes c ON s.id = c.student_id
      GROUP BY s.name
  )
  SELECT name, class_count
  FROM StudentClasses
  WHERE class_count > 0;
  ```
  - **Output:**
    | name   | class_count |
    |--------|-------------|
    | Alice  | 2           |
    | Bob    | 1           |

### Usage Note
CTEs improve readability for complex queries.

---

## Summary
- **GROUP BY/HAVING:** Group and filter groups.
- **Aggregate Functions:** Calculate per group (COUNT, AVG).
- **Nested Aggregation:** Layered calculations.
- **CTEs:** Temporary tables for clarity.