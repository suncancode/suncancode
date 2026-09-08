# SQL for Data Warehousing

With the relational schema in place (star/snowflake/constellation, see part 1), the next question is: how do we use SQL to compute analytical (OLAP) aggregations efficiently — across many combinations of dimensions at once?

## 1. The starting problem: the data cube

Given a fact table `Sales(ProductKey, CustomerKey, SalesAmount)`, suppose we want:
- Totals per Product
- Totals per Customer
- Totals per (Product, Customer) pair
- The grand total

The naive approach combines several `SELECT ... GROUP BY ...` statements with `UNION`, filling unused grouping columns with `NULL` for each combination — this manual construction is effectively building a **data cube**.

The problem: for **n dimensions**, this naive approach requires `2ⁿ` `SELECT` statements (e.g. 4 statements for 2 dimensions: both dimensions, each alone, and neither).

## 2. ROLLUP, CUBE and GROUPING SETS

SQL/OLAP extends `GROUP BY` to replace this manual UNION construction:

- **`ROLLUP(a, b)`** — computes aggregates following a **hierarchical order**: `(a,b) → (a) → ()`. It does *not* compute the standalone `(b)` grouping. Useful when the grouping columns represent a hierarchy (e.g. roll up from Product to nothing).
- **`CUBE(a, b)`** — computes **every possible combination**: `(a,b), (a), (b), ()`. This is the full data cube, equivalent to the UNION approach above but far more concise.
- **`GROUPING SETS(...)`** — the most **general** form: you list exactly the combinations you want, instead of getting every combination (`CUBE`) or a fixed hierarchy (`ROLLUP`). Example: `GROUPING SETS((ProductKey, CustomerKey), (ProductKey), ())` computes only 3 of the 4 `CUBE` combinations, skipping the standalone `CustomerKey` grouping.

`ROLLUP` and `CUBE` are simply **shorthand** for the two most common `GROUPING SETS` patterns. Understanding `GROUPING SETS` is understanding the underlying mechanism; `ROLLUP`/`CUBE` are convenient special cases.

## 3. Window functions

While `GROUP BY`/`ROLLUP`/`CUBE` **collapse** rows (one row per group), a **window function** keeps every detail row while making an aggregated value visible alongside it — very useful for comparing a detail row against its group's summary (e.g. "what fraction of the group maximum is this row?").

General syntax:

```sql
function(...) OVER (PARTITION BY ... ORDER BY ... [frame clause])
```

### a) Window partitioning (`PARTITION BY`)
Splits rows into "windows" (similar to `GROUP BY`, but without collapsing rows).

```sql
SELECT ProductKey, CustomerKey, SalesAmount,
       MAX(SalesAmount) OVER (PARTITION BY ProductKey) AS MaxAmount
FROM Sales;
```

Each row keeps its own detail, plus a `MaxAmount` column showing the maximum `SalesAmount` **within the same `ProductKey` group** — no self-join required.

### b) Window ordering (`ORDER BY` inside `OVER`)
Ranks rows within each partition.

```sql
SELECT ProductKey, CustomerKey, SalesAmount,
       RANK() OVER (PARTITION BY CustomerKey ORDER BY SalesAmount DESC) AS SalesRank
FROM Sales;
```

### c) Window framing (`ROWS BETWEEN ... AND ...`)
Defines a "frame" that is only part of the partition, relative to the current row — used for time-series calculations such as **moving averages**.

```sql
-- 3-month moving average
SELECT ProductKey, Year, Month,
       AVG(SalesAmount) OVER (
         PARTITION BY ProductKey
         ORDER BY Year, Month
         ROWS 2 PRECEDING
       ) AS MovAvg
FROM MonthlySales;

-- Year-to-date cumulative total
SELECT ProductKey, Year, Month,
       SUM(SalesAmount) OVER (
         PARTITION BY ProductKey, Year
         ORDER BY Month
         ROWS UNBOUNDED PRECEDING
       ) AS YTD
FROM MonthlySales;
```

## 4. How this connects

`ROLLUP`/`CUBE`/`GROUPING SETS` answer "what is the total for each combination of dimensions?" Window functions answer "compared to that total/group, where does each detail row stand?" The two techniques are commonly combined to build complete analytical reports.

## References
A. Vaisman, E. Zimanyi, *Data Warehouse Systems: Design and Implementation*, Springer Verlag, 2014.
