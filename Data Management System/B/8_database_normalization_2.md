# Database Normalization (3NF and BCNF) 

## Introduction
- **Subject**: CSIT882: Data Management Systems
- **Topic**: Database Normalization focusing on Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF)
- **Objective**: Eliminate data redundancy and anomalies (insert/update/delete) through normalization.

## Outline
- Third Normal Form (3NF)
- Boyce-Codd Normal Form (BCNF)

## Transitive Functional Dependency
- **Definition**: In a relational schema R, if there are non-empty subsets X, Y, Z of R with valid functional dependencies (FDs) X → Z and Z → Y, then X → Y is a transitive FD.
- **Transitive Dependence**: Y is transitively dependent on X if X → Y is valid and transitive.
- **Example**: If X = employee_id, Z = department, Y = department_salary, then employee_id → department → department_salary is transitive, causing redundancy.

## Third Normal Form (3NF)
- **Definition**: A schema R is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key.
- **Alternative Definition**: R is in 3NF if for every FD X → A, either:
  1. X is a superkey, or
  2. A is a prime attribute.
- **Example: Supplier Schema**
  - Attributes: s# (primary key), sname, company_name, city
  - FDs: s# → sname, s# → company_name, s# → city, company_name → city
  - Minimal key: (s#)
  - **Issue**: Not in 3NF because city is transitively dependent on s# via company_name.
  - **Decomposition**:
    - Supplier_new: s#, sname, company_name (s# → sname, s# → company_name; key: s#)
    - Company: company_name, city (company_name → city; key: company_name)
  - Both are in 3