# Normalization Exercises - Determining Highest Normal Form

---

## Introduction
This file contains exercises to practice identifying the highest normal form (1NF, 2NF, 3NF, or BCNF) of relational schemas based on given functional dependencies (FDs). Use the provided examples to understand the process, then solve the practice problems.

---

## Background
- **1NF**: All attributes are atomic, no nested sets.
- **2NF**: In 1NF and no partial dependencies (non-key attributes depend on the full primary key).
- **3NF**: In 2NF and no transitive dependencies (non-key attributes depend only on the primary key).
- **BCNF**: In 3NF and every determinant in an FD is a superkey.
- **Process**: Check each level sequentially, starting from 1NF, using the FDs and primary key.

---

## Example Problems with Solutions

### Example 1
- **Schema**: R(A, B, C)
- **Primary Key**: A
- **FDs**: A → B, B → C
- **Solution**:
  - **1NF**: Attributes are atomic (assumed), so R is in 1NF.
  - **2NF**: A is the primary key, and no partial dependency exists (only one attribute in key), so R is in 2NF.
  - **3NF**: Check transitive dependency. A → B and B → C imply A → C (transitive). Since C is a non-key attribute and depends on B (not directly on A), R is not in 3NF.
  - **BCNF**: Since B → C has B as a determinant but not a superkey (A is the key), R is not in BCNF.
  - **Highest Normal Form**: 2NF.

### Example 2
- **Schema**: S(A, B, C, D)
- **Primary Key**: (A, B)
- **FDs**: A → C, (A, B) → D
- **Solution**:
  - **1NF**: Attributes are atomic, so S is in 1NF.
  - **2NF**: Check partial dependency. A → C means C depends only on A (part of the key), violating 2NF.
  - **3NF and BCNF**: Not applicable since 2NF fails.
  - **Highest Normal Form**: 1NF.

### Example 3
- **Schema**: T(A, B, C)
- **Primary Key**: A
- **FDs**: A → B, A → C
- **Solution**:
  - **1NF**: Attributes are atomic, so T is in 1NF.
  - **2NF**: A is the key, no partial dependency, so T is in 2NF.
  - **3NF**: All non-key attributes (B, C) depend directly on A (the key), no transitive dependency, so T is in 3NF.
  - **BCNF**: All FDs (A → B, A → C) have A as a superkey (the primary key), so T is in BCNF.
  - **Highest Normal Form**: BCNF.

---

## Practice Problems

### Problem 1
- **Schema**: R1(A, B, C, D)
- **Primary Key**: (A, B)
- **FDs**: A → C, (A, B) → D, C → D
- **Task**: Determine the highest normal form. Write your solution below:

---

### Problem 2
- **Schema**: R2(A, B, C)
- **Primary Key**: A
- **FDs**: A → B, B → C, C → A
- **Task**: Determine the highest normal form. Write your solution below:

---

### Problem 3
- **Schema**: R3(A, B, C, D)
- **Primary Key**: (A, C)
- **FDs**: A → B, (A, C) → D
- **Task**: Determine the highest normal form. Write your solution below:

---

### Problem 4
- **Schema**: R4(A, B, C, D)
- **Primary Key**: A
- **FDs**: A → B, A → C, B → D
- **Task**: Determine the highest normal form. Write your solution below:

---

## Solution Guidelines
- **Step 1**: Verify 1NF (assume attributes are atomic unless specified otherwise).
- **Step 2**: Check 2NF:
  - If the primary key is composite (e.g., (A, B)), ensure no non-key attribute depends on part of the key.
- **Step 3**: Check 3NF:
  - Ensure no non-key attribute depends on another non-key attribute (transitive dependency).
- **Step 4**: Check BCNF:
  - Ensure every determinant in an FD is a superkey.
- **Write Down**: For each problem, note why it fails or passes each level.

## Example Solution Format
- **For Problem 1** (sample):
  - **1NF**: Attributes are atomic, so R1 is in 1NF.
  - **2NF**: (A, B) is the key, A → C is a partial dependency (C depends on A only), so R1 is not in 2NF.
  - **3NF and BCNF**: Not applicable.
  - **Highest Normal Form**: 1NF.

Feel free to fill in your answers and test with a database tool!

---

## Summary
- Practice identifying the highest normal form using FDs and primary keys.
- Focus on 1NF (atomicity), 2NF (no partial dependencies), 3NF (no transitive dependencies), and BCNF (all determinants are superkeys).