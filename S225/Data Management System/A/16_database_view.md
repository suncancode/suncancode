# Database Views - Lecture 16 Summary

---

## Outline
- Definition and Purpose of Views
- Creating Views
- Using Views
- Types of Views
- Security and Maintenance Considerations

---

## Definition and Purpose of Views
- **Definition**: A view is a virtual table derived from one or more base tables, defined by a SQL query. It does not store data physically but retrieves it dynamically.
- **Purpose**:
  - Simplify complex queries for users.
  - Enhance security by restricting access to specific data.
  - Provide a customized perspective of the database.
- **Example**: A view showing only active employees can hide sensitive salary details from unauthorized users.

---

## Creating Views
- **Syntax**: 
  ```sql
  CREATE VIEW view_name AS
  SELECT column1, column2
  FROM table_name
  WHERE condition;
  ```
- **Example**: Base Table: Employees(EmpID, EmpName, DeptID, Salary)
  ```sql
  CREATE VIEW ActiveEmployees AS
  SELECT EmpID, EmpName, DeptID
  FROM Employees
  WHERE Salary > 0;
  ```
- **Explanation**: The view ActiveEmployees shows only employees with a positive salary, omitting the Salary column.
- **Usage Note**: Views can be based on joins, aggregations, or subqueries.

## Using Views
- **Queruing a View**: Treat it like a table.
  - **Example**:
    ```sql
    SELECT EmpName, DeptID
    FROM ActiveEmployees
    WHERE DeptID = 1;
    ```
  - **Output**:Lists names and department IDs of employees in DeptID 1.

- **Updating Views**:  Some views allow INSERT, UPDATE, DELETE if they are updatable (based on a single table with no aggregations).
  - **Example**:
    ```sql
    UPDATE ActiveEmployees
    SET DeptID = 2
    WHERE EmpID = 101;
    ```

- **Dropping a View**:
  ```sql
  DROP VIEW ActiveEmployees;
  ```

## Types of Views
- **Simple Views**:
  - Based on a single table with no aggregations.
  - **Example**:
    ```sql
    CREATE VIEW DeptEmployees AS SELECT * 
    FROM Employees 
    WHERE DeptID = 1;
    ```

- **Complex Views**: Involve joins, group functions, or subqueries.
  - **Example**:
    ```sql
    CREATE VIEW DeptSummary AS
    SELECT DeptID, COUNT(EmpID) as EmployeeCount, AVG(Salary) as AvgSalary
    FROM Employees
    GROUP BY DeptID;
    ```

- **Materialized Views** (Projected):
  - Store precomputed results for performance (not always supported in basic SQL).

## Security and Maintanance Considerations
- **Security**: Views restrict access to sensitive data.

- **Maintainance**: Views must be updated if base tables change structure.

- **Performance**: Simple view are efficient as queries are rewritten, but complex view may slow down with large data.
