# Data Warehouse Concepts


## 1. OLAP vs OLTP

### OLTP (Online Transaction Processing)
Traditional database systems designed and tuned to support day-to-day operations.

- Ensure fast, concurrent access to data
- Transaction processing and concurrency control
- Focus on online update / data consistency
- Also known as **operational databases**

**Characteristics:**
- Detailed data (row-level, no aggregation)
- Do **not** keep historical data — only the current state
- **Highly normalized** (1NF/2NF/3NF) to avoid insert/update/delete anomalies
- Poor performance on complex analytical queries (heavy joins, aggregation)

Typical OLTP query: *"pending orders for a customer"*

### OLAP (Online Analytical Processing)
A new paradigm needed for data analysis, since normalization (good for OLTP) makes analytical/aggregation queries slow (too many joins).

Typical OLAP query: *"total sales amount by product and by customer"*

**OLAP characteristics:**
- Focused on analytical queries rather than transactions
- Normalization is not helpful; reconstructing data requires many joins
- Supports a heavy, complex query load
- OLTP indexing techniques (designed to access few rows) are not efficient for OLAP (which typically aggregates over many rows)

### Data Warehouse
A (usually) large repository that:
- Consolidates data from different sources (internal and external to the organization)
- Is updated **offline** (batch, not real-time like OLTP)
- Follows the **multidimensional data model**
- Is designed/optimized to efficiently support OLAP queries

**Key contrast:** OLTP uses the ER model + normalization (optimized for consistent writes). OLAP/DW uses the multidimensional model + deliberate denormalization (optimized for reads/aggregation), trading off some write-consistency because a DW is not written to continuously like an OLTP system.

## 2. The Multidimensional Model

### Data cube
A view of data in n-dimensional space. A data cube is composed of **dimensions** and **facts**.

Classic example: a 3-D cube for sales data with dimensions `Product`, `Time`, `Customer`, and measure `Quantity`.

### Core building blocks

| Concept | Definition |
|---|---|
| **Dimension** | An axis/perspective used to analyze the data (e.g., `Product`, `Time`, `Customer`) |
| **Member** | A concrete value on a dimension, at a specific level (e.g., `Seafood`, `Beverages` are members of `Product` at level `Category`) |
| **Attribute** | Descriptive information attached to a member (e.g., `Product` has attributes `ProductNumber`, `UnitPrice`); attributes do **not** participate in defining a fact |
| **Fact / Cell** | The intersection obtained by choosing exactly one member from **each** dimension; each such combination identifies a unique cell |
| **Measure** | The numeric value stored inside a fact/cell (e.g., `Quantity`) |
| **Granularity** | The level of detail at which measures are represented, for each dimension of the cube (e.g., sales aggregated to `Category`, `Quarter`, `City`) |

