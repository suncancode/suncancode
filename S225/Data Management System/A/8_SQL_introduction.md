# Introduction to SQL

---

## Structured Query Language
### History
- **Origin**: Created by IBM in the early 1970s, originally called SEQUEL (Structured English Query Language).

- **First Use**: Implemented in IBM's SYSTEM R, leading to DB/2 and UDB.

- **Standards**: First ANSI/ISO standard (SQL-86) in 1986, updated in 1989, 1992, 1999, 2993, 2996, 2998. 2011. and 2016.

### Nature
- **Command-Oriented**: You gives orders, and the database executes them.

- **Declarative**: You say what you want, not how to do it.

- **Universal**: Works across all relational database systems.

- **Key commands**:
  - *DDL*: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` (Define structure).
  - *DML*: `INSERT`, `UPDATE`, `DELETE`, `SELECT` (Manage data).
  - *DCL*: `GRANT`, `REVOKE` (Control access).

---

## Characteristics
### Key features
- **Easy to Use**: Syntax mimics English, great for beginners.
- **Flexibility**: Handles complex queries with joins and conditions.
- **High performance**: Optimized for large datasets.
- **Standardized**: Mostly consistent across systems (small variations).

---

## Functionality
### Stucture Management Commands (DDL)
These commands define, modify, or delete database structures.

- `CREATE TABLE`: Create new table with columns and constraints.
  - *Example*:

    ```sql
    CREATE TABLE student (
        student_id INT PRIMARY KEY,           -- Unique identifier, mandatory
        first_name VARCHAR(50) NOT NULL,      -- First name, required
        last_name VARCHAR(50),
        date_of_birth DATE
    );
    ```

    - *Note*: List all columns with their data types and constraints. Use `VARCHAR` for variable-length strings, `DATE` for dates.

- `ALTER TABLE`: Adds, modifies, or drops columns/constraints in an existing table.
  - *Example*:

    ```sql
    ALTER TABLE student
    ADD email VARCHAR(100);                -- Adds an email column
    ```
  - *Note*: Can add constraints like `CHECK`: `ALTER TABLE student ADD CONSTRAINT check_email CHECK abc@uowmail.edu.au;`. Be cautious with existing data.

- `DROP TABLE`: Deletes a table and all its data.
  - *Example*:

    ```sql
    DROP TABLE IF EXISTS student;          -- Deletes the student table safely
    ```
  - *Note*: Use `IF EXISTS` to avoid errors if the table doesn't exist!

### Data Manipulation Commands (DML)
These commands manage data within tables.

- `INSERT`: Add new rows to a table.
  - *Example*: 

    ```sql
    INSERT INTO student (student_id, first_name, last_name, date_of_birth)
    VALUES (1, 'John', 'Doe', '2000-05-15');
    ```
  - *Note*: Specify columns and matching values. Ensure `PRIMARY KEY` values are unique and `NOT NULL` fields are filled.

- `UPDATE`: Modifies existing data in a table.
  - *Example*: 

    ```sql
    UPDATE student
    SET last_name = 'Smith'
    WHERE student_id = 1;                  -- Updates only the row with student_id = 1
    ```
  - *Note*: Use `WHERE` to target specific rows. Without it, all rows are updated—use cautiously!

- `DELETE`: Removes rows from a table.
  - *Example*:

    ```sql
    DELETE FROM student
    WHERE student_id = 1;                  -- Deletes the student with student_id = 1
    ```

  - *Note*: `WHERE` limits deletion. Omit it to delete all rows—double-check before executing!

- `SELECT`: Retrieves data from a table.
  - *Example*:

    ```sql
    SELECT first_name, last_name
    FROM student
    WHERE date_of_birth > '2000-01-01';    -- Gets students born after 2000
    ```

  - *Note*: Use `*` for all columns (`SELECT * FROM student;`). Add `WHERE` for filtering, `ORDER BY` for sorting if needed.

### Access Control Commands (DCL)
These commands manage user permissions.

- `GRANT`: Grant privileges to a user.
  - *Example*: 

    ```sql
    GRANT SELECT, INSERT
    ON student
    TO 'user1'@'localhost';                -- Allows user1 to read and insert
    ```

- `REVOKE`: Revokes privileges from a user.
  - *Example*: 

    ```sql
    REVOKE INSERT
    ON student
    FROM 'user1'@'localhost';              -- Removes insert privilege
    ```

### Integrity Constraints
These are not standalone commands but part of table definition to ensure data quality.

- `PRIMARY KEY`: Defines an unique, non-null identifier for each row.
  - *Example*:

    ```sql
    CREATE TABLE course (
        course_id INT PRIMARY KEY,
        course_name VARCHAR(100)
    );
    ```

- `FOREIGN KEY`: Links tables by referencing a primary key.
  - *Example*: 

    ```sql
    CREATE TABLE enrollment (
        student_id INT,
        course_id INT,
        FOREIGN KEY (student_id) REFERENCES student(student_id),
        FOREIGN KEY (course_id) REFERENCES course(course_id)
    );
    ```

- `CHECK`: Enforces a condition on column values.
  - *Example*: 

    ```sql
    ALTER TABLE student
    ADD CONSTRAINT chk_age CHECK (YEAR(CURRENT_DATE) - YEAR(date_of_birth) >= 18);
    ```

---

## Formatting
### How to Write SQL
- **Rules:**
  - Use **UPPERCASE** for keywords (e.g., `SELECT`, `FROM`) to stand out.
  - Use **lowercase** for table/column names (e.g., `student`, `name`).
  - Indent for readability in complex queries.
  - **Example**:

    ```sql
    SELECT s.name, o.order_date
    FROM student s
    JOIN orders o ON s.id = o.student_id
    WHERE o.order_date > '2023-01-01';
    ```

- **Comments**:
  - **Single-line:** Use `--`.
  - **Multi-line:** Use `/* ... */`.
  - *Example*:

    ```sql
    -- This gets all students
    /* This is a
       multi-line note */
    SELECT * FROM student;
    ```

- **Flexibility:** Spaces and new lines don’t affect execution, just ensure syntax.
  - **Example:** `SELECT * FROM student;` and `SELECT *   FROM student;` are the same.