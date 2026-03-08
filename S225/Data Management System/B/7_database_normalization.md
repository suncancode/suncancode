# Database Normalization (1NF and 2NF)

---

## First Normal Form (1NF)
### What It Does
A schema is in 1NF if all rows have the same number of fields and only atomic values (no repeating groups).

### Example
- **Non-1NF Table (Employee with Car):**
  | e# | name | car used |
  |----|------|----------|
  | 950001 | Peter | Toyota, PKR234, Ford, WER545 |
  | 932345 | Paul | Honda, RTQ456 |
  | 960020 | Joan | Holden, KLR197, Holden, KLR567 |
- **Issue:** `car used` has groups, not atomic.

- **1NF Table (Employee with Hobbies):**
  | e# | name | Hobbies |
  |----|------|---------|
  | 950001 | Peter | Cooking |
  | 932345 | Paul | Playing games |
  | 960020 | Joan | Reading |
- **Issue:** `Hobbies` is a group.

### Usage Note
To achieve 1NF, split multivalued attributes into separate tables with associations.

---

## Full/Partial Functional Dependencies
### What It Means
- **Full FD:** X → Y if removing any attribute from X breaks the dependency.
- **Partial FD:** Not full; Y depends on a subset of X.

### Example
- **From Inventory Table:** warehouse → warehouse-address is partial if key is (part, warehouse).
- **Usage Note:** Partial FDs cause redundancy; full FDs are ideal for 2NF.

---

## Second Normal Form (2NF)
### What It Does
A schema is in 2NF if every nonprime attribute is fully dependent on the primary key.

### Example
- **Non-2NF Table (Inventory):**
  | part | quantity | warehouse | warehouse-address |
  |------|----------|-----------|-------------------|
  - FD: warehouse → warehouse-address (partial on key (part, warehouse)).
- **To 2NF:** Split into Store (part, quantity, warehouse) and Location (warehouse, warehouse-address).

- **Note:** Schemas with single-attribute keys or ≤2 attributes are always in 2NF.

### Usage Note
Decompose schemas with partial FDs to eliminate anomalies.
