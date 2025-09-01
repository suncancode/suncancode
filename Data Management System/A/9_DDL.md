# SQL - Data Definition Language (DDL)

---

## CREATE TABLE Statement
The `CREATE TABLE` statement creates a new relational table with a specified name, attribute names, data types, and logical constraints.

### Example
- **Requirements (from Slide):**
  - `name`: Primary key, variable string (max 50 chars), mandatory.
  - `code`: Candidate key, fixed string (exactly 5 chars).
  - `total_staff`: Integer, range 1-50, mandatory.
  - `chair`: Variable string (max 50 chars).

- **SQL Command:**
  ```sql
  CREATE TABLE department (
      name VARCHAR(50) PRIMARY KEY,        -- Primary key, mandatory
      code CHAR(5) UNIQUE,                 -- Candidate key, fixed 5 chars
      total_staff INT NOT NULL CHECK (total_staff BETWEEN 1 AND 50),  -- Mandatory, range 1-50
      chair VARCHAR(50)                    -- Optional
  );
  ```
- **Usage Note:** Use `VARCHAR` for variable strings, `CHAR` for fixed lengths. `PRIMARY KEY` ensures uniqueness and non-null, `UNIQUE` for candidate keys, `CHECK` for range constraints.

### Additional Example
- **Create a Linked Table:**
  ```sql
  CREATE TABLE employee (
      emp_id INT PRIMARY KEY,
      emp_name VARCHAR(50) NOT NULL,
      dept_name VARCHAR(50),
      FOREIGN KEY (dept_name) REFERENCES department(name)
  );
  ```

- **Usage Note:** `FOREIGN KEY` links to the parent table’s primary key, ensuring referential integrity.

---

## DROP TABLE Statement
The `DROP TABLE` statement deletes a table and all its data permanently.

### Example
- **SQL Command:**
  ```sql
  DROP TABLE IF EXISTS department;          -- Safely drops the table
  ```
  
- **Usage Note:** Use `IF EXISTS` to avoid errors if the table doesn’t exist. Drop child tables (e.g., `employee`) first if there are foreign key constraints.

---

## ALTER TABLE Statement
The `ALTER TABLE` statement modifies an existing table’s structure, like adding columns or constraints.

### Example
- **Add a Column:**
  ```sql
  ALTER TABLE employee
  ADD phone VARCHAR(15);                   -- Adds a phone number column
  ```
- **Usage Note:** Can add constraints, e.g., `ALTER TABLE employee ADD CONSTRAINT chk_phone CHECK (phone LIKE '[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]');` for phone format.

### Additional Example
- **Modify a Column:**
  ```sql
  ALTER TABLE department
  MODIFY total_staff INT NOT NULL;         -- Makes total_staff mandatory
  ```
- **Usage Note:** Ensure existing data complies with new constraints (e.g., no nulls in `total_staff`).