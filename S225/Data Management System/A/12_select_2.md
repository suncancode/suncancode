# SELECT Statement (2)
---

## Outline
- Subqueries in WHERE Clause
- Correlated Subqueries
- EXISTS/NOT EXISTS
- Joins
- Set Operations

---

## Subqueries in WHERE Clause
### What It Does
Uses a subquery in WHERE to filter data.

### Example
- **Older Than Average:** `SELECT name FROM Students WHERE age > (SELECT AVG(age) FROM Students);`
  - **Output:**
    | name |
    |------|
    | Bob  |
- **Alice’s Classes:** `SELECT class_name FROM Classes WHERE student_id = (SELECT id FROM Students WHERE name = 'Alice');`
  - **Output:**
    | class_name |
    |------------|
    | Math       |
    | History    |

### Usage Note
Subquery must return one value for =, >; use IN for multiple.

---

## Correlated Subqueries
### What It Does
Runs a subquery for each row of the outer query.

### Example
- **Students with Classes:** `SELECT name FROM Students s WHERE EXISTS (SELECT * FROM Classes c WHERE c.student_id = s.id);`
  - **Output:**
    | name  |
    |-------|
    | Alice |
    | Bob   |

### Usage Note
Slower, depends on outer row values.

---

## EXISTS/NOT EXISTS
### What It Does
Checks if rows exist in a subquery.

### Example
- **With Classes:** `SELECT name FROM Students s WHERE EXISTS (SELECT * FROM Classes c WHERE c.student_id = s.id);`
  - **Output:**
    | name  |
    |-------|
    | Alice |
    | Bob   |
- **Without Classes:** `SELECT name FROM Students s WHERE NOT EXISTS (SELECT * FROM Classes c WHERE c.student_id = s.id);`
  - **Output:**
    | name   |
    |--------|
    | Charlie|

### Usage Note
Use for existence checks, not values.

---

## Joins
### What It Does
Combines data from multiple tables.

### Example
- **INNER JOIN:** `SELECT s.name, c.class_name FROM Students s INNER JOIN Classes c ON s.id = c.student_id;`
  - **Output:**
    | name   | class_name |
    |--------|------------|
    | Alice  | Math       |
    | Alice  | History    |
    | Bob    | Science    |
- **LEFT JOIN:** `SELECT s.name, c.class_name FROM Students s LEFT JOIN Classes c ON s.id = c.student_id;`
  - **Output:**
    | name   | class_name |
    |--------|------------|
    | Alice  | Math       |
    | Alice  | History    |
    | Bob    | Science    |
    | Charlie| NULL       |

### Usage Note
Use ON for join conditions; LEFT keeps all rows from the left table.

---

## Set Operations
### What It Does
Combines query results (UNION, INTERSECT, EXCEPT).

### Example
- **UNION:** `SELECT name FROM Students WHERE age > 20 UNION SELECT class_name FROM Classes;`
  - **Output:**
    | name   |
    |--------|
    | Bob    |
    | Math   |
    | Science|
    | History|
- **INTERSECT:** `SELECT id FROM Students WHERE age > 19 INTERSECT SELECT student_id FROM Classes;`
  - **Output:**
    | id |
    |----|
    | 1  |
    | 2  |
- **EXCEPT:** `SELECT id FROM Students EXCEPT SELECT student_id FROM Classes;`
  - **Output:**
    | id |
    |----|
    | 3  |

### Usage Note
Must have same column count and types; UNION removes duplicates.

---

## Summary
- **Subqueries:** Filter with inner queries.
- **Correlated:** Run per row with EXISTS.
- **EXISTS/NOT EXISTS:** Check presence.
- **Joins:** Combine tables (INNER, LEFT).
- **Set Operations:** UNION, INTERSECT, EXCEPT.