Important distinction: **Fact ≠ combination of attributes.** A fact is a combination of *members* (one per dimension). Attributes only describe a single member and never participate in identifying a fact. Changing an attribute (e.g., updating a product's price) does not create or remove a fact.

### Dense vs sparse cubes
- **Dense**: nearly every cell has a value.
- **Sparse** (the typical/common case): most cells are empty, because not every combination of dimension members actually occurs (e.g., not every customer buys every product category every quarter).

Implication: in practice, ROLAP systems store data as relational tables (fact + dimension tables) rather than a full dense array, because a full array would waste enormous space on sparse data.

### Hierarchies
A hierarchy defines a sequence of mappings relating lower-level (detailed) concepts to higher-level (more general) ones, allowing the same dimension to be viewed at several granularities.

- **Child** level: the lower level. **Parent** level: the higher level.
- **Leaf level**: the most detailed level. **Root level**: the most general level (usually `All`).
- **Dimension schema**: the full hierarchical structure of levels (a "blueprint", fixed once at design time).
- **Dimension instance**: all members at all levels, for actual data (can grow/change over time without touching the schema).

Example hierarchies:
```
Product:  All → Category → Product
Time:     All → Year → Semester → Quarter → Month → Day
Customer: All → Continent → Country → State → City → Customer
```

**Hierarchy vs Granularity** — a key distinction:
- **Hierarchy** = the entire, fixed structure of levels for a dimension (defined once, shared by every cube built on that dimension).
- **Granularity** = which single level of that hierarchy a *specific cube* stops at (chosen per cube; different cubes can use the same hierarchy at different granularities).

Consequences of granularity choice:
- Finer granularity → more cells/rows, but supports deeper drill-down.
- Coarser granularity → smaller/faster cube, but detail is permanently lost once aggregated (aggregation is lossy — you cannot "unSUM" a total back into its original components). Drilling down is only possible if a finer-grained source (the base fact table, or the original data) still exists somewhere in the system.
- Granularity must be **uniform** across an entire fact table — mixing granularities in one table causes double-counting or incorrect aggregates.
- Adding a **new member** at an existing level (e.g., a new product) does not require any schema change. Adding a **new level** finer than the current leaf level (e.g., going below `Product` to `Batch`) *is* a schema-level change, and historical data at that new finer level cannot be reconstructed retroactively if it was never captured.

## 3. Classification of Measures

### By additivity (whether SUM makes sense along a dimension)
- **Additive**: can be meaningfully summarized along *all* dimensions using addition. The most common type (e.g., quantity sold, revenue).
- **Semiadditive**: can be summarized using addition along *some* dimensions but not others. Classic example: inventory level — additive across `Product`, but **not** across `Time` (you cannot add end-of-January stock to end-of-February stock to get a meaningful "two-month stock").
- **Nonadditive**: cannot be meaningfully summed along *any* dimension (e.g., unit price, exchange rate). Must instead use another aggregate (e.g., `AVG`).

### By computability
- **Distributive**: can be computed in a "divide and conquer" fashion — partition the data, aggregate each partition, then combine the partial results, and get the same answer as aggregating the whole set at once. `SUM`, `COUNT`, `MIN`, `MAX` are distributive.
  - **Warning**: `COUNT DISTINCT` is **not** distributive. Example: S = {3,3,4,5,8,4,7,3,8}. Partitioned into {3,3,4}, {5,8,4}, {7,3,8}: COUNT DISTINCT per partition = 2, 3, 3 → sum = 8. But COUNT DISTINCT over the whole S = 5. Mismatch, because 3 is double-counted across partitions.
- **Algebraic**: not distributive by itself, but computable from other distributive measures via a scalar formula. Example: `AVG = SUM / COUNT`.

**Design implication**: fact tables typically store the underlying distributive measures (SUM, COUNT) rather than only algebraic ones (AVG), so that correct re-aggregation is possible at any granularity without returning to the raw detailed data.

## 4. OLAP Operations

Starting cube (example): quarterly sales by product category and customer city.

| Operation | Meaning | Rough SQL analogue |
|---|---|---|
| **Roll-up** | Aggregate up a dimension hierarchy (coarser granularity) | `GROUP BY` at a higher level + aggregate function |
| **Drill-down** | Opposite of roll-up; move to a more detailed level | Removing a grouping condition to see more detail |
| **Slice** | Fix a single value on one dimension, reducing the number of dimensions | `WHERE dim = value` |
| **Dice** | Filter with a (possibly complex, Boolean) condition on multiple dimensions; number of dimensions unchanged | `WHERE (complex AND/OR condition)` |
| **Pivot** | Rotate axes for a different visualization; does **not** change granularity | No direct SQL equivalent — OLAP-specific |
| **Sort** | Order members by name or by value | `ORDER BY` |

**Slice vs Dice**: Slice fixes exactly one value on exactly one dimension and *reduces dimensionality*. Dice applies an arbitrary Boolean condition (possibly multiple values, multiple dimensions, AND/OR) and *keeps the same dimensionality*, only reducing the number of facts.

### Formal algebraic operators (from the slides)

```
ROLLUP(CubeName, (Dimension → Level)*, AggFunction(Measure)*)
ROLLUP(Sales, Customer → Country, SUM(Quantity))
```
Extended roll-up — drops all dimensions not involved in the operation:
```
ROLLUP*(CubeName, [(Dimension → Level)*], AggFunction(Measure)*)
```
Recursive roll-up — aggregates over a recursive hierarchy (a level that rolls up to itself):
```
RECOLLUP(CubeName, Dimension → Level, AggFunction(Measure)*)
```
Drill-down — moves from a general to a more detailed level:
```
DRILLDOWN(CubeName, (Dimension → Level)*)
```
Sort:
```
SORT(CubeName, Dimension, Expression [ASC | DESC])
```
`NAME` is a predefined keyword representing the name of a member.

Pivot (axes specified as {X, Y, Z, X1, Y1, Z1, ...}):
```
PIVOT(CubeName, (Dimension → Axis)*)
```
Slice (drops a dimension by fixing a single value; assumes the cube's granularity matches the specified level):
```
SLICE(CubeName, Dimension, Level = Value)
```
Dice (`?` is a Boolean condition over dimension levels, attributes, and measures):
```
DICE(CubeName, ?)
```

### Worked numeric example

Base cube (granularity: Category, Quarter, City):

| Category | Quarter | City | Quantity |
|---|---|---|---|
| Beverages | Q1 | Hanoi | 50 |
| Beverages | Q1 | Danang | 30 |
| Beverages | Q2 | Hanoi | 60 |
| Beverages | Q2 | Danang | 35 |
| Seafood | Q1 | Hanoi | 20 |
| Seafood | Q1 | Danang | 15 |
| Seafood | Q2 | Hanoi | 25 |
| Seafood | Q2 | Danang | 18 |

**Question**: total Quantity of Beverages across H1 (Q1+Q2), across both cities combined.

This requires handling each dimension separately:
1. **Slice** on `Product`: fix `Category = 'Beverages'` (drops the Product dimension) → 2-D sub-cube (Quarter, City).
2. **Roll-up** on `Time`: `Quarter → Semester` (SUM) → Hanoi H1 = 50+60 = 110; Danang H1 = 30+35 = 65.
3. **Roll-up** on `Customer`: `City → Country` (SUM) → Vietnam H1 = 110+65 = **175**.

Each dimension in the question needs its own, distinct operation (slice on Product ≠ roll-up on Time ≠ roll-up on Customer) — they cannot be collapsed into a single generic "group by everything" step.

## 5. Data Warehouse Architecture

```
[Data sources] → [Back-end tier] → [Data warehouse tier] → [OLAP tier] → [Front-end tier]
```

A one-directional pipeline; each tier consumes the previous tier's output.

### 1. Data sources
- **Internal sources**: operational (OLTP) databases.
- **External sources**: files, partner data, purchased data, web data, etc.

### 2. Back-end tier
- **ETL (Extract, Transform, Load)**:
  - *Extract*: pull raw data from sources.
  - *Transform*: clean (nulls, duplicates, format inconsistencies), standardize, re-aggregate to the target granularity, map keys (surrogate keys) — this is where the shift from normalized OLTP to the multidimensional DW model actually happens.
  - *Load*: write the transformed data into the warehouse.
- **Data staging area**: an intermediate database where integration/transformation runs, *before* data is loaded into the production data warehouse. Kept separate from production DW for two reasons: (a) isolates dirty/in-progress data so it never corrupts or is visible in the production warehouse, and (b) avoids overloading the production DW (heavy transform operations run elsewhere, without slowing down OLAP queries for end users).

### 3. Data warehouse tier
- **Enterprise Data Warehouse (EDW)**: the central, organization-wide warehouse.
- **Data marts**: smaller, subject-/department-specific warehouses (often derived from the EDW, sometimes built independently — the slides use "and/or", meaning an architecture is not required to have both).
- **Metadata repository**: stores information *about* the warehouse and its contents (schema, hierarchies, measure types, lineage, refresh times) — this is where the conceptual (MultiDim) schema lives.

### 4. OLAP tier
- **OLAP server**: provides a multidimensional (cube) view of the data, regardless of how data is physically stored underneath. Common storage strategies (useful background, not always in these particular slides):
  - **ROLAP** (Relational OLAP): data physically stored as relational tables (fact + dimension tables, i.e., star/snowflake schema); the OLAP server translates cube operations into SQL.
  - **MOLAP** (Multidimensional OLAP): data physically stored as a multidimensional array; faster but can be costly for sparse cubes.
  - **HOLAP** (Hybrid OLAP): detail data in ROLAP, pre-aggregated summaries in MOLAP.

### 5. Front-end tier
Client tools used for data analysis and visualization: OLAP tools, reporting tools, statistical tools, data-mining tools.

## Cross-references to prior (ER/SQL) knowledge

| You already know (SQL/ER) | New (DW) knowledge |
|---|---|
| OLTP database, daily CRUD operations | OLAP: analysis/aggregation over large data |
| Normalization (reduces redundancy, avoids anomalies) | Deliberate denormalization in DW to optimize reads |
| `GROUP BY`, `WHERE`, aggregate functions (`SUM`/`COUNT`/`AVG`) | Roll-up, Slice/Dice, distributive/algebraic measures |
