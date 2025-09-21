# SELECT Statement (5) - Lecture 15 Summary

---

## Outline
- Nested Queries
- Correlated Nested Queries

---

## Nested Queries
### What It Does
Runs a query inside another query in WHERE, SELECT, or FROM clauses.

### Example
- **Find HR Employees:** `SELECT emp_id, emp_name FROM Employees WHERE dept_id IN (SELECT dept_id FROM Departments WHERE dept_name = 'HR');`
  - **Output:**
    | emp_id | emp_name |
    |--------|----------|
    | 101    | Alice    |
    | 104    | David    |
  - **Explanation:** Inner query finds HR dept_id (1), outer query filters Employees with that dept_id.

### Usage Note
Inner query runs once, good for simple filtering.

---

## Correlated Nested Queries
### What It Does
Runs an inner query for each outer row, linking them with shared columns.

### Example
- **Max Salary per Dept:** `SELECT emp_id, emp_name FROM Employees e1 WHERE salary = (SELECT MAX(salary) FROM Employees e2 WHERE e2.dept_id = e1.dept_id);`
  - **Output:**
    | emp_id | emp_name |
    |--------|----------|
    | 101    | Alice    |  (if 50000 is max in HR)
    | 104    | David    |  (if 65000 is max in IT)
  - **Explanation:** Inner query checks max salary per dept for each e1 row, outer query matches.

### Usage Note
Slower due to repeated execution, best for row-specific logic.

---

## Nested Queries in Clauses
### What It Does
Uses nested queries in different parts.
- **SELECT:** Adds dynamic data, e.g., `SELECT emp_name, (SELECT AVG(salary) FROM Employees e2 WHERE e2.dept_id = e1.dept_id) AS dept_avg FROM Employees e1`.
- **FROM:** Creates temp tables, e.g., `SELECT c.customer_name, o.order_count FROM Customers c JOIN (SELECT customer_id, COUNT(*) AS order_count FROM Orders GROUP BY customer_id) o ON c.customer_id = o.customer_id`.

### Usage Note
Flexible but requires clear logic to avoid confusion.

---

## Comparison
### Nested vs. Correlated
- **Nested:** Runs inner query once, fast for independent tasks.
- **Correlated:** Runs per row, powerful but slower.
- **Choose Based On:** Complexity and performance needs.

---

## Summary
- **Nested Queries:** Simple, embedded filtering.
- **Correlated Nested Queries:** Row-linked, complex logic.
- **Clauses:** Enhances SELECT and FROM flexibility.