# SELECT Statement (4): A Simple Guide

---

## Outline
- Window Functions
- Ranking Functions
- Value Functions
- Frame Specification

---

## Window Functions
### What It Does
Calculates values over a set of rows (window) for each row, keeping all rows.

### Example
- **Sum by Age:** `SELECT name, age, SUM(age) OVER (PARTITION BY age) as age_sum FROM Students;`
  - **Output:**
    | name   | age | age_sum |
    |--------|-----|---------|
    | Alice  | 20  | 20      |
    | Bob    | 22  | 22      |
    | Charlie| 19  | 19      |
  - **Explanation:** PARTITION BY age groups by age. SUM(age) adds ages in each group. With one student per age, it matches the age.

---

## Ranking Functions
### What It Does
Assigns a rank to each row based on order.

### Example
- **Rank by Age:** `SELECT name, age, ROW_NUMBER() OVER (ORDER BY age DESC) as row_num, RANK() OVER (ORDER BY age DESC) as rank_num, DENSE_RANK() OVER (ORDER BY age DESC) as dense_rank FROM Students;`
  - **Output:**
    | name   | age | row_num | rank_num | dense_rank |
    |--------|-----|---------|----------|------------|
    | Bob    | 22  | 1       | 1        | 1          |
    | Alice  | 20  | 2       | 2        | 2          |
    | Charlie| 19  | 3       | 3        | 3          |
  - **Explanation:** ROW_NUMBER() gives unique numbers (1, 2, 3). RANK() and DENSE_RANK() give ranks, with DENSE_RANK() avoiding gaps if ties exist (none here). ORDER BY age DESC sorts highest to lowest.

### Usage Note
ORDER BY in OVER sets the ranking order; PARTITION BY (if used) splits into groups.

---

## Value Functions
### What It Does
Fetches values from other rows in the window.

### Example
- **First and Neighbor Ages:** `SELECT name, age, FIRST_VALUE(age) OVER (ORDER BY age) as first_age, LAG(age) OVER (ORDER BY age) as prev_age, LEAD(age) OVER (ORDER BY age) as next_age FROM Students;`
  - **Output:**
    | name   | age | first_age | prev_age | next_age |
    |--------|-----|-----------|----------|----------|
    | Charlie| 19  | 19        | NULL     | 20       |
    | Alice  | 20  | 19        | 19       | 22       |
    | Bob    | 22  | 19        | 20       | NULL     |
  - **Explanation:** FIRST_VALUE(age) takes the smallest age (19) for all rows. LAG(age) gets the previous row’s age (NULL for first). LEAD(age) gets the next row’s age (NULL for last). ORDER BY age sorts ascending.

### Usage Note
Default frame is from start to current row; adjust with frame specification.

---

## Frame Specification
### What It Does
Defines the range of rows (frame) for window functions.

### Example
- **Running Sum:** `SELECT name, age, SUM(age) OVER (ORDER BY age ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_sum FROM Students;`
  - **Output:**
    | name   | age | running_sum |
    |--------|-----|-------------|
    | Charlie| 19  | 19          |
    | Alice  | 20  | 39          |
    | Bob    | 22  | 61          |
  - **Explanation:** ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW includes all rows from the start to the current row. Running sum adds ages: 19 + 20 = 39, then 39 + 22 = 61. This is great for cumulative totals.

---

## Summary
- **Window Functions:** Calculate over windows, keep all rows.
- **Ranking Functions:** Assign unique or ranked positions.
- **Value Functions:** Fetch nearby row values.
- **Frame Specification:** Customize the window range.