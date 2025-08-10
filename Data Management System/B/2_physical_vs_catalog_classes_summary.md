#######################################
# Physical vs Catalog Classes Summary #
#######################################

---

## 1. Basic Concepts
### Description
- *Physical Class*: Represents specific, non-reusable instances tied to a particular object.

- *Catalog Class*: Represents reusable, general descriptions applicable to multiple instances.

### Example
- *Physical Class*: A single book copy.
- *Catalog Class*: A book title shared by many copies.

--- 

## 2. Sample Phisical Classes
### Description
Physical classes focus on individual, tangible instances with unique identifiers.

### Example
**Use Case**: Track specific item - which book copy is borrowed by a student.
- `BOOK-COPY` (CopyID, Location).
- `ROOM` (RoomNumber, Building).
- `BORROW-INSTANCE` (BorrowID, Date, Time).

## 3. Sample Catalog Classes
### Description
Catalog classes provide general templates reusble across multiple instances.

### Example
**Use Case**: Store reusable information - all copy of "How to crack coding interview" share the same title.
- `BOOK` (ISBN, Title)
- `ROOM` (Type, Capacity)

---

## 4. Physical vs Catalog Classes
### Description
- *Physical*: Focus on specific instances.

- *Catalog*: Focus on types or templates.

### Example
- *Physical*: Room 3-125.
- *Catalog*: Building 3. 

---

## 5. Equivalence
### Description
Two database designs are equivalent if they store the same information and provide the same functionality.

### Example
- *Design 1*: Use `BOOK` to list all book titles. 

- *Design 2*: Use `BOOK-COPY` to list all copies.

Not equivalent `BOOK` tracks titles, while `BOOK-COPY` tracks instances, serving different purposes.

--- 

### 6. Correctness
### Description
A design is correct if it accurately models the real-world scenario it intends to represent.

### Example
**Scenario**: Students borrow book copies from a library.
- *Correct Design*: Use `STUDENT` and `BOOK-COPY` with a `BORROW-INSTANCE` relationship.

- *Incorrect Design*: Use `BOOK` (catalog) alone, as it doesn't track specific copies available for borrowing.
