# Discretionary Access Control

---

## Outline
- Introduction to Discretionary Access Control (DAC)
- DAC Mechanisms
- Grant and Revoke Operations
- Practical Examples

---

## Introduction to Discretionary Access Control (DAC)
DAC lets the object owner decide who can access data and with what rights (e.g., read, write), unlike mandatory control.

### Explanation
DAC is flexible, ideal for environments where owners need to share data selectively. It uses access lists and ownership to enforce security.

---

## DAC Mechanisms
Uses Access Control Lists (ACL) and ownership to manage permissions.

### Explanation
ACL lists users/roles and their rights. The owner (usually the creator) can grant or revoke access.

### Example Rights
- `SELECT`: Read data.
- `INSERT`: Add data.
- `UPDATE`: Modify data.
- `DELETE`: Remove data.
- `ALL PRIVILEGES`: All rights.

---

## Grant and Revoke Operations
GRANT gives permissions; REVOKE takes them away. WITH GRANT OPTION allows further delegation.

### Example
- **Grant Read Access:** 
  ```sql
  GRANT SELECT ON Students TO 'student_user';
  ```
  - **Explanation:** Allows `student_user` to read the Students table but not edit it.

- **Grant All with Delegation:** 
  ```sql
  GRANT ALL PRIVILEGES ON Classes TO 'teacher_user' WITH GRANT OPTION;
  ```
  - **Explanation:** Gives `teacher_user` full control over Classes and the ability to grant rights to others.

- **Revoke Access:** 
  ```sql
  REVOKE SELECT ON Students FROM 'student_user';
  ```
  - **Explanation:** Removes read permission from `student_user` on Students.

---

## Practical Examples
### Example 1: Role-Based Access
- **Setup Roles and Grants:** 
  ```sql
  CREATE ROLE 'teacher_role';
  CREATE ROLE 'student_role';
  GRANT SELECT, INSERT, UPDATE, DELETE ON Students TO 'teacher_role';
  GRANT SELECT ON Students TO 'student_role';
  GRANT 'teacher_role' TO 'teacher_user';
  GRANT 'student_role' TO 'student_user';
  ```
  - **Explanation:** Creates roles for teachers (full rights) and students (read-only), then assigns them to users.
- **Check Grants:** 
  ```sql
  SHOW GRANTS FOR 'teacher_user';
  ```
  - **Explanation:** Displays all permissions assigned to `teacher_user`, including those from `teacher_role`.

### Example 2: Revoke on Graduation
- **Revoke Role:** 
  ```sql
  REVOKE 'student_role' FROM 'graduated_user';
  ```
  - **Explanation:** Removes access from a graduated student (`graduated_user`) by revoking their role.
