# Database Normalization 3

---

## Outline
- Review of Normal Forms (1NF, 2NF, 3NF, BCNF)
- Normalization Process for Relational Schemas
- Practical Examples
- Special Considerations

---

## Review of Normal Forms
### 1NF (First Normal Form)
- **Definition**: All attributes are atomic (no nested sets or multi-valued attributes).
- **Example**: A table with a single phone number per row, not a list.
- **Check**: Ensure no repeating groups.

### 2NF (Second Normal Form)
- **Definition**: In 1NF and no partial dependencies (non-key attributes depend on the full primary key).
- **Example**: For a composite key (OrderID, ProductID), CustomerName must depend on both, not just OrderID.
- **Check**: Remove dependencies on part of a composite key.

### 3NF (Third Normal Form)
- **Definition**: In 2NF and no transitive dependencies (non-key attributes depend only on the primary key).
- **Example**: If EmployeeID → Department → Location, Location must be separated.
- **Check**: Ensure no non-key attribute depends on another non-key attribute.

### BCNF (Boyce-Codd Normal Form)
- **Definition**: In 3NF and every determinant in a functional dependency (FD) is a superkey.
- **Example**: If Department → Location but Department is not a superkey, decompose further.
- **Check**: All left-hand sides of FDs must be superkeys.

---

## Normalization Process for Relational Schemas
### Steps
1. **Identify Functional Dependencies (FDs)**:
   - List all FDs based on data and business rules (e.g., CustomerID → CustomerName).
2. **Check Current Normal Form**:
   - Determine the primary key and test against 1NF, 2NF, 3NF, BCNF rules.
3. **Decompose**:
   - Split into smaller tables if not in the desired form, ensuring lossless join and (if possible) dependency preservation.
4. **Verify**:
   - Confirm new tables eliminate anomalies.

---

## Practical Examples
### Example 1: Order Schema
- **Un-normalized Schema**: Order(OrderID, CustomerID, CustomerName, ProductID, ProductName, Price)
- **FDs**: CustomerID → CustomerName, OrderID → ProductID, ProductID → ProductName, OrderID → Price
- **Normalization**:
  - **1NF**: Assumed atomic (no nested data).
  - **2NF**: Decompose CustomerName (depends on CustomerID) into Customer(CustomerID, CustomerName).
  - **3NF**: Decompose ProductName (transitive via ProductID) into Product(ProductID, ProductName).
  - **BCNF**: If Price depends on ProductID (ProductID → Price), split into Order(OrderID, CustomerID, ProductID) and Product(ProductID, ProductName, Price).
- **Result**: Fully normalized to BCNF.

### Example 2: Employee Schema
- **Schema**: Employee(EmpID, DeptID, DeptName, ManagerID)
- **FDs**: EmpID → DeptID, DeptID → DeptName, EmpID → ManagerID
- **Normalization**:
  - **1NF**: Atomic attributes.
  - **2NF**: No partial dependency (EmpID is key).
  - **3NF**: DeptName depends on DeptID (transitive), so split into Department(DeptID, DeptName).
  - **BCNF**: EmpID → ManagerID is fine (EmpID is key), so Employee(EmpID, DeptID, ManagerID) and Department(DeptID, DeptName) are in BCNF.
- **Result**: BCNF.

---

## Special Considerations
- **Dependency Preservation**:
  - Decomposing to BCNF may lose some FDs (e.g., OrderID, ProductID → Price if Price is split).
  - Solution: Use joins or views to restore dependencies.
- **Performance Trade-off**:
  - Higher normalization (BCNF) reduces redundancy but increases join costs.
  - 3NF may be preferred for performance in some cases.

---

## Summary
- **1NF**: Atomic attributes, no nesting.
- **2NF**: No partial dependencies.
- **3NF**: No transitive dependencies.
- **BCNF**: All determinants are superkeys.
- **Process**: Identify FDs, decompose, and balance dependency preservation with performance.
- **Examples**: Practical schemas normalized step-by-step.
