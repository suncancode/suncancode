# Derivations of Functional Dependencies

---

## Derivations of Functional Dependencies
Deriving FDs involves using known dependencies (e.g., `X → Y`) to infer new ones based on logical rules.

### Example (Employee Table)
- **Schema**: `e#`, `ename`, `department`, `department-address`, `chairperson`.

- **Given FDs**:
  - `e# → ename`: Employee ID determines name.
  - `e# → department`: ID determines department.
  - `department → department-address`: Department determines address.
  - `department → chairperson`: Department determines chairperson.
  - `chairperson → department`: Chairperson determines department.

- **Derived FDs**:
  - `e# → department-address`: Since `e# → department` and `department → department-address`.
  - `e# → chairperson`: From `e# → department` and `department → chairperson`.
  - `chairperson → department-address`: From `chairperson → department` and `department → department-address`.
  - `e# → ename, department`: Combines `e# → ename` and `e# → department`.
  
### Additional Derivations
- *Example*:
  - `e# → e#`: Always true (self-determination).
  - `e# → e#, ename`: Adds `ename` to the dependent set.
  - `e#, ename → e#`: `e#` is part of the determinant.
  - `e#, department → ename`: `e# → ename` holds regardless of `department`.

### Rules for Derivation
- **Always True**:
  - `a → a`: Any attribute determines itself.
  - `a, b → a`: A set including `a` determines `a`.

- **Inference Rules**:
  - If `a → b`, then `a, c → b`: Adding `c` doesn’t change the dependency.
  - If `a → b, c`, then `a → b` and `a → c`: Split a combined FD.
  - If `a → b` and `b → c`, then `a → c`: Transitivity rule.

- **Usage Note**: Apply these rules to the entire dataset to confirm FDs.

### General Definition
- Let `R = (A1, ..., An)` be a relational schema, and `X`, `Y` be non-empty subsets of `R`.

- `X → Y` means `X` values uniquely determine `Y` values in all rows.
  - *Example*: If `X = {e#}` and `Y = {ename, department}`, then `e# → ename, department`.

---

## Keys, Functional Dependencies and Keys
### Key Concepts
- **Superkey**: A set of attributes that uniquely identifies each row.

- **Candidate Key**: A minimal superkey (no subset works).

- **Primary Key**: A chosen candidate key.

- **Relation to FDs**: A candidate key determines all other attributes via FDs.

- *Example*: If `e# → ename, department, department-address, chairperson`, then `e#` is a candidate key.

### Usage Note
FDs help identify keys by tracking which attributes determine others. Ensure the key covers all dependencies.