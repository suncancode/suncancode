#########################
# Relational Data Model #
#########################

---

## Basic Concepts
### What is a Data Model?
A data model is like a blueprint for organizing data. It gives an `abstract view` to `define`, `manipulate`, `retrieve`, and `manage` data. Think of it as a way to see data in different shapes:
- Low-level (e.g., sectors on a hard drive).
- Files and records.
- Tables, trees, graphs, or object classes.

The Relational Model uses **tables** (like spreadsheets) to represent data.

### Origin of Relational Model
Edgar F. Codd from IBM created this model in 1970. It’s now the most popular data model, powering systems like MySQL or Oracle. Other models (e.g., Object
Oriented Model, Object-Relational Model, XML Data Model, and recently JSON) exist, but relational rules the world!

---

## Relational Table
### What is a Relational Table?
A relational table is a two-dimensional grid with:
- **Header (or Relational schema):** Column names ( consists of a sequence of attribute names).
- **Rows:** Data entries (consists of a sequence of values of attributes).
- **Columns:** Attributes with values from a specific set (set of all values of an attribute is called a domain).

A relational table consists of a header and theoretically an unlimited number of rows.
A database is a set of relational tables.

**Example: Applicant Table**
| anum | fname  | lname  | dob        | city     | state             |
|------|--------|--------|------------|----------|-------------------|
| 1    | Harry  | Potter | 1980-12-12 | Perth    | Western Australia |
| 2    | Johnny | Walker | 1990-01-13 | Geelong  | Victoria          |

- Header: {anum, fname, lname, dob, city, state}.
- Domain of "dob": All valid dates.
- A row represents one applicant.

### Mathematical View
A table is a subset of the *Cartesian Product* of its domains. Order of columns doesn’t matter, but each row must be unique.

**Example:** If domains are ID={1,2} and Name={a,b}, the product is {(1,a), (1,b), (2,a), (2,b)}. A table might be {(1,a), (2,b)}.

---

## Principles of Relational Model
### Key Rules
- **First Normal Form (1NF):** No multivalued or nested data. All `values must be atomic`.
  - **Example:** A "phones" column with multiple numbers (e.g., "123, 456") is invalid. Split into a separate table.
- **Access by Content:** `Retrieve data by values, not positions`.
  - **Example:** Find "Harry" by anum=1, not "row 2."
- **Unique Rows:** `No duplicate rows allowed`.
  - **Example:** Two identical applicant rows are not permitted.

---

## Consistency Constraints
### Keys
- **Key:** A minimal set of attributes that uniquely identifies each row.
- **Superkey:** A key with extra attributes (not minimal).
- **Candidate Key:** A minimal key (e.g., {snum} or {name, dob}).
- **Primary Key:** One chosen candidate key (e.g., {snum}).
- **Foreign Key:** Links to a primary/candidate key in another table.

**Example: Student Table**
- Schema: STUDENT(snum, fname, lname, dob).
- Candidate Keys: {snum}, {fname, lname, dob}.
- Primary Key: {snum}.

### NULL Values
- NULL means "unknown," "not applicable," or "missing."
- Allowed in most columns but **not** in primary/candidate keys.

**Example:** DEPARTMENT(name, budget) – budget can be NULL if not set.

### Referential Integrity
- A foreign key must match a primary/candidate key in another table or be NULL.

**Example:** ENROLMENT(s#, course#) – s# must match a snum in STUDENT.

### Domain Constraints
- Rules on attribute values (e.g., date < today, gender = "male" or "female").

**Example:** student-id must be 7 digits.

---

## Summary
- A database is a set of relational tables.
- Tables have rows and columns, all values are atomic.
- Each attribute has a domain.
- Rows show relationships between attributes.
- Tables are subsets of domain products.
- NULL is allowed (except in keys).
- Tables can represent objects or associations.
- Identifiers become keys in tables.
