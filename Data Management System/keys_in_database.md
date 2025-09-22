# Keys in Database - A Simple Guide

---

## Introduction
This file explains different types of keys in relational databases (super key, candidate key, primary key, alternate key, and foreign key) with definitions, examples, and practice exercises.

---

## Types of Keys

### 1. Super Key
- **What It Does**: A set of one or more attributes that uniquely identifies a tuple (row) in a relation. It may include extra attributes not necessary for uniqueness.
- **Example**:
  - Schema: `Student(ID, Name, Email, Phone)`
  - Super Keys: {ID}, {ID, Name}, {ID, Email, Phone}, {Name, Email, Phone} (any combination with ID).
  - **Explanation**: ID alone is enough, but adding other attributes still forms a super key.
- **Note**: Every relation has at least one super key (usually the primary key or its supersets).

### 2. Candidate Key
- **What It Does**: A minimal super key, meaning no subset of it can uniquely identify tuples. It’s a potential primary key.
- **Example**:
  - Schema: `Student(ID, Email)`
  - Candidate Keys: {ID}, {Email}
  - **Explanation**: Both ID and Email can uniquely identify a student, and neither can be reduced further.
- **Note**: A relation can have multiple candidate keys.

### 3. Primary Key
- **What It Does**: A single chosen candidate key used to uniquely identify tuples. It cannot contain NULL values.
- **Example**:
  - Schema: `Student(ID, Email, Name)`
  - Candidate Keys: {ID}, {Email}
  - Primary Key: {ID} (chosen as the main identifier)
  - **Explanation**: ID is selected as the primary key, and Email becomes an alternate key.
- **Note**: Only one primary key is allowed per table.

### 4. Alternate Key
- **What It Does**: A candidate key that is not selected as the primary key.
- **Example**:
  - Schema: `Student(ID, Email, Name)`
  - Candidate Keys: {ID}, {Email}
  - Primary Key: {ID}
  - Alternate Key: {Email}
  - **Explanation**: Email could have been the primary key but is an alternate since ID is chosen.
- **Note**: Alternate keys are useful for additional unique constraints.

### 5. Foreign Key
- **What It Does**: An attribute (or set of attributes) in one table that links to the primary key of another table, enforcing referential integrity.
- **Example**:
  - Schema: `Student(ID, Name)` and `Enrollment(StudentID, Course)`
  - Primary Key in Student: {ID}
  - Foreign Key in Enrollment: {StudentID} → References Student(ID)
  - **Explanation**: StudentID in Enrollment must match an existing ID in Student.
- **Note**: Can contain NULL values if the relationship is optional.

---

## Example Scenario
- **Schema**: `Employee(EmpID, EmpName, DeptID, Email)`
- **FDs**: EmpID → {EmpName, DeptID, Email}, Email → EmpID
- **Analysis**:
  - **Super Keys**: {EmpID}, {EmpID, EmpName}, {Email}, {Email, DeptID}, etc.
  - **Candidate Keys**: {EmpID}, {Email} (both are minimal and unique).
  - **Primary Key**: {EmpID} (chosen).
  - **Alternate Key**: {Email}.
  - **Foreign Key**: If DeptID references a `Department(DeptID, DeptName)` table, then DeptID is a foreign key.

---

## Practice Exercises

### Exercise 1
- **Schema**: `Product(ProductID, ProductName, SerialNumber)`
- **FDs**: ProductID → {ProductName, SerialNumber}, SerialNumber → ProductID
- **Tasks**:
  - List all super keys.
  - Identify all candidate keys.
  - Suggest a primary key and an alternate key.
  - Write your answers below:

---

### Exercise 2
- **Schema**: `Order(OrderID, CustomerID, OrderDate, CustomerName)`
- **FDs**: (OrderID, CustomerID) → {OrderDate, CustomerName}, CustomerID → CustomerName
- **Tasks**:
  - List all super keys.
  - Identify all candidate keys.
  - Suggest a primary key.
  - Identify any foreign key if linked to a `Customer(CustomerID, CustomerName)` table.
  - Write your answers below:

---

### Exercise 3
- **Schema**: `Student(StudentID, CourseID, Grade, Email)`
- **FDs**: (StudentID, CourseID) → Grade, Email → StudentID
- **Tasks**:
  - List all super keys.
  - Identify all candidate keys.
  - Suggest a primary key and an alternate key.
  - Write your answers below:

---

## Solution Guidelines
- **Super Keys**: Include the primary key and any combination with other attributes.
- **Candidate Keys**: Find minimal sets that uniquely identify tuples (no redundant attributes).
- **Primary Key**: Choose one candidate key; ensure it’s minimal and NULL-free.
- **Alternate Key**: Any unused candidate key.
- **Foreign Key**: Look for attributes linking to another table’s primary key.
- **Write Format**: E.g., "Super Keys: {A}, {A, B}; Candidate Keys: {A}; Primary Key: {A}; Alternate Key: None."

## Sample Solution (for Exercise 1)
- **Super Keys**: {ProductID}, {ProductID, ProductName}, {SerialNumber}, {SerialNumber, ProductName}, etc.
- **Candidate Keys**: {ProductID}, {SerialNumber}.
- **Primary Key**: {ProductID}.
- **Alternate Key**: {SerialNumber}.

Feel free to fill in your answers and verify with a database tool!

---

## Summary
- **Super Key**: Any unique identifier (may include extras).
- **Candidate Key**: Minimal unique identifier.
- **Primary Key**: Chosen unique identifier.
- **Alternate Key**: Unused candidate key.
- **Foreign Key**: Links to another table’s primary key.