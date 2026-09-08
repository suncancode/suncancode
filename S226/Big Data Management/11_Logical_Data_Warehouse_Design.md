# Logical Data Warehouse Design

## 1. OLAP Technologies

Before storing warehouse data, we choose an implementation technology:

- **ROLAP (Relational OLAP)** — data stored in relational tables, with SQL extensions and special access methods to implement OLAP operations.
- **MOLAP (Multidimensional OLAP)** — data stored in special structures (e.g. arrays). Better query/aggregation performance than ROLAP, and typically less storage than ROLAP for the same aggregated data.
- **HOLAP (Hybrid OLAP)** — combines both, e.g. detailed data stored relationally, pre-computed aggregations stored in a MOLAP store.

This lecture focuses on **ROLAP**: how to translate a conceptual multidimensional (MultiDim) model — facts and dimensions — into relational tables. This is the "logical design" step.

## 2. Relational Data Warehouse Schemas

The core idea: a **fact table** (holds measures — numeric values to analyze) is linked to several **dimension tables** (hold descriptive context: product, store, time, etc.).

### Star schema
- One fact table + a set of dimension tables, each dimension is a single table (not split further).
- Dimension tables are **denormalized** — hierarchical attributes (e.g. `CategoryName`, `DepartmentName`) live inside the same table as the level they belong to, causing redundancy.
- The fact table is normalized.
- Referential integrity constraints exist between the fact table and each dimension table.
- Pro: fast queries (few joins). Con: more storage due to redundancy.

### Snowflake schema
- Removes star-schema redundancy by **normalizing dimension tables** — a hierarchy like `Product → Category → Department` becomes three separate tables instead of one.
- Pro: saves storage. Con: slower queries (more joins across the hierarchy).
- This is the classic **storage vs. performance** trade-off.

### Starflake schema
- A **combination** of star and snowflake: some dimensions are normalized (split), others are not — depending on how heavily that hierarchy is used.

### Constellation schema (galaxy schema)
- **Multiple fact tables** that share some dimension tables.
- Example: `Sales` and `Purchases` as two fact tables, both referencing the shared `Product` and `Time` dimensions — useful when a business has several processes (selling, purchasing) that must be analyzed along the same dimensions.

**Quick memory hook**: Star = fast, more storage. Snowflake = less storage, slower. Starflake = hybrid. Constellation = multiple facts, shared dimensions.

## 3. Relational Implementation of the Conceptual (MultiDim) Model

A set of rules translates the conceptual model into relational tables.

- **Rule 1** — a level `L` (not related to a fact with a one-to-one relationship) maps to a table `TL` containing all attributes of the level. A surrogate key may be added, otherwise the level's identifier becomes the table's key.
- **Rule 2** — a fact `F` maps to a table `TF` containing all measures of the fact. A surrogate key may be added.
- **Rule 3** — a relationship between a fact and a level, or between a parent level `LP` and a child level `LC`, is mapped according to its **cardinality**:
  - **Rule 3a (one-to-one)**: the table on the "one" side (`TF` or `TC`) is extended with all attributes of the other table.
  - **Rule 3b (one-to-many)**: the table on the "many" side (`TF` or `TC`) is extended with the **surrogate key (foreign key)** of the table on the "one" side (`TL` or `TP`). This is exactly how a star schema is built.
  - **Rule 3c (many-to-many)**: a new **bridge table** `TB` is created, containing the surrogate keys of both related tables. If the relationship has a distributing attribute, it is stored as an additional column in the bridge table.

### Worked example: Northwind Data Warehouse

The `Sales` fact table includes one foreign key for every level related to the fact with a one-to-many relationship: `CustomerKey`, `EmployeeKey`, `ProductKey`, `SupplierKey`, `ShipperKey`, and **three separate foreign keys** — `OrderDateKey`, `DueDateKey`, `ShippedDateKey` — that all reference the *same* `Time` dimension table.

This is called a **role-playing dimension**: one physical dimension table (`Time`) is referenced multiple times by the fact table, each foreign key playing a different "role" (order date, due date, shipped date). The `Time` table itself only needs one key column, `TimeKey`; it does not need to know it is being referenced three times.

```
Time
──────────
TimeKey (PK)
Date
DayNbWeek
...

Sales
──────────────────
CustomerKey      (FK)
EmployeeKey      (FK)
OrderDateKey      (FK) ──┐
DueDateKey        (FK) ──┼──►  Time.TimeKey
ShippedDateKey    (FK) ──┘
ShipperKey        (FK)
ProductKey        (FK)
SupplierKey       (FK)
OrderNo
OrderLineNo
UnitPrice, Quantity, Discount, SalesAmount, Freight
```

Because `Time` is a single physical table referenced three times, retrieving order date, due date and shipped date in one query requires **joining `Time` three times with three different aliases**:

```sql
SELECT s.OrderNo,
       t1.Date AS OrderDate,
       t2.Date AS DueDate,
       t3.Date AS ShippedDate
FROM Sales s
JOIN Time t1 ON s.OrderDateKey   = t1.TimeKey
JOIN Time t2 ON s.DueDateKey     = t2.TimeKey
JOIN Time t3 ON s.ShippedDateKey = t3.TimeKey;
```

Other notable mappings in the Northwind example:
- `Order` is related to the fact with a one-to-one relationship, so it is mapped as a **degenerate dimension** — its attributes (`OrderNo`, `OrderLineNo`) sit directly inside `Sales` rather than in a separate table.
- The many-to-many relationship between `Employee` and `Territory` is mapped (Rule 3c) to a bridge table `Territories`, containing both `EmployeeKey` and `CityKey`.
- `Customer` has a surrogate key `CustomerKey` plus an alternate/database key `CustomerAltKey` (`CustomerID`); `SupplierKey` in `Supplier` is a database key.

## 4. The Time Dimension

- A data warehouse is a **historical database**, so a time dimension is present in almost every warehouse.
- In OLTP systems, temporal information is usually a plain `DATE` attribute, with derived facts (e.g. "is this a weekend?") **computed on the fly** using functions.
- In a data warehouse, time information is **stored as explicit attributes** in the time dimension (`WeekdayFlag`, `WeekendFlag`, `Season`, ...), so it can be queried directly without recomputation:

```sql
-- Total sales during weekends, using the WeekendFlag stored in the Time dimension
SELECT SUM(SalesAmount)
FROM Time T, Sales S
WHERE T.TimeKey = S.TimeKey AND T.WeekendFlag;
```

- The **granularity** of the time dimension depends on its intended use. A time dimension with `month` granularity spanning 5 years has 5 × 12 = 60 rows.

## References
A. Vaisman, E. Zimanyi, *Data Warehouse Systems: Design and Implementation*, Chapter 5 "Logical Data Warehouse Design", Springer Verlag, 2014.
