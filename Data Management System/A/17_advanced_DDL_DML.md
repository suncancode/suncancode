# Advanced DDL and DML Statements

---

## Outline
- Advanced DDL
- Advanced DML

## Advanced DDL
Defines and modifies database structures with advanced features like complex constraints and triggers.

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
  - **Explanation:** Creates a table with a primary key, checks age (18-25), and a foreign key to Classes. ON DELETE SET NULL sets class_id to NULL if the class is deleted.

- **Alter Table:** 
  ```sql
  ALTER TABLE Students
  ADD email VARCHAR(100) UNIQUE;
  ```
  - **Explanation:** Adds an email column with a UNIQUE constraint to avoid duplicates.

- **Trigger:** 
  ```sql
  CREATE TRIGGER update_student_count
  AFTER INSERT ON Students
  FOR EACH ROW
  BEGIN
      UPDATE Classes
      SET student_count = student_count + 1
      WHERE class_id = NEW.class_id;
  END;
  ```
  - **Explanation:** Automatically increases student_count in Classes when a new student is inserted.

## Advanced DML
Manipulates data with advanced techniques like subqueries, joins, and transactions.

### Example
- **Insert with Subquery:** 
  ```sql
  INSERT INTO Students (id, name, age)
  SELECT id, name, age FROM Temp_Students
  WHERE age > 20;
  ```
  - **Explanation:** Inserts data from Temp_Students (hypothetical) into Students for ages over 20.

- **Update with Join:** 
  ```sql
  UPDATE Students s
  JOIN Classes c ON s.class_id = c.class_id
  SET s.age = s.age + 1
  WHERE c.class_name = 'Math';
  ```
  - **Explanation:** Increases age for students in the Math class by joining with Classes.

- **Delete with Join:** 
  ```sql
  DELETE s FROM Students s
  LEFT JOIN Classes c ON s.class_id = c.class_id
  WHERE c.class_id IS NULL;
  ```
  - **Explanation:** Deletes students with no class by checking for NULL class_id.

- **Transaction:** 
  ```sql
  START TRANSACTION;
  INSERT INTO Students (id, name, age) VALUES (4, 'David', 21);
  UPDATE Classes SET student_count = student_count + 1 WHERE class_id = 101;
  COMMIT;
  ```
  - **Explanation:** Starts a transaction, adds a student and updates class count, then commits changes. Use ROLLBACK to undo if needed.
