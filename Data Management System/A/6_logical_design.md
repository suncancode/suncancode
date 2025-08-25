##################
# Logical Design #
##################

---

## Methodology
Logical design transforms a conceptual schema into relational schemas through these steps:

1. **Handle Multivalued Attributes:** Replace with new object classes and one-to-many or many-to-many associations based on meaning.
2. **Handle Association Classes and Link Attributes:** Use triples (one-to-many : class : many-to-one).
3. **Handle Many-to-Many Associations:** Replace with triples (one-to-many : class : many-to-one).
4. **Handle Qualifications:** Turn into one-to-many associations with composite identifiers on the "many" side.
5. **Copy Identifiers:** Move identifiers from "one" to "many" sides, tagging them as FK (foreign keys) with indexes.
6. **Convert Triples to Schemas:** Create tables with primary and foreign keys.

---

## Transformations
This section details how to convert conceptual elements into tables.

- **Multivalued Attributes:** Split into a new table with a one-to-many link.
  - **Example:** STUDENT(snum, name) → PHONE(snum FK, phone_num) with one-to-many.

- **Association Classes and Link Attributes:** Use a middle table with link data.
  - **Example:** ENROLLS (grade) between STUDENT and COURSE → ENROLLMENT(snum FK, course# FK, grade).

- **Many-to-Many Associations:** Create a junction table.
  - **Example:** AUTHOR-BOOK (many-to-many) → AUTHORSHIP(aid FK, isbn FK).

- **Qualifications:** Add composite keys on the "many" side.
  - **Example:** PARENT-CHILD with "birth order" → CHILD(parent_id, birth_order PK).

- **Foreign Keys:** Copy from "one" to "many."
  - **Example:** DEPARTMENT(dept_id) to EMPLOYEE(dept_id FK).
  
- **Triples to Schemas:** Map to tables with keys.
  - **Example:** STUDENT : ENROLLS : COURSE → ENROLLMENT(snum FK, course# FK).

**Key Rule:** Keep data lossless (no information lost).

---

## Example
Let’s apply this to a **Bookstore System**.

- **Conceptual Schema:**
  - BOOK (isbn, title, multivalued authors).
  - CUSTOMER (cid, name) many-to-many BUYS (date, quantity) with BOOK.

- **Step-by-Step:**
  1. **Multivalued Authors:** Create AUTHOR (aid, name), one-to-many from BOOK to AUTHOR.
  2. **Many-to-Many BUYS:** Create PURCHASE (cid FK, isbn FK, date, quantity).
  3. **Qualifications:** None here.
  4. **Foreign Keys:** Copy cid from CUSTOMER, isbn from BOOK to PURCHASE.
  5. **Schemas:**
     - BOOK(isbn PK, title)
     - AUTHOR(aid PK, isbn FK, name)
     - CUSTOMER(cid PK, name)
     - PURCHASE(cid FK1, isbn FK2, date, quantity; PK: cid + isbn)
